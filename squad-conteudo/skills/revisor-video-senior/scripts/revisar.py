#!/usr/bin/env python3
"""
revisor-video-senior · controle de qualidade de vídeos para redes sociais
Skill gratuita da Trentin Solutions · trentinsolutions.com.br · CC BY 4.0

Comandos:
  preparar                                   instala dependências e baixa o modelo de transcrição
  revisar VIDEO [--briefing B.json] [--config C.json] [--plataforma reels] [--saida pasta]
                                             analisa o vídeo e gera revisao.json, revisao.html e candidatos.jpg
  relatorio PASTA/revisao.json               refaz nota e HTML depois de marcar falsos positivos
"""
import json, math, os, re, subprocess, sys, shutil, unicodedata, base64
from pathlib import Path

CACHES = [Path.home() / '.cache' / 'revisor-video-senior', Path.home() / '.cache' / 'editor-video-senior']
CACHE = Path(os.environ.get('REVISOR_VIDEO_CACHE', CACHES[0]))
WHISPER_URL = 'https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.tar.bz2'
YUNET_URL = 'https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx'

# ---------------------------------------------------------------- regras por plataforma
# zonas em pixels de uma tela 1080x1920 (9:16) ou 1080x1350 (4:5) ou 1920x1080 (16:9)
PLATAFORMAS = {
    'reels':  {'aspecto': 9 / 16, 'min_res': (1080, 1920), 'dur_max': 180, 'topo': 220, 'base': 420, 'direita': 150, 'direita_y': (800, 1700)},
    'stories': {'aspecto': 9 / 16, 'min_res': (1080, 1920), 'dur_max': 60, 'topo': 250, 'base': 340, 'direita': 0, 'direita_y': (0, 0)},
    'tiktok': {'aspecto': 9 / 16, 'min_res': (1080, 1920), 'dur_max': 600, 'topo': 160, 'base': 480, 'direita': 150, 'direita_y': (700, 1600)},
    'shorts': {'aspecto': 9 / 16, 'min_res': (1080, 1920), 'dur_max': 180, 'topo': 160, 'base': 400, 'direita': 150, 'direita_y': (900, 1650)},
    'feed':   {'aspecto': 4 / 5, 'min_res': (1080, 1350), 'dur_max': 3600, 'topo': 0, 'base': 0, 'direita': 0, 'direita_y': (0, 0)},
    'youtube': {'aspecto': 16 / 9, 'min_res': (1920, 1080), 'dur_max': 43200, 'topo': 0, 'base': 0, 'direita': 0, 'direita_y': (0, 0)},
    'linkedin': {'aspecto': None, 'min_res': (1080, 1080), 'dur_max': 600, 'topo': 0, 'base': 0, 'direita': 0, 'direita_y': (0, 0)},
}
PESO = {'erro': 12, 'alerta': 4, 'info': 0}


def sh(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def norm(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^A-Z0-9]', '', s.upper())


def ratio(a, b):
    """similaridade 0..1 (Levenshtein normalizado)"""
    if not a and not b:
        return 1.0
    la, lb = len(a), len(b)
    prev = list(range(lb + 1))
    for i in range(1, la + 1):
        cur = [i] + [0] * lb
        for j in range(1, lb + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] != b[j - 1]))
        prev = cur
    return 1 - prev[lb] / max(la, lb)



def ocr_norm(s):
    """normaliza e corrige confusões comuns do OCR entre letras e números"""
    n = norm(s)
    if sum(ch.isdigit() for ch in n) < len(n) / 2:
        n = n.translate(str.maketrans('0158', 'OISB'))
    return n


def contem(s, w):
    """w aparece em s, tolerando 1 erro de leitura a cada 5 letras"""
    if not w:
        return False
    if w in s:
        return True
    L = len(w)
    if L < 4:
        return False
    tol = 1 - max(1, L // 5) / L - 1e-9
    for k in (L - 1, L, L + 1):
        for i in range(0, max(1, len(s) - k + 1)):
            if ratio(s[i:i + k], w) >= tol:
                return True
    return False


def formavel(n, ref):
    """n é a junção de até 3 palavras de referência (o OCR às vezes junta palavras)"""
    from functools import lru_cache
    @lru_cache(None)
    def ok(i, partes):
        if i == len(n):
            return True
        if partes == 3:
            return False
        return any(ok(j, partes + 1) for j in range(i + 1, len(n) + 1) if n[i:j] in ref)
    return ok(0, 0)


def parece_legenda(txt, ref):
    toks = [ocr_norm(x) for x in txt.split() if ocr_norm(x)]
    return bool(toks) and sum(1 for t in toks if t in ref or formavel(t, ref)) >= 0.6 * len(toks)


# ---------------------------------------------------------------- preparar
def achar_whisper():
    for c in [CACHE] + CACHES:
        d = c / 'sherpa-onnx-whisper-small'
        if (d / 'small-encoder.onnx').exists():
            return d
    return None


def preparar():
    pkgs = {'numpy': 'numpy', 'cv2': 'opencv-python-headless', 'PIL': 'pillow', 'soundfile': 'soundfile',
            'sherpa_onnx': 'sherpa-onnx', 'rapidocr_onnxruntime': 'rapidocr-onnxruntime', 'onnxruntime': 'onnxruntime'}
    falta = []
    for mod, pkg in pkgs.items():
        try:
            __import__(mod)
        except ImportError:
            falta.append(pkg)
    if falta:
        sh([sys.executable, '-m', 'pip', 'install', '-q', '--break-system-packages', *falta])
    if not achar_whisper():
        CACHE.mkdir(parents=True, exist_ok=True)
        print('baixando modelo de transcrição (~640 MB)...', flush=True)
        sh(['curl', '-sSL', '-o', str(CACHE / 'w.tar.bz2'), WHISPER_URL])
        sh(['tar', 'xjf', str(CACHE / 'w.tar.bz2'), '-C', str(CACHE)])
        (CACHE / 'w.tar.bz2').unlink()
    CACHE.mkdir(parents=True, exist_ok=True)
    if not (CACHE / 'yunet.onnx').exists():
        print('baixando detector de rostos (YuNet, ~230 KB)...', flush=True)
        sh(['curl', '-sSL', '-o', str(CACHE / 'yunet.onnx'), YUNET_URL])
    print('pronto')


# ---------------------------------------------------------------- medições
def probe(video):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                        'format=duration,bit_rate:stream=codec_type,codec_name,width,height,avg_frame_rate,sample_rate,channels',
                        '-of', 'json', video], capture_output=True, text=True)
    j = json.loads(r.stdout)
    v = next((s for s in j['streams'] if s['codec_type'] == 'video'), {})
    a = next((s for s in j['streams'] if s['codec_type'] == 'audio'), None)
    num, den = (v.get('avg_frame_rate', '30/1') + '/1').split('/')[:2]
    return {'duracao': float(j['format'].get('duration', 0)), 'bitrate': int(j['format'].get('bit_rate', 0) or 0),
            'largura': v.get('width'), 'altura': v.get('height'), 'fps': float(num) / max(1.0, float(den)),
            'codec_video': v.get('codec_name'), 'audio': bool(a), 'codec_audio': a.get('codec_name') if a else None}


def loudness(video):
    r = subprocess.run(['ffmpeg', '-nostats', '-i', video, '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True)
    txt = r.stderr[r.stderr.rfind('Summary:'):]
    I = re.search(r'I:\s+(-?[\d.]+) LUFS', txt)
    TP = re.search(r'Peak:\s+(-?[\d.]+) dBFS', txt)
    return (float(I.group(1)) if I else None, float(TP.group(1)) if TP else None)


def silencios(wav, db=-30, dur=0.12):
    r = subprocess.run(['ffmpeg', '-i', wav, '-af', f'silencedetect=n={db}dB:d={dur}', '-f', 'null', '-'],
                       capture_output=True, text=True)
    out, cur = [], None
    for ln in r.stderr.splitlines():
        if 'silence_start:' in ln:
            cur = float(ln.split('silence_start:')[1].split()[0])
        elif 'silence_end:' in ln and cur is not None:
            out.append([max(0.0, cur), float(ln.split('silence_end:')[1].split()[0])]); cur = None
    if cur is not None:
        out.append([cur, 1e9])
    return out


def cortes_de_cena(video):
    r = subprocess.run(['ffmpeg', '-i', video, '-vf', "select='gt(scene,0.08)',showinfo", '-f', 'null', '-'],
                       capture_output=True, text=True)
    brutos = [float(l.split('pts_time:')[1].split()[0]) for l in r.stderr.splitlines() if 'pts_time:' in l]
    cortes = []
    for c in brutos:
        if not cortes or c - cortes[-1] > 0.3:
            cortes.append(c)
    return cortes


def detectar(video, filtro, chave):
    r = subprocess.run(['ffmpeg', '-i', video, '-vf', filtro, '-an', '-f', 'null', '-'], capture_output=True, text=True)
    return [ln for ln in r.stderr.splitlines() if chave in ln]


# ---------------------------------------------------------------- transcrição
def transcrever(wav, total):
    import numpy as np, soundfile as sf, sherpa_onnx
    d = achar_whisper()
    if not d:
        raise SystemExit('modelo de transcrição ausente: rode "revisar.py preparar"')
    sil_f = silencios(wav, -35, 0.3)
    sil_i = silencios(wav, -30, 0.12)
    fala, cur = [], 0.0
    for s, e in sil_f:
        if s > cur:
            fala.append([max(0, cur - 0.05), min(total, s + 0.05)])
        cur = max(cur, e)
    if cur < total - 0.05:
        fala.append([max(0, cur - 0.05), total])
    fala = [f for f in fala if f[1] - f[0] > 0.12]
    # trechos curtos (até ~4 s) cortados no ponto mais baixo de energia: no vídeo final, efeitos e música
    # enchem as pausas e o Whisper pula frases inteiras em trechos longos
    audio_full, sr_full = sf.read(wav, dtype='float32')
    hop = int(0.05 * sr_full)
    rms = np.array([np.sqrt(np.mean(audio_full[k:k + hop] ** 2)) for k in range(0, len(audio_full), hop)])
    final = []
    for a, b in fala:
        pend = [[a, b]]
        while pend:
            x, y = pend.pop(0)
            if y - x <= 4.5:
                final.append([x, y]); continue
            i0, i1 = int((x + 1.2) / 0.05), int((y - 1.2) / 0.05)
            k = i0 + int(np.argmin(rms[i0:i1])) if i1 > i0 else int((x + y) / 2 / 0.05)
            c = k * 0.05 + 0.025
            pend[:0] = [[x, c], [c, y]]
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=str(d / 'small-encoder.onnx'), decoder=str(d / 'small-decoder.onnx'), tokens=str(d / 'small-tokens.txt'),
        language='pt', task='transcribe', num_threads=os.cpu_count() or 2)
    audio, sr = sf.read(wav, dtype='float32')
    frases, palavras = [], []
    for a, b in final:
        st = rec.create_stream(); st.accept_waveform(sr, audio[int(a * sr):int(b * sr)]); rec.decode_stream(st)
        txt = st.result.text.strip()
        frases.append({'de': round(a, 2), 'ate': round(b, 2), 'texto': txt})
        # tempo de cada palavra: proporcional dentro das ilhas de fala
        isl, c = [], a
        for s, e in sil_i:
            if e <= a or s >= b:
                continue
            if s > c:
                isl.append((c, min(s, b)))
            c = max(c, e)
        if c < b:
            isl.append((c, b))
        isl = isl or [(a, b)]
        ws = txt.split()
        if not ws:
            continue
        wts = np.array([len(w) + 1.5 for w in ws]); tot = sum(e - s for s, e in isl)
        cum = np.concatenate([[0], np.cumsum(wts)]) / wts.sum() * tot

        def src_at(dd):
            for s, e in isl:
                if dd <= e - s:
                    return s + dd
                dd -= e - s
            return isl[-1][1]
        for i, w in enumerate(ws):
            palavras.append({'t': round(src_at(cum[i] + 1e-4), 2), 'fim': round(src_at(cum[i + 1] - 1e-4), 2), 'p': w})
    return frases, palavras, sil_i


# ---------------------------------------------------------------- visão
class Visao:
    def __init__(self):
        import cv2
        from rapidocr_onnxruntime import RapidOCR
        self.cv2 = cv2
        self.ocr = RapidOCR()
        m = CACHE / 'yunet.onnx'
        if not m.exists():
            raise SystemExit('detector de rostos ausente: rode "revisar.py preparar"')
        self.face = cv2.FaceDetectorYN.create(str(m), '', (320, 320), 0.7, 0.3, 50)

    def textos(self, rgb, escala):
        bgr = self.cv2.cvtColor(rgb, self.cv2.COLOR_RGB2BGR)
        r, _ = self.ocr(bgr)
        out = []
        for box, txt, conf in (r or []):
            xs = [p[0] for p in box]; ys = [p[1] for p in box]
            if float(conf) < 0.6 or len(norm(txt)) == 0:
                continue
            out.append({'texto': txt, 'conf': round(float(conf), 2),
                        'box': [min(xs) / escala, min(ys) / escala, max(xs) / escala, max(ys) / escala]})
        return out

    def rostos(self, rgb, escala):
        bgr = self.cv2.cvtColor(rgb, self.cv2.COLOR_RGB2BGR)
        h, w = bgr.shape[:2]
        self.face.setInputSize((w, h))
        _, fs = self.face.detect(bgr)
        out = []
        for f in (fs if fs is not None else []):
            x, y, fw, fh = f[:4]
            if fw * fh < (0.03 * h) ** 2:
                continue
            out.append([float(x / escala), float(y / escala), float((x + fw) / escala), float((y + fh) / escala)])
        return out


def inter(a, b):
    x0, y0, x1, y1 = max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])
    return max(0, x1 - x0) * max(0, y1 - y0)


def cor_do_texto(rgb_full, box, ignorar=None, todas=False):
    """estima a cor do texto: cluster mais uniforme dentro da caixa (fora do rosto)"""
    import numpy as np, cv2
    x0, y0, x1, y1 = [int(v) for v in box]
    reg = rgb_full[max(0, y0):y1, max(0, x0):x1].reshape(-1, 3).astype(np.float32)
    if ignorar is not None:
        m = np.ones((max(0, y1 - max(0, y0)), max(0, x1 - max(0, x0))), bool)
        ix0, iy0, ix1, iy1 = [int(v) for v in ignorar]
        m[max(0, iy0 - y0):max(0, iy1 - y0), max(0, ix0 - x0):max(0, ix1 - x0)] = False
        reg = reg[m.reshape(-1)] if m.size == len(reg) else reg
    if len(reg) < 30:
        return None
    _, lab, cen = cv2.kmeans(reg, 2, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0), 2, cv2.KMEANS_PP_CENTERS)
    lab = lab.reshape(-1)
    stds = [float(reg[lab == k].std(axis=0).mean()) if (lab == k).sum() > 10 else 1e9 for k in range(2)]
    k = int(np.argmin(stds))
    if todas:  # cor do texto e, se for uniforme, a cor da placa/pílula por trás dele
        return [cen[i] for i in range(2) if i == k or stds[i] < 28]
    return cen[k]


# ---------------------------------------------------------------- revisão
class Revisao:
    def __init__(self, video, briefing=None, config=None, plataforma=None, saida=None):
        self.video = video
        self.saida = Path(saida or 'revisao'); self.saida.mkdir(parents=True, exist_ok=True)
        (self.saida / 'quadros').mkdir(exist_ok=True)
        self.b = json.load(open(briefing)) if briefing else {}
        self.cfg = json.load(open(config)) if config else None
        self.cfg_dir = Path(config).parent if config else Path('.')
        self.plat = plataforma or self.b.get('plataforma') or None
        self.achados = []

    def add(self, grav, cat, msg, tempo=None, sugestao=None, boxes=None, dados=None, visual=False, chave=None, janela=2.0):
        if chave is not None:
            for a in self.achados:
                if a.get('_chave') == chave and (janela is None or tempo is None or a['tempo'] is None or abs(a['tempo'] - tempo) < janela):
                    return
        self.achados.append({'_chave': chave} | {'id': len(self.achados) + 1, 'gravidade': grav, 'categoria': cat, 'mensagem': msg,
                             'tempo': None if tempo is None else round(tempo, 2), 'sugestao': sugestao,
                             'boxes': boxes or [], 'dados': dados or {}, 'precisa_olhar': visual, 'confirmado': None})

    # ---------- briefing a partir do config do editor ----------
    def contexto(self):
        b = dict(self.b)
        if self.cfg:
            c = self.cfg
            b.setdefault('cores', list(c['marca']['cores'].values()))
            if c['marca'].get('logo'):
                lp = self.cfg_dir / c['marca']['logo']
                if lp.exists():
                    b.setdefault('logo', str(lp))
            b.setdefault('fala_esperada', ' '.join(t['texto'] for t in c['trechos']))
            textos = [e.get('texto', '') for e in c.get('elementos', [])]
            textos += [i.get('texto', '') for i in c.get('tela_final', {}).get('itens', [])]
            b.setdefault('textos_aprovados', [t for t in textos if t])
            b.setdefault('legendas', c.get('legendas', {}).get('estilo', 'karaoke') != 'nenhuma')
            if c.get('tela_final'):
                b.setdefault('cta', [i['texto'] for i in c['tela_final'].get('itens', []) if i.get('tipo') in ('botao', 'link')])
            fala = b['fala_esperada']
            nomes = []
            for frase in re.split(r'[.?!]\s*', fala):
                ws = frase.split()
                nomes += [w.strip(',;:') for w in ws[1:] if w[:1].isupper() and len(w.strip(',;:')) >= 4]
            b.setdefault('nomes_proprios', sorted(set(nomes)))
            W, H = c.get('formato', {}).get('largura', 1080), c.get('formato', {}).get('altura', 1920)
            if not self.plat:
                self.plat = 'reels' if abs(W / H - 9 / 16) < 0.02 else ('feed' if abs(W / H - 0.8) < 0.02 else 'youtube')
        self.ctx = b
        if not self.plat:
            self.plat = 'reels'

    # ---------- execução ----------
    def rodar(self, fps_ocr=4):
        import numpy as np, cv2
        self.contexto()
        m = probe(self.video); self.meta = m
        W, H = m['largura'], m['altura']
        P = PLATAFORMAS.get(self.plat, PLATAFORMAS['reels'])
        self.ref_W = 1080
        self.k = W / 1080 if P['aspecto'] and P['aspecto'] < 1 else W / 1920  # px reais por px de referência
        # ---- formato
        asp = W / H
        if P['aspecto'] and abs(asp - P['aspecto']) > 0.02:
            self.add('erro', 'formato', f'Proporção {W}x{H} não é a de {self.plat} ({P["aspecto"]:.3f}).', sugestao='Exportar no formato da plataforma.')
        if W < P['min_res'][0] or H < P['min_res'][1]:
            self.add('alerta', 'formato', f'Resolução {W}x{H} abaixo do recomendado ({P["min_res"][0]}x{P["min_res"][1]}).', sugestao='Exportar em 1080p ou mais.')
        if m['duracao'] > P['dur_max']:
            self.add('erro', 'formato', f'Duração {m["duracao"]:.1f}s acima do limite de {self.plat} ({P["dur_max"]}s).')
        if m['fps'] < 24 or m['fps'] > 61:
            self.add('alerta', 'formato', f'Taxa de quadros incomum: {m["fps"]:.2f} fps.')
        if m['codec_video'] not in ('h264', 'hevc'):
            self.add('alerta', 'formato', f'Codec de vídeo {m["codec_video"]}: prefira H.264.')
        if not m['audio']:
            self.add('alerta', 'som', 'Vídeo sem faixa de áudio.')
        # ---- som
        wav = str(self.saida / 'audio16k.wav')
        frases, palavras, sil = [], [], []
        if m['audio']:
            sh(['ffmpeg', '-y', '-v', 'error', '-i', self.video, '-ac', '1', '-ar', '16000', wav])
            I, TP = loudness(self.video)
            self.som = {'lufs': I, 'pico_db': TP}
            alvo = self.b.get('lufs_alvo', -14)
            if I is not None and abs(I - alvo) > 2:
                self.add('alerta' if abs(I - alvo) <= 4 else 'erro', 'som', f'Volume médio {I:.1f} LUFS; o alvo das redes é {alvo} LUFS.',
                         sugestao='Normalizar com loudnorm=I=-14:TP=-1.5.')
            if TP is not None and TP > -0.5:
                self.add('erro', 'som', f'Pico de {TP:.1f} dBFS: risco de estouro (clipping).', sugestao='Limitar o pico em -1,5 dBFS.')
            frases, palavras, sil = transcrever(wav, m['duracao'])
            # fala cortada no início/fim
            import soundfile as sf
            a0, sr0 = sf.read(wav, dtype='float32')
            ini_db = 20 * np.log10(np.sqrt(np.mean(a0[:int(0.03 * sr0)] ** 2)) + 1e-9)
            if palavras and palavras[-1]['fim'] > m['duracao'] - 0.12:
                self.add('erro', 'cortes', 'A fala termina colada no fim do vídeo: a última palavra pode estar cortada.',
                         tempo=m['duracao'] - 0.3, sugestao='Deixar 0,3 s de respiro depois da última palavra.')
            if ini_db > -32:
                self.add('alerta', 'cortes', 'A fala começa no primeiro quadro: a primeira sílaba pode estar cortada.', tempo=0,
                         sugestao='Começar o corte 0,05 a 0,1 s antes da primeira palavra.')
        self.frases, self.palavras = frases, palavras
        # ---- cortes no meio da fala e cliques
        cortes = cortes_de_cena(self.video)
        self.cortes = cortes
        if m['audio'] and cortes:
            import soundfile as sf
            a, sr = sf.read(wav, dtype='float32')
            for c in cortes:
                i = int(c * sr); w = int(0.03 * sr)
                if i - w < 0 or i + w >= len(a):
                    continue
                antes = 20 * np.log10(np.sqrt(np.mean(a[i - w:i] ** 2)) + 1e-9)
                depois = 20 * np.log10(np.sqrt(np.mean(a[i:i + w] ** 2)) + 1e-9)
                d = np.abs(np.diff(a[i - int(0.005 * sr):i + int(0.005 * sr)]))
                base = np.median(np.abs(np.diff(a[i - w:i + w]))) + 1e-6
                # emenda de áudio no meio da fala: com fade curto, aparece um "buraco" de energia de ~10-30 ms
                # bem no corte; zoom/punch-in sem corte de áudio não tem esse buraco
                w5 = int(0.005 * sr)
                mini = min(20 * np.log10(np.sqrt(np.mean(a[k:k + w5] ** 2)) + 1e-9) for k in range(i - 3 * w5, i + 3 * w5, w5))
                if min(antes, depois) > -24 and mini < min(antes, depois) - 15:
                    self.add('alerta', 'cortes', f'Corte em {c:.2f}s com fala dos dois lados ({antes:.0f}/{depois:.0f} dB): possível palavra cortada.',
                             tempo=c, sugestao='Mover o corte para a pausa mais próxima.', visual=False, dados={'corte': c})
                elif d.max() > 25 * base and d.max() > 0.08:
                    self.add('alerta', 'cortes', f'Possível estalo no áudio no corte em {c:.2f}s.', tempo=c, sugestao='Aplicar fade de 10 a 15 ms no corte.')
        # ---- imagem: preto, congelado, flash
        for ln in detectar(self.video, 'blackdetect=d=0.1:pix_th=0.08', 'black_start'):
            s = float(re.search(r'black_start:([\d.]+)', ln).group(1)); e = float(re.search(r'black_end:([\d.]+)', ln).group(1))
            self.add('erro' if s > 0.05 else 'alerta', 'imagem', f'Tela preta de {s:.2f}s a {e:.2f}s.', tempo=s)
        fz = detectar(self.video, 'freezedetect=n=0.002:d=1.2', 'freeze_')
        st = None
        for ln in fz:
            if 'freeze_start' in ln:
                st = float(ln.split('freeze_start:')[1].split()[0])
            elif 'freeze_end' in ln and st is not None:
                en = float(ln.split('freeze_end:')[1].split()[0])
                if st < m['duracao'] - 4.5:  # tela final estática é normal
                    self.add('alerta', 'imagem', f'Imagem parada de {st:.2f}s a {en:.2f}s.', tempo=st, visual=True)
                st = None
        self.flash()
        # ---- quadros: OCR + rostos
        vis = Visao()
        cap = cv2.VideoCapture(self.video)
        fps = cap.get(5) or m['fps']
        n = int(cap.get(7))
        passo = max(1, int(round(fps / fps_ocr)))
        alvo_w = 720
        amostras = []
        idx = 0
        while True:
            ok = cap.grab()
            if not ok:
                break
            if idx % passo == 0:
                _, f = cap.retrieve()
                rgb = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
                esc = alvo_w / rgb.shape[1]
                small = cv2.resize(rgb, (alvo_w, int(rgb.shape[0] * esc)), interpolation=cv2.INTER_AREA)
                tx = vis.textos(small, esc)
                fc = vis.rostos(cv2.resize(rgb, (540, int(rgb.shape[0] * 540 / rgb.shape[1]))), 540 / rgb.shape[1])
                amostras.append({'t': idx / fps, 'textos': tx, 'rostos': fc, '_rgb': rgb if (tx and fc) else None})
            idx += 1
        self.amostras = amostras
        self.marcar_cenario()
        self.checar_emendas()
        self.checar_textos(P)
        self.checar_legendas()
        self.checar_conteudo()
        self.checar_marca()
        for a in self.amostras:
            a.pop('_rgb', None)
        self.salvar()

    def flash(self):
        import numpy as np, cv2
        cap = cv2.VideoCapture(self.video); fps = cap.get(5) or 30
        L = []
        while True:
            ok, f = cap.read()
            if not ok:
                break
            g = cv2.cvtColor(cv2.resize(f, (64, 114)), cv2.COLOR_BGR2GRAY)
            L.append(g.mean() / 255)
        L = np.array(L)
        if len(L) < 3:
            return
        d = np.diff(L)
        ev = [i for i in range(1, len(d)) if abs(d[i]) > 0.1 and np.sign(d[i]) != np.sign(d[i - 1]) and abs(d[i - 1]) > 0.1]
        win = int(fps)
        for i in ev:
            cnt = sum(1 for j in ev if i <= j < i + win)
            if cnt >= 3:
                self.add('erro', 'imagem', f'Flashes rápidos perto de {i / fps:.2f}s (3 ou mais por segundo): risco para pessoas fotossensíveis.',
                         tempo=i / fps, sugestao='Trocar por transição suave.')
                break

    # ---------- textos na tela: rosto, borda, áreas seguras ----------
    def checar_textos(self, P):
        import numpy as np
        m = self.meta; W, H = m['largura'], m['altura']
        sy = H / (1920 if (P['aspecto'] or 1) < 1 else 1080)
        sx = W / (1080 if (P['aspecto'] or 1) < 1 else 1920)
        vistos_borda, vistos_rosto, vistos_zona = set(), set(), set()
        zonas = {}
        com_rosto = [a for a in self.amostras if a['rostos']]
        for a in self.amostras:
            t = a['t']
            for tx in a['textos']:
                if tx.get('cenario'):
                    continue
                x0, y0, x1, y1 = tx['box']; h = y1 - y0
                chave = norm(tx['texto'])[:12]
                decor = h > 0.08 * H  # texto gigante decorativo
                # borda
                if (x0 < 0.006 * W or x1 > W * 0.994):
                    vistos_borda.add(chave)
                    self.add('alerta' if decor else 'erro', 'legibilidade',
                             f'Texto "{tx["texto"]}" encostado ou cortado na borda.', tempo=t, boxes=[tx['box']],
                             sugestao='Reduzir o tamanho ou afastar da borda (margem de 40 px).', visual=True, chave='borda')
                # áreas seguras (texto pequeno/médio)
                cy = (y0 + y1) / 2
                if not decor and t < m['duracao'] - 0.1:
                    zona = None
                    if P['topo'] and y0 < P['topo'] * sy and y1 < (P['topo'] + 60) * sy and y0 > 10:
                        zona = 'topo (nome do perfil e áudio)'
                    if P['base'] and y1 > H - P['base'] * sy:
                        zona = 'base (descrição e botões do app)'
                    if P['direita'] and x1 > W - P['direita'] * sx and P['direita_y'][0] * sy < cy < P['direita_y'][1] * sy:
                        zona = 'lateral direita (curtir, comentar, compartilhar)'
                    if zona:
                        zonas.setdefault(zona, []).append((t, tx))
                # rosto
                if a['_rgb'] is not None:
                    for fb0 in a['rostos']:
                        fw, fh = fb0[2] - fb0[0], fb0[3] - fb0[1]
                        fb = [fb0[0] - 0.1 * fw, fb0[1] - 0.45 * fh, fb0[2] + 0.1 * fw, fb0[3]]  # rosto + testa/cabelo
                        ar = (fb[2] - fb[0]) * (fb[3] - fb[1])
                        if ar <= 0 or inter(tx['box'], fb) / ar < 0.12:
                            continue
                        cores_tx = cor_do_texto(a['_rgb'], tx['box'], ignorar=fb, todas=True)
                        if not cores_tx:
                            continue
                        # mede só dentro do rosto (caixa justa): texto atrás da pessoa ocupa o fundo, não o rosto
                        ix0, iy0 = int(max(tx['box'][0], fb0[0])), int(max(tx['box'][1], fb0[1]))
                        ix1, iy1 = int(min(tx['box'][2], fb0[2])), int(min(tx['box'][3], fb0[3]))
                        if ix1 <= ix0 or iy1 <= iy0:
                            continue
                        reg = a['_rgb'][iy0:iy1, ix0:ix1].reshape(-1, 3).astype(np.float32)
                        if len(reg) == 0:
                            continue
                        perto = np.zeros(len(reg), bool)
                        for cor in cores_tx:
                            perto |= np.linalg.norm(reg - cor, axis=1) < 45
                        frac = float(perto.mean())
                        if frac > 0.15 and (chave, round(t)) not in vistos_rosto:
                            vistos_rosto.add((chave, round(t)))
                            self.add('erro', 'pessoas', f'Texto "{tx["texto"]}" sobre o rosto ({frac:.0%} da área do rosto coberta).',
                                     tempo=t, boxes=[tx['box'], fb0], sugestao='Mover o elemento ou colocá-lo atrás da pessoa.', visual=True,
                                     chave=('rosto', ocr_norm(tx['texto'])[:10]), janela=3.0)
        for zona, hits in zonas.items():
            textos = []
            for t, tx in hits:
                n = ocr_norm(tx['texto'])[:10]
                if n not in [ocr_norm(x['texto'])[:10] for _, x in textos]:
                    textos.append((t, tx))
            if len(textos) >= 3:
                t0, tx0 = textos[0]
                self.add('erro' if len(textos) >= 6 else 'alerta', 'plataforma',
                         f'{len(textos)} textos diferentes na área {zona}, de {textos[0][0]:.1f}s a {textos[-1][0]:.1f}s (ex.: "{tx0["texto"]}"). Essa área fica coberta em {self.plat}.',
                         tempo=t0, boxes=[tx0['box']], visual=True, sugestao='Subir as legendas ou os elementos para dentro da área segura.')
            else:
                for t, tx in textos:
                    self.add('alerta', 'plataforma', f'Texto "{tx["texto"]}" na área {zona}, que fica coberta em {self.plat}.',
                             tempo=t, boxes=[tx['box']], sugestao='Mover para dentro da área segura.', visual=True)
        # rosto que some enquanto há texto grande (possível oclusão não detectada)
        if len(com_rosto) > 0.6 * len(self.amostras):
            seq = 0
            for a in self.amostras:
                if not a['rostos'] and a['textos'] and a['t'] < self.meta['duracao'] - 4:
                    seq += 1
                    if seq == 3:
                        self.add('alerta', 'pessoas', f'Rosto não encontrado por alguns quadros perto de {a["t"]:.2f}s, com texto na tela: confira se algo cobre o rosto.',
                                 tempo=a['t'], visual=True)
                else:
                    seq = 0

    # ---------- legendas ----------
    def checar_legendas(self):
        import difflib
        if not self.palavras and not self.ctx.get('fala_esperada'):
            return
        esperadas = self.ctx.get('legendas', True)
        tela = [(a['t'], ocr_norm(' '.join(t['texto'] for t in a['textos'] if not t.get('cenario')))) for a in self.amostras]

        def na_tela(w, t0, t1):
            for t, s in tela:
                if t0 <= t <= t1 and contem(s, w):
                    return t
            return None
        # palavras de referência: texto aprovado (config/briefing) alinhado aos tempos da transcrição
        trans = [(norm(p['p']), p['t'], p['fim']) for p in self.palavras]
        exp_txt = self.ctx.get('fala_esperada')
        if exp_txt:
            exp = [w for w in exp_txt.split() if norm(w)]
            en = [norm(w) for w in exp]
            sm = difflib.SequenceMatcher(None, en, [x[0] for x in trans], autojunk=False)
            tempos = [None] * len(en)
            for a_, b_, n_ in sm.get_matching_blocks():
                for k in range(n_):
                    tempos[a_ + k] = (trans[b_ + k][1], trans[b_ + k][2])
            # interpola os que não casaram
            conhecidos = [i for i, x in enumerate(tempos) if x]
            for i in range(len(tempos)):
                if tempos[i] is None and conhecidos:
                    ant = max([k for k in conhecidos if k < i], default=None)
                    dep = min([k for k in conhecidos if k > i], default=None)
                    t0 = tempos[ant][1] if ant is not None else 0
                    t1 = tempos[dep][0] if dep is not None else self.meta['duracao']
                    tempos[i] = (t0, t1)
            ref_words = [(w, *(tempos[i] or (0, self.meta['duracao']))) for i, w in enumerate(exp)]
        else:
            ref_words = [(p['p'], p['t'], p['fim']) for p in self.palavras]
        cobertas, atrasos, faltando = 0, [], []
        alvo = [r for r in ref_words if len(norm(r[0])) >= 3]
        for w, t0, t1 in alvo:
            t = na_tela(ocr_norm(w), t0 - 0.8, t1 + 0.8)
            if t is not None:
                cobertas += 1
                if t1 - t0 < 1.5:
                    atrasos.append(t - t0)
            else:
                faltando.append((w, t0))
        cob = cobertas / max(1, len(alvo))
        self.legenda_stats = {'palavras': len(alvo), 'cobertura': round(cob, 2),
                              'atraso_mediano': round(sorted(atrasos)[len(atrasos) // 2], 2) if atrasos else None}
        if esperadas and alvo:
            if cob < 0.6:
                self.add('erro', 'legendas', f'Só {cob:.0%} das palavras faladas aparecem na legenda.',
                         sugestao='Conferir se a legenda está ligada e acompanha toda a fala.')
            elif cob < 0.9:
                ex = ', '.join(w for w, _ in faltando[:8])
                self.add('alerta', 'legendas', f'{cob:.0%} das palavras faladas aparecem na legenda. Ausentes: {ex}.',
                         tempo=faltando[0][1] if faltando else None, visual=True,
                         sugestao='Conferir esses trechos: legenda faltando, palavra diferente ou erro de leitura (OCR).')
            if atrasos:
                med = sorted(atrasos)[len(atrasos) // 2]
                if abs(med) > 0.35:
                    self.add('alerta', 'legendas', f'Legenda {"atrasada" if med > 0 else "adiantada"} em cerca de {abs(med):.2f}s em relação à fala.',
                             sugestao='Ajustar o tempo das legendas.')
        # vocabulário de referência
        ref = set()
        for x in [exp_txt or '', ' '.join(p['p'] for p in self.palavras)] + list(self.ctx.get('textos_aprovados', [])) + list(self.ctx.get('fatos', [])):
            for w in re.split(r'[\s·/|]+', x):
                n = ocr_norm(w)
                if n:
                    ref.add(n)
        # nomes próprios escritos diferente (estável em 2+ amostras)
        contagem = {}
        for a in self.amostras:
            for t in a['textos']:
                if t.get('cenario') or (t['box'][3] - t['box'][1]) > 0.08 * self.meta['altura']:
                    continue  # texto gigante decorativo costuma ficar parcialmente atrás da pessoa
                for tok in re.split(r'\s+', t['texto']):
                    n = ocr_norm(tok)
                    if len(n) >= 4:
                        c = contagem.setdefault(n, {'n': 0, 't': a['t'], 'box': t['box'], 'tok': tok})
                        c['n'] += 1
        for nome in self.ctx.get('nomes_proprios', []):
            nn = ocr_norm(nome)
            if len(nn) < 4:
                continue
            for n, c in contagem.items():
                if c['n'] >= 2 and nn not in n and n not in nn and ratio(n, nn) >= 0.75 and not formavel(n, ref):
                    self.add('erro', 'legendas', f'"{c["tok"]}" na tela parece ser "{nome}" escrito de outro jeito.', tempo=c['t'], boxes=[c['box']],
                             visual=True, sugestao=f'Corrigir para "{nome}".')
        # palavras que não batem com o texto aprovado (prováveis erros de digitação)
        if exp_txt or self.ctx.get('textos_aprovados'):
            suspeitas = 0
            for n, c in sorted(contagem.items(), key=lambda kv: -kv[1]['n']):
                if c['n'] < 2 or n in ref or formavel(n, ref) or any(f'"{c["tok"]}"' in x['mensagem'] for x in self.achados):
                    continue
                parecida = max(ref, key=lambda r: ratio(n, r)) if ref else ''
                if parecida and 0.75 <= ratio(n, parecida) < 1 and suspeitas < 6:
                    suspeitas += 1
                    self.add('alerta', 'legendas', f'"{c["tok"]}" na tela difere do texto aprovado (seria "{parecida.lower()}"?).', tempo=c['t'],
                             boxes=[c['box']], visual=True, sugestao='Confirmar a grafia. Pode ser erro de leitura do OCR (acentos são ignorados).')
        # velocidade de leitura: só caixas que parecem legenda (casam com a fala)
        ref_fala = set(ocr_norm(w) for w in re.split(r'\s+', (exp_txt or '') + ' ' + ' '.join(p['p'] for p in self.palavras)) if ocr_norm(w))
        H_ = self.meta['altura']
        cand = [((t['box'][1] + t['box'][3]) / 2) for a in self.amostras for t in a['textos']
                if not t.get('cenario') and (t['box'][3] - t['box'][1]) < 0.08 * H_ and parece_legenda(t['texto'], ref_fala)]
        faixa = sorted(cand)[len(cand) // 2] if cand else None
        mud, ant = [], None
        for a in self.amostras:
            if faixa is None:
                break
            leg = [t for t in a['textos'] if not t.get('cenario') and abs((t['box'][1] + t['box'][3]) / 2 - faixa) < 0.05 * H_
                   and (t['box'][3] - t['box'][1]) < 0.08 * H_ and parece_legenda(t['texto'], ref_fala)]
            s_ = ' '.join(t['texto'] for t in leg)
            if s_ and ocr_norm(s_) != ant:
                mud.append((a['t'], s_)); ant = ocr_norm(s_)
        for (t0, s0), (t1, s1) in zip(mud, mud[1:]):
            dur = t1 - t0
            if dur > 0 and len(s0) / dur > 25 and len(s0) > 18:
                self.add('alerta', 'legendas', f'Legenda "{s0}" fica só {dur:.2f}s na tela ({len(s0) / dur:.0f} caracteres/s): rápida demais para ler.',
                         tempo=t0, sugestao='Grupos menores ou mais tempo na tela (até 17 caracteres/s).')
                break

    def checar_emendas(self):
        """com o config do editor: a primeira e a última palavra de cada trecho precisam aparecer na fala perto da emenda"""
        if not self.cfg or not self.palavras:
            return
        trs = self.cfg['trechos']
        t, bounds = 0.0, []
        for tr in trs:
            bounds.append((t, t + tr['ate'] - tr['de'], tr['texto'])); t += tr['ate'] - tr['de']
        fala = [(ocr_norm(p['p']), p['t'], p['fim']) for p in self.palavras]

        def ouvida(w, t0, t1):
            wn = ocr_norm(w)
            return any(t0 <= pt <= t1 and (ratio(wn, n) >= 0.7 or (len(wn) >= 4 and len(n) >= 4 and (wn in n or n in wn))) for n, pt, _ in fala)
        import numpy as np, soundfile as sf
        au, sr = sf.read(str(self.saida / 'audio16k.wav'), dtype='float32')

        def db(t0, t1):
            seg = au[max(0, int(t0 * sr)):max(0, int(t1 * sr))]
            return 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9) if len(seg) else -99
        for k, (a, b, txt) in enumerate(bounds):
            ws = [w for w in txt.split() if len(ocr_norm(w)) >= 5]
            if not ws:
                continue
            # sinal de palavra cortada: a palavra da emenda não aparece na transcrição E já há fala nos 30 ms colados ao corte
            if k > 0 and db(a + 0.005, a + 0.035) > -26 and not ouvida(ws[0], a - 0.5, a + 1.5):
                self.add('alerta', 'cortes', f'No corte em {a:.2f}s, a palavra "{ws[0]}" (início do trecho) não foi ouvida inteira: pode ter sido cortada.',
                         tempo=a, sugestao='Começar o trecho 0,05 a 0,1 s antes da palavra (na pausa anterior).', visual=False)
            if k < len(bounds) - 1 and db(b - 0.035, b - 0.005) > -26 and not ouvida(ws[-1], b - 1.5, b + 0.5):
                self.add('alerta', 'cortes', f'No corte em {b:.2f}s, a palavra "{ws[-1]}" (fim do trecho) não foi ouvida inteira: pode ter sido cortada.',
                         tempo=b, sugestao='Terminar o trecho depois da palavra (na pausa seguinte).', visual=False)

    def marcar_cenario(self):
        """texto que é do cenário (camiseta, placa): aparece em muitas amostras, sempre no mesmo lugar, e não é texto aprovado"""
        aprov = set(ocr_norm(x) for x in self.ctx.get('textos_aprovados', []))
        grupos = {}
        for a in self.amostras:
            for t in a['textos']:
                n = ocr_norm(t['texto'])
                if len(n) < 3:
                    continue
                grupos.setdefault(n, []).append(t)
        total = max(1, len(self.amostras))
        for n, ts in grupos.items():
            if any(n in x or x in n for x in aprov if len(x) >= 3):
                continue
            tempos = [a['t'] for a in self.amostras for t in a['textos'] if t in ts]
            if len(ts) >= max(8, 0.2 * total) and tempos and (max(tempos) - min(tempos)) >= 0.6 * self.meta['duracao']:
                for t in ts:
                    t['cenario'] = True
        # fragmentos de texto do cenário lidos parcialmente
        cen = [n for n, ts in grupos.items() if ts and ts[0].get('cenario')]
        for n, ts in grupos.items():
            if not ts[0].get('cenario') and any(ratio(n, c) > 0.6 or (len(n) >= 3 and n in c) for c in cen):
                for t in ts:
                    t['cenario'] = True

    # ---------- conteúdo: números e datas não confirmados ----------
    def checar_conteudo(self):
        fala = ' '.join(p['p'] for p in self.palavras) + ' ' + (self.ctx.get('fala_esperada') or '')
        fontes = fala + ' ' + ' '.join(self.ctx.get('fatos', [])) + ' ' + ' '.join(self.ctx.get('textos_aprovados', []))
        nums_ok = set(re.findall(r'\d+', fontes))
        meses = {'janeiro': '01', 'fevereiro': '02', 'marco': '03', 'abril': '04', 'maio': '05', 'junho': '06', 'julho': '07',
                 'agosto': '08', 'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'}
        fn = norm(fontes).lower()
        for mes, num in meses.items():
            if mes in fn:
                nums_ok.add(num); nums_ok.add(str(int(num)))
        vistos = set()
        for a in self.amostras:
            for t in a['textos']:
                if t.get('cenario'):
                    continue
                for nnum in re.findall(r'\d+', t['texto']):
                    tok = next((x for x in t['texto'].split() if nnum in x), nnum)
                    if len(nnum) < 2 and sum(ch.isdigit() for ch in tok) < 0.6 * len(norm(tok) or 'x'):
                        continue  # "0UTUBR0": O lido como zero
                    if nnum not in nums_ok and nnum.lstrip('0') not in nums_ok and nnum not in vistos:
                        vistos.add(nnum)
                        self.add('alerta', 'conteudo', f'Número "{nnum}" na tela (em "{t["texto"]}") não aparece na fala nem no briefing.',
                                 tempo=a['t'], boxes=[t['box']], visual=True, sugestao='Confirmar a informação com a pessoa.')

    # ---------- marca: CTA, logo, cores ----------
    def checar_marca(self):
        import numpy as np, cv2
        dur = self.meta['duracao']
        finais = [a for a in self.amostras if a['t'] > dur - 5]
        texto_final = norm(' '.join(t['texto'] for a in finais for t in a['textos']))
        cta = self.ctx.get('cta')
        if cta:
            if not any(norm(c) and norm(c) in texto_final for c in cta):
                self.add('alerta', 'marca', f'Chamada para ação esperada ({", ".join(cta)}) não encontrada nos últimos 5 s.', tempo=dur - 3)
        elif self.ctx.get('exigir_cta', True) and dur > 8:
            if not re.search(r'LINK|BIO|INSCREV|GARANT|COMPR|SAIBA|CHAM|ACESS|RESERV|AGEND|SIGA|CLIQUE|WHATSAPP|DM', texto_final):
                self.add('alerta', 'marca', 'Não encontrei chamada para ação no final do vídeo.', tempo=dur - 3,
                         sugestao='Fechar com uma ação clara (inscrever, comprar, seguir, link na bio).')
        logo = self.ctx.get('logo')
        if logo and Path(logo).exists():
            lg = cv2.imread(logo, cv2.IMREAD_UNCHANGED)
            if lg is not None:
                if lg.shape[2] == 4:
                    a = lg[..., 3:4] / 255.0
                    lg = (lg[..., :3] * a + 255 * (1 - a)).astype(np.uint8)
                g_logo = cv2.cvtColor(lg, cv2.COLOR_BGR2GRAY)
                cap = cv2.VideoCapture(self.video); fps = cap.get(5) or 30
                cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, int((dur - 1.0) * fps)))
                ok, f = cap.read()
                melhor = 0
                if ok:
                    g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
                    for frac in np.linspace(0.15, 0.7, 12):
                        w = int(g.shape[1] * frac); h = int(g_logo.shape[0] * w / g_logo.shape[1])
                        if h >= g.shape[0] or w < 20:
                            continue
                        t = cv2.resize(g_logo, (w, h), interpolation=cv2.INTER_AREA)
                        r = cv2.matchTemplate(g, t, cv2.TM_CCOEFF_NORMED)
                        melhor = max(melhor, float(r.max()))
                if melhor < 0.55:
                    self.add('alerta', 'marca', f'Logo não encontrado no último segundo (semelhança {melhor:.2f}).', tempo=dur - 1, visual=True,
                             sugestao='Incluir o logo na tela final.')
        elif self.ctx.get('exigir_logo'):
            self.add('alerta', 'marca', 'O briefing pede logo, mas o arquivo do logo não foi informado para conferir.')
        # cores do texto fora da paleta
        cores = [tuple(int(c.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)) for c in self.ctx.get('cores', [])]
        if cores:
            pal = np.array(cores + [(255, 255, 255), (0, 0, 0), (20, 20, 22)], np.float32)
            fora = {}
            for a in self.amostras[::2]:
                if a['_rgb'] is None:
                    continue
                for t in a['textos']:
                    c = cor_do_texto(a['_rgb'], t['box'])
                    if c is None:
                        continue
                    dmin = float(np.linalg.norm(pal - c, axis=1).min())
                    sat = c.max() - c.min()
                    if dmin > 70 and sat > 60:
                        k = tuple((c // 40).astype(int))
                        fora.setdefault(k, (a['t'], t, c))
            for k, (t, tx, c) in list(fora.items())[:3]:
                self.add('alerta', 'marca', f'Texto "{tx["texto"]}" em cor fora da paleta (RGB {int(c[0])},{int(c[1])},{int(c[2])}).',
                         tempo=t, boxes=[tx['box']], visual=True, sugestao='Usar uma cor da paleta da marca.')

    # ---------- saída ----------
    def salvar(self):
        for a in self.achados:
            a.pop('_chave', None)
        dados = {'video': self.video, 'plataforma': self.plat, 'meta': self.meta, 'som': getattr(self, 'som', None),
                 'legendas': getattr(self, 'legenda_stats', None), 'cortes': self.cortes,
                 'transcricao': self.frases, 'achados': self.achados,
                 'amostras_texto': [{'t': round(a['t'], 2), 'textos': [t['texto'] for t in a['textos']], 'rostos': len(a['rostos'])} for a in self.amostras]}
        p = self.saida / 'revisao.json'
        json.dump(dados, open(p, 'w'), ensure_ascii=False, indent=1)
        miniaturas(dados, self.saida)
        relatorio(str(p))


def miniaturas(dados, saida):
    import numpy as np, cv2
    cap = cv2.VideoCapture(dados['video']); fps = cap.get(5) or 30
    thumbs = []
    for a in dados['achados']:
        if a['tempo'] is None:
            continue
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(a['tempo'] * fps))
        ok, f = cap.read()
        if not ok:
            continue
        for i, b in enumerate(a['boxes']):
            cv2.rectangle(f, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (0, 0, 255) if i == 0 else (255, 200, 0), max(2, f.shape[1] // 200))
        th = cv2.resize(f, (270, int(270 * f.shape[0] / f.shape[1])))
        cv2.putText(th, f'#{a["id"]} {a["tempo"]:.1f}s', (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        nome = f'quadros/achado_{a["id"]:02d}.jpg'
        cv2.imwrite(str(Path(saida) / nome), th, [cv2.IMWRITE_JPEG_QUALITY, 82])
        a['quadro'] = nome
        if a.get('precisa_olhar'):
            thumbs.append(th)
    if thumbs:
        cols = 5
        while len(thumbs) % cols:
            thumbs.append(np.zeros_like(thumbs[0]))
        hmax = max(t.shape[0] for t in thumbs)
        thumbs = [cv2.copyMakeBorder(t, 0, hmax - t.shape[0], 0, 0, cv2.BORDER_CONSTANT) for t in thumbs]
        rows = [np.hstack(thumbs[i:i + cols]) for i in range(0, len(thumbs), cols)]
        cv2.imwrite(str(Path(saida) / 'candidatos.jpg'), np.vstack(rows))
    json.dump(dados, open(Path(saida) / 'revisao.json', 'w'), ensure_ascii=False, indent=1)


def nota(achados):
    validos = [a for a in achados if a.get('confirmado') is not False]
    n = 100 - sum(PESO[a['gravidade']] for a in validos)
    erros = sum(1 for a in validos if a['gravidade'] == 'erro')
    n = max(0, n)
    if erros == 0 and n >= 85:
        v = 'aprovado'
    elif erros <= 2 and n >= 60:
        v = 'ajustes'
    else:
        v = 'reprovado'
    return n, v, validos


def relatorio(caminho_json):
    p = Path(caminho_json); d = json.load(open(p))
    n, v, validos = nota(d['achados'])
    d['nota'], d['veredito'] = n, v
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=1)
    cor_v = {'aprovado': '#1f7a3f', 'ajustes': '#b26a00', 'reprovado': '#b3261e'}[v]
    nome_v = {'aprovado': 'Aprovado', 'ajustes': 'Precisa de ajustes', 'reprovado': 'Reprovado'}[v]
    linhas = []
    ordem = {'erro': 0, 'alerta': 1, 'info': 2}
    for a in sorted(validos, key=lambda x: (ordem[x['gravidade']], x['tempo'] if x['tempo'] is not None else -1)):
        img = ''
        if a.get('quadro') and (p.parent / a['quadro']).exists():
            b64 = base64.b64encode(open(p.parent / a['quadro'], 'rb').read()).decode()
            img = f'<img src="data:image/jpeg;base64,{b64}" alt="quadro do achado {a["id"]}">'
        t = f'{a["tempo"]:.1f}s' if a['tempo'] is not None else 'vídeo todo'
        sug = f'<p class="sug">{esc(a["sugestao"])}</p>' if a.get('sugestao') else ''
        linhas.append(f'<article class="ach {a["gravidade"]}"><div class="tx"><span class="tag">{a["gravidade"]}</span>'
                      f'<span class="cat">{esc(a["categoria"])} · {t}</span><p>{esc(a["mensagem"])}</p>{sug}</div>{img}</article>')
    falsos = [a for a in d['achados'] if a.get('confirmado') is False]
    m = d['meta']; s = d.get('som') or {}; lg = d.get('legendas') or {}
    resumo = (f'{m["largura"]}×{m["altura"]} · {m["fps"]:.0f} fps · {m["duracao"]:.1f}s · {d["plataforma"]}'
              + (f' · {s["lufs"]:.1f} LUFS' if s.get('lufs') is not None else '')
              + (f' · legenda cobre {lg["cobertura"]:.0%} da fala' if lg.get('cobertura') is not None else ''))
    html = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Revisão de vídeo</title><style>
:root{{--bg:#f6f5f2;--card:#fff;--ink:#17171a;--mut:#6b6b73;--line:#e4e2dc}}
@media (prefers-color-scheme:dark){{:root{{--bg:#151517;--card:#1e1e21;--ink:#f1f0ec;--mut:#a3a3ab;--line:#2c2c31}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
main{{max-width:860px;margin:0 auto;padding:28px 16px 60px}}
h1{{font-size:22px;margin:0 0 4px}} .meta{{color:var(--mut);font-size:13px}}
.v{{display:flex;gap:16px;align-items:center;margin:20px 0;padding:18px;border-radius:14px;background:var(--card);border:1px solid var(--line)}}
.n{{font-size:44px;font-weight:800;color:{cor_v};line-height:1}} .vv{{font-weight:700;color:{cor_v};font-size:18px}}
.ach{{display:flex;gap:14px;justify-content:space-between;background:var(--card);border:1px solid var(--line);border-left:5px solid #999;border-radius:12px;padding:14px;margin:10px 0}}
.ach.erro{{border-left-color:#d93025}} .ach.alerta{{border-left-color:#e8a100}} .ach img{{width:120px;height:auto;border-radius:8px;flex:none}}
.tag{{text-transform:uppercase;font-size:11px;font-weight:800;letter-spacing:.08em;margin-right:8px}} .erro .tag{{color:#d93025}} .alerta .tag{{color:#b26a00}}
.cat{{color:var(--mut);font-size:13px}} .ach p{{margin:6px 0 0}} .sug{{color:var(--mut);font-size:14px}}
footer{{margin-top:30px;color:var(--mut);font-size:12px}}
@media (max-width:520px){{.ach{{flex-direction:column}} .ach img{{width:100%}}}}
</style></head><body><main>
<h1>Revisão de vídeo</h1><div class="meta">{esc(Path(d["video"]).name)} · {resumo}</div>
<div class="v"><div class="n">{n}</div><div><div class="vv">{nome_v}</div><div class="meta">{sum(1 for a in validos if a["gravidade"]=="erro")} erro(s) · {sum(1 for a in validos if a["gravidade"]=="alerta")} alerta(s){f" · {len(falsos)} descartado(s) na conferência visual" if falsos else ""}</div></div></div>
{"".join(linhas) or "<p>Nenhum problema encontrado.</p>"}
<footer>Revisado com a skill Revisor de vídeo sênior, da Trentin Solutions · trentinsolutions.com.br</footer>
</main></body></html>'''
    open(p.parent / 'revisao.html', 'w').write(html)
    print(f'nota {n} · {v} · {len(validos)} achado(s)')
    for a in validos:
        t = f'{a["tempo"]:6.2f}s' if a['tempo'] is not None else '   todo'
        print(f'  #{a["id"]:02d} [{a["gravidade"]:6}] {t} {a["categoria"]}: {a["mensagem"]}{"  (olhar)" if a.get("precisa_olhar") and a.get("confirmado") is None else ""}')
    print(p.parent / 'revisao.html')


def esc(s):
    return (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == 'preparar':
        preparar()
    elif cmd == 'revisar':
        video = args[0]
        opt = {k: v for k, v in zip(args[1::2], args[2::2])}
        Revisao(video, opt.get('--briefing'), opt.get('--config'), opt.get('--plataforma'), opt.get('--saida')).rodar(
            fps_ocr=float(opt.get('--fps-ocr', 4)))
    elif cmd == 'relatorio':
        relatorio(args[0])
    else:
        print(__doc__); sys.exit(1)


if __name__ == '__main__':
    main()
