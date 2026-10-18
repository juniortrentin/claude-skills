#!/usr/bin/env python3
"""
editor-video-senior · motor de edição
Skill gratuita da Trentin Solutions · trentinsolutions.com.br · CC BY 4.0

Comandos:
  preparar                         instala dependências, baixa modelos e fontes
  analisar  VIDEO [--sem-profundidade]   áudio, silêncios, transcrição e recorte da pessoa -> trabalho/
  referencia VIDEO                 ritmo de cortes e folha de contato de um vídeo de referência
  previa    CONFIG T1 T2 ...       quadros de prévia em uma folha (trabalho/previa.jpg)
  render    CONFIG                 vídeo final (vídeo + áudio) no caminho "saida" do config
  folha     VIDEO [SAIDA.jpg]      folha de contato para revisão
"""
import json, math, os, subprocess, sys, shutil
from pathlib import Path

CACHE = Path(os.environ.get('EDITOR_VIDEO_CACHE', Path.home() / '.cache' / 'editor-video-senior'))
WHISPER_URL = 'https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.tar.bz2'
U2NET_URL = 'https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net_human_seg.onnx'
TRAB = Path('trabalho')


def sh(cmd, **kw):
    return subprocess.run(cmd, shell=isinstance(cmd, str), check=True, **kw)


# ======================================================================
# preparar
# ======================================================================
def preparar(fontes=('anton', 'montserrat')):
    pkgs = ['numpy', 'opencv-python-headless', 'pillow', 'soundfile', 'scipy', 'onnxruntime', 'sherpa-onnx']
    missing = []
    for p in pkgs:
        mod = {'opencv-python-headless': 'cv2', 'pillow': 'PIL', 'sherpa-onnx': 'sherpa_onnx'}.get(p, p)
        try:
            __import__(mod)
        except ImportError:
            missing.append(p)
    if missing:
        sh([sys.executable, '-m', 'pip', 'install', '-q', '--break-system-packages', *missing])
    if not shutil.which('ffmpeg'):
        print('AVISO: ffmpeg não encontrado. Instale (apt-get install -y ffmpeg).')
    CACHE.mkdir(parents=True, exist_ok=True)
    wd = CACHE / 'sherpa-onnx-whisper-small'
    if not (wd / 'small-encoder.onnx').exists():
        print('baixando modelo de transcrição (~640 MB)...', flush=True)
        sh(['curl', '-sSL', '-o', str(CACHE / 'w.tar.bz2'), WHISPER_URL])
        sh(['tar', 'xjf', str(CACHE / 'w.tar.bz2'), '-C', str(CACHE)])
        (CACHE / 'w.tar.bz2').unlink()
    if not (CACHE / 'u2net_human_seg.onnx').exists():
        print('baixando modelo de recorte (~170 MB)...', flush=True)
        sh(['curl', '-sSL', '-o', str(CACHE / 'u2net_human_seg.onnx'), U2NET_URL])
    for f in fontes:
        baixar_fonte(f)
    print('pronto')


def baixar_fonte(nome):
    nome = nome.lower().replace(' ', '-')
    d = CACHE / 'fontes' / nome
    if d.exists() and any(d.glob('*.woff')):
        return d
    d.mkdir(parents=True, exist_ok=True)
    tmp = CACHE / 'fontes' / '_tmp'
    tmp.mkdir(parents=True, exist_ok=True)
    out = subprocess.run(['npm', 'pack', '-s', f'@fontsource/{nome}'], cwd=tmp, capture_output=True, text=True)
    tgz = out.stdout.strip().splitlines()[-1] if out.stdout.strip() else ''
    if not tgz:
        raise SystemExit(f'fonte "{nome}" não encontrada no @fontsource')
    sh(['tar', 'xzf', str(tmp / tgz), '-C', str(tmp)])
    for f in (tmp / 'package' / 'files').glob(f'{nome}-latin-*-normal.woff'):
        shutil.copy(f, d / f.name)
    shutil.rmtree(tmp)
    return d


def caminho_fonte(nome, peso):
    d = baixar_fonte(nome)
    nome = nome.lower().replace(' ', '-')
    p = d / f'{nome}-latin-{peso}-normal.woff'
    if p.exists():
        return str(p)
    pesos = sorted(int(x.name.split('-')[-2]) for x in d.glob('*.woff'))
    perto = min(pesos, key=lambda w: abs(w - peso))
    return str(d / f'{nome}-latin-{perto}-normal.woff')


# ======================================================================
# analisar
# ======================================================================
def silencios(wav, db, dur):
    r = subprocess.run(['ffmpeg', '-i', wav, '-af', f'silencedetect=n={db}dB:d={dur}', '-f', 'null', '-'],
                       capture_output=True, text=True)
    out, cur = [], None
    for ln in r.stderr.splitlines():
        if 'silence_start:' in ln:
            cur = float(ln.split('silence_start:')[1].split()[0])
        elif 'silence_end:' in ln and cur is not None:
            out.append([max(0.0, cur), float(ln.split('silence_end:')[1].split()[0])])
            cur = None
    return out


def complemento(sil, total, pad=0.0):
    fala, cur = [], 0.0
    for s, e in sil:
        if s > cur:
            fala.append([max(0, cur - pad), min(total, s + pad)])
        cur = max(cur, e)
    if cur < total - 0.05:
        fala.append([max(0, cur - pad), total])
    return [f for f in fala if f[1] - f[0] > 0.12]


def duracao(video):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', video],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def analisar(video, profundidade=True, idioma='pt'):
    import numpy as np, soundfile as sf
    TRAB.mkdir(exist_ok=True)
    wav = str(TRAB / 'audio16k.wav')
    sh(['ffmpeg', '-y', '-v', 'error', '-i', video, '-ac', '1', '-ar', '16000', wav])
    total = duracao(video)
    sil_frases = silencios(wav, -35, 0.3)
    sil_ilhas = silencios(wav, -30, 0.12)
    frases = complemento(sil_frases, total, pad=0.05)
    # quebra frases longas no maior silêncio interno
    final = []
    for a, b in frases:
        pend = [[a, b]]
        while pend:
            x, y = pend.pop(0)
            if y - x <= 6:
                final.append([x, y]); continue
            internos = [s for s in sil_ilhas if s[0] > x + 0.8 and s[1] < y - 0.8]
            if not internos:
                final.append([x, y]); continue
            s = max(internos, key=lambda q: q[1] - q[0])
            pend[:0] = [[x, s[0] + 0.03], [s[1] - 0.03, y]]
    import sherpa_onnx
    d = CACHE / 'sherpa-onnx-whisper-small'
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=str(d / 'small-encoder.onnx'), decoder=str(d / 'small-decoder.onnx'),
        tokens=str(d / 'small-tokens.txt'), language=idioma, task='transcribe', num_threads=os.cpu_count() or 2)
    audio, sr = sf.read(wav, dtype='float32')
    out = []
    for a, b in final:
        st = rec.create_stream(); st.accept_waveform(sr, audio[int(a * sr):int(b * sr)]); rec.decode_stream(st)
        out.append({'de': round(a, 2), 'ate': round(b, 2), 'texto': st.result.text.strip()})
        print(f'[{a:6.2f}-{b:6.2f}] {st.result.text.strip()}', flush=True)
    meta = video_meta(video)
    json.dump({'video': video, 'duracao': total, **meta, 'frases': out, 'silencios': sil_ilhas},
              open(TRAB / 'analise.json', 'w'), ensure_ascii=False, indent=1)
    if profundidade:
        recortar_pessoa(video)
    print('analise salva em trabalho/analise.json')


def video_meta(video):
    import cv2
    c = cv2.VideoCapture(video)
    return {'largura': int(c.get(3)), 'altura': int(c.get(4)), 'fps': c.get(5) or 30, 'quadros': int(c.get(7))}


def recortar_pessoa(video):
    import numpy as np, cv2, onnxruntime as ort
    s = ort.InferenceSession(str(CACHE / 'u2net_human_seg.onnx'), providers=['CPUExecutionProvider'])
    inp = s.get_inputs()[0].name
    cap = cv2.VideoCapture(video)
    mean = np.array([0.485, 0.456, 0.406]); std = np.array([0.229, 0.224, 0.225])
    masks = []; n = 0
    while True:
        ok, f = cap.read()
        if not ok:
            break
        h, w = f.shape[:2]
        mw = min(w, 720); mh = int(round(h * mw / w))
        x = cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2RGB), (320, 320)).astype(np.float32) / 255
        x = ((x - mean) / std).transpose(2, 0, 1)[None].astype(np.float32)
        o = s.run(None, {inp: x})[0][0, 0]
        o = (o - o.min()) / (o.max() - o.min() + 1e-8)
        masks.append(cv2.resize((o * 255).astype(np.uint8), (mw, mh), interpolation=cv2.INTER_LINEAR))
        n += 1
        if n % 60 == 0:
            print('recorte', n, flush=True)
    np.save(TRAB / 'mascaras.npy', np.stack(masks))


# ======================================================================
# referencia
# ======================================================================
def referencia(video):
    TRAB.mkdir(exist_ok=True)
    # limiar baixo: jump cuts no mesmo cenário mudam pouco a imagem; cortes a menos de 0,3 s viram um só
    r = subprocess.run(['ffmpeg', '-i', video, '-vf', "select='gt(scene,0.08)',showinfo", '-f', 'null', '-'],
                       capture_output=True, text=True)
    brutos = [float(l.split('pts_time:')[1].split()[0]) for l in r.stderr.splitlines() if 'pts_time:' in l]
    cortes = []
    for c in brutos:
        if not cortes or c - cortes[-1] > 0.3:
            cortes.append(c)
    total = duracao(video)
    planos = len(cortes) + 1
    folha(video, str(TRAB / 'referencia_folha.jpg'), fps=2, cols=8)
    res = {'duracao': round(total, 2), 'cortes': [round(c, 2) for c in cortes], 'planos': planos,
           'duracao_media_plano': round(total / planos, 2)}
    json.dump(res, open(TRAB / 'referencia.json', 'w'), indent=1)
    print(json.dumps(res, ensure_ascii=False))
    print('folha em trabalho/referencia_folha.jpg')


def folha(video, saida=None, fps=1.5, cols=7):
    saida = saida or str(TRAB / 'folha.jpg')
    Path(saida).parent.mkdir(parents=True, exist_ok=True)
    total = duracao(video)
    n = max(1, int(total * fps))
    rows = math.ceil(n / cols)
    sh(['ffmpeg', '-v', 'error', '-y', '-i', video, '-vf', f'fps={fps},scale=216:-2,tile={cols}x{rows}',
        '-frames:v', '1', saida])
    print(saida)


# ======================================================================
# motor de render
# ======================================================================
def hexrgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def bez(p1x, p1y, p2x, p2y):
    def f(x):
        x = min(max(x, 0.0), 1.0); t = x
        for _ in range(8):
            cx = 3 * p1x * t * (1 - t) ** 2 + 3 * p2x * t * t * (1 - t) + t ** 3 - x
            d = 3 * p1x * (1 - t) ** 2 + 6 * (p2x - p1x) * t * (1 - t) + 3 * (1 - p2x) * t * t
            if abs(d) < 1e-6:
                break
            t = min(max(t - cx / d, 0), 1)
        return 3 * p1y * t * (1 - t) ** 2 + 3 * p2y * t * t * (1 - t) + t ** 3
    return f


class Motor:
    def __init__(self, cfg_path):
        import numpy as np, cv2
        from PIL import ImageFont
        self.np, self.cv2, self.ImageFont = np, cv2, ImageFont
        self.cfg_path = Path(cfg_path)
        c = json.load(open(cfg_path))
        self.c = c
        base = self.cfg_path.parent
        self.video = str((base / c['video']).resolve()) if not os.path.isabs(c['video']) else c['video']
        fmt = c.get('formato', {})
        self.W, self.H, self.FPS = fmt.get('largura', 1080), fmt.get('altura', 1920), fmt.get('fps', 30)
        self.sx, self.sy = self.W / 1080, self.H / 1920
        self.su = min(self.sx, self.sy)
        m = c['marca']
        self.cores = {k: hexrgb(v) for k, v in m['cores'].items()}
        self.cores.setdefault('branco', (255, 255, 255))
        mv = m.get('movimento', {})
        self.EASE = bez(*mv.get('curva', [.16, 1, .3, 1]))
        self.FAST = bez(.2, .8, .2, 1)
        self.DIN = mv.get('duracao', 0.52)
        ft, fx = m['fontes']['titulo'], m['fontes']['texto']
        self.f_titulo = caminho_fonte(ft['nome'], ft.get('peso', 400))
        self.f_texto = {w: caminho_fonte(fx['nome'], w) for w in (500, 600, 800)}
        self._fc = {}
        self.logo = None
        if m.get('logo'):
            lp = Path(m['logo']); lp = lp if lp.is_absolute() else base / lp
            if lp.exists():
                self.logo = str(lp)
        self._timeline()
        self._words()
        self._sprites()

    # ---------------- helpers ----------------
    def cor(self, k):
        if isinstance(k, (list, tuple)):
            return tuple(k)
        if isinstance(k, str) and k.startswith('#'):
            return hexrgb(k)
        return self.cores[k]

    def fonte(self, qual, peso=800):
        return self.f_titulo if qual == 'titulo' else self.f_texto.get(peso, self.f_texto[800])

    def font(self, path, size):
        k = (path, size)
        if k not in self._fc:
            self._fc[k] = self.ImageFont.truetype(path, size)
        return self._fc[k]

    def prog(self, t, start, dur, ease=None):
        ease = ease or self.EASE
        return ease((t - start) / dur) if t > start else 0.0

    def text_sprite(self, text, path, size, fill, tracking=0.0):
        from PIL import Image, ImageDraw
        np = self.np
        size = max(8, int(round(size)))
        f = self.font(path, size)
        asc, desc = f.getmetrics()
        widths = [f.getlength(ch) for ch in text]
        tw = int(sum(widths) + tracking * size * (len(text) - 1)) + 8
        im = Image.new('RGBA', (max(tw, 8), asc + desc + 8), (0, 0, 0, 0))
        d = ImageDraw.Draw(im); x = 4
        for ch, w in zip(text, widths):
            d.text((x, 4), ch, font=f, fill=tuple(fill) + (255,))
            x += w + tracking * size
        a = np.array(im)
        ys, xs = np.where(a[..., 3] > 0)
        if len(ys) == 0:
            return np.zeros((1, 1, 4), np.uint8)
        return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

    def pill(self, text, path, size, fg, bg, padx=34, pady=22, radius=None, tracking=0.0, bg_alpha=255):
        from PIL import Image, ImageDraw
        s = self.text_sprite(text, path, size, fg, tracking)
        h, w = s.shape[:2]
        padx, pady = int(round(padx)), int(round(pady))
        W2, H2 = w + 2 * padx, h + 2 * pady
        im = Image.new('RGBA', (W2, H2), (0, 0, 0, 0))
        ImageDraw.Draw(im).rounded_rectangle((0, 0, W2 - 1, H2 - 1), radius=radius if radius is not None else H2 // 2,
                                             fill=tuple(bg) + (bg_alpha,))
        a = self.np.array(im); self.blend(a, s, padx, pady)
        return a

    def blend(self, dst, src, x, y, op=1.0):
        np = self.np
        x, y = int(round(x)), int(round(y))
        h, w = src.shape[:2]
        x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, dst.shape[1]), min(y + h, dst.shape[0])
        if x1 <= x0 or y1 <= y0 or op <= 0:
            return
        s = src[y0 - y:y1 - y, x0 - x:x1 - x].astype(np.float32)
        a = (s[..., 3:4] / 255.0) * op
        d = dst[y0:y1, x0:x1]
        if dst.shape[2] == 4:
            da = d[..., 3:4].astype(np.float32) / 255
            oa = a + da * (1 - a)
            rgb = (s[..., :3] * a + d[..., :3].astype(np.float32) * da * (1 - a)) / np.maximum(oa, 1e-6)
            d[..., :3] = rgb.astype(dst.dtype); d[..., 3:4] = (oa * 255).astype(dst.dtype)
        else:
            d[:] = (s[..., :3] * a + d.astype(np.float32) * (1 - a)).astype(dst.dtype)

    def place(self, dst, spr, cx, cy, op=1.0, scale=1.0, anchor='c'):
        if op <= 0.003:
            return
        if abs(scale - 1) > 1e-3:
            spr = self.cv2.resize(spr, None, fx=scale, fy=scale,
                                  interpolation=self.cv2.INTER_LINEAR if scale > 1 else self.cv2.INTER_AREA)
        h, w = spr.shape[:2]
        x = cx - w / 2 if anchor in ('c', 't', 'b') else (cx if anchor in ('l', 'tl', 'bl') else cx - w)
        y = cy - h / 2 if anchor in ('c', 'l', 'r') else (cy if anchor in ('t', 'tl', 'tr') else cy - h)
        self.blend(dst, spr, x, y, op)

    def enter_exit(self, t, t0, t1, din=None, dout=0.22):
        din = din or self.DIN
        if t < t0 or t > t1:
            return 0.0, 0.0
        p = self.prog(t, t0, din)
        o = min(1.0, (t - t0) / (din * 0.6))
        if t > t1 - dout:
            o *= max(0.0, (t1 - t) / dout)
        return o, p

    # ---------------- timeline ----------------
    def _timeline(self):
        tr = self.c['trechos']
        self.SEGS = [(x['de'], x['ate']) for x in tr]
        self.T0 = []; acc = 0
        for a, b in self.SEGS:
            self.T0.append(acc); acc += b - a
        self.T_END = acc
        tf = self.c.get('tela_final')
        self.CARD = tf.get('duracao', 3.6) if tf else 0.0
        self.TOTAL = self.T_END + self.CARD
        self.NF = int(round(self.TOTAL * self.FPS))
        self.SIL = self.c.get('silencios')
        if self.SIL is None:
            an = self.cfg_path.parent / 'trabalho' / 'analise.json'
            self.SIL = json.load(open(an))['silencios'] if an.exists() else []

    def seg_at(self, t):
        for k in range(len(self.SEGS)):
            if t < self.T0[k] + self.SEGS[k][1] - self.SEGS[k][0]:
                return k
        return len(self.SEGS) - 1

    def out_time(self, src_t):
        for k, (a, b) in enumerate(self.SEGS):
            if a <= src_t <= b:
                return self.T0[k] + src_t - a
        return None

    def islands(self, a, b):
        out = []; cur = a
        for s, e in self.SIL:
            if e <= a or s >= b:
                continue
            if s > cur:
                out.append((cur, min(s, b)))
            cur = max(cur, e)
        if cur < b:
            out.append((cur, b))
        return out or [(a, b)]

    def _words(self):
        np = self.np
        leg = self.c.get('legendas', {})
        dest = [d.lower().split() for d in leg.get('destaques', [])]
        clean = lambda w: w.lower().strip(',.?!;:"\'')
        self.WORDS, self.SEGIDX = [], []
        for k, ((a, b), trc) in enumerate(zip(self.SEGS, self.c['trechos'])):
            isl = self.islands(a, b); words = trc['texto'].split()
            if not words:
                continue
            wts = np.array([len(w) + 1.5 for w in words], float); tot = sum(e - s for s, e in isl)
            cum = np.concatenate([[0], np.cumsum(wts)]) / wts.sum() * tot

            def src_at(dd):
                for s, e in isl:
                    if dd <= e - s:
                        return s + dd
                    dd -= e - s
                return isl[-1][1]
            keys = [False] * len(words)
            cw = [clean(w) for w in words]
            for ph in dest:
                for i in range(len(cw) - len(ph) + 1):
                    if cw[i:i + len(ph)] == [clean(p) for p in ph]:
                        for j in range(i, i + len(ph)):
                            keys[j] = True
            for i, w in enumerate(words):
                s0, s1 = src_at(cum[i] + 1e-4), src_at(cum[i + 1] - 1e-4)
                self.WORDS.append((self.out_time(s0), self.out_time(s1), w, keys[i]))
                self.SEGIDX.append(k)
        maxc = leg.get('max_caracteres', 13)
        self.GROUPS = []; cur = []
        for n, wd in enumerate(self.WORDS):
            cur.append(wd)
            txt = ' '.join(x[2] for x in cur)
            last = n + 1 == len(self.WORDS) or self.SEGIDX[n + 1] != self.SEGIDX[n]
            if len(txt) >= maxc or wd[2][-1] in ',.?!' or (cur[-1][1] - cur[0][0]) > 1.0 or last:
                self.GROUPS.append(cur); cur = []
        if cur:
            self.GROUPS.append(cur)
        self.GT = []
        for i, g in enumerate(self.GROUPS):
            s = g[0][0]; e = self.GROUPS[i + 1][0][0] if i + 1 < len(self.GROUPS) else g[-1][1] + 0.3
            self.GT.append((s, min(e, g[-1][1] + 0.45)))

    def resolve(self, ref):
        """referência de tempo -> segundos na saída"""
        if ref is None:
            return None
        if isinstance(ref, (int, float)):
            return float(ref)
        aj = ref.get('ajuste', 0.0)
        if 'tempo' in ref:
            return ref['tempo'] + aj
        if 'trecho' in ref:
            return self.T0[ref['trecho']] + aj
        if 'trecho_fim' in ref:
            k = ref['trecho_fim']
            return (self.T0[k + 1] if k + 1 < len(self.T0) else self.T_END) + aj
        if 'fim' in ref:
            return self.T_END + aj
        if 'palavra' in ref:
            alvo = ref['palavra'].lower(); occ = ref.get('ocorrencia', 1)
            after = self.T0[ref['a_partir_do_trecho']] if 'a_partir_do_trecho' in ref else -1
            n = 0
            for s, e, w, k in self.WORDS:
                if s >= after and alvo in w.lower():
                    n += 1
                    if n == occ:
                        return s + aj
            raise SystemExit(f'palavra não encontrada: {ref}')
        raise SystemExit(f'referência de tempo inválida: {ref}')

    # ---------------- sprites ----------------
    def _sprites(self):
        np = self.np
        self.E = []
        for el in self.c.get('elementos', []):
            e = dict(el)
            e['_t0'] = self.resolve(el['de']); e['_t1'] = self.resolve(el['ate'])
            e['_spr'] = self.make_sprite(e)
            self.E.append(e)
        cn = self.c['marca'].get('cantoneiras', True)
        self.cantoneiras = None
        if cn:
            L, th = int(110 * self.su), max(2, int(12 * self.su))
            self.cantoneiras = (self.corner(L, th, self.cor('primaria')), self.corner(L, th, self.cor('primaria'))[::-1, ::-1].copy())
        H, W = self.H, self.W
        yy, xx = np.mgrid[0:H, 0:W]
        self.yy, self.xx = yy, xx
        self.VIG = (1 - 0.38 * np.clip((((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.42) / (H * 0.7)) ** 2), 0, 1))[..., None].astype(np.float32)
        rng = np.random.default_rng(7)
        self.GRAIN = [self.cv2.resize(rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32), (W, H))[..., None] for _ in range(6)]
        self.grain_amt = self.c['marca'].get('granulado', 7)
        if self.c.get('tela_final'):
            self._end_sprites()

    def corner(self, L, th, color):
        a = self.np.zeros((L, L, 4), self.np.uint8)
        a[:th, :, :3] = color; a[:th, :, 3] = 255; a[:, :th, :3] = color; a[:, :th, 3] = 255
        return a

    def make_sprite(self, e):
        su = self.su; tp = e['tipo']
        if tp == 'texto_atras':
            return self.text_sprite(e['texto'], self.f_titulo, e.get('tamanho', 600) * su, self.cor(e.get('cor', 'primaria')), e.get('espacamento', -0.02))
        if tp == 'rotulo':
            return self.text_sprite(e['texto'], self.fonte(e.get('fonte', 'texto'), e.get('peso', 800)), e.get('tamanho', 30) * su,
                                    self.cor(e.get('cor', 'fundo')), e.get('espacamento', 0.16))
        if tp == 'pilula':
            return self.pill(e['texto'], self.fonte(e.get('fonte', 'texto'), e.get('peso', 800)), e.get('tamanho', 40) * su,
                             self.cor(e.get('cor_texto', 'branco')), self.cor(e.get('cor_fundo', 'primaria')),
                             padx=e.get('padx', 34) * su, pady=e.get('pady', 22) * su,
                             radius=None if e.get('raio') is None else int(e['raio'] * su), tracking=e.get('espacamento', 0.0))
        if tp == 'nome':
            return {'rot': self.text_sprite(e.get('rotulo', 'COM'), self.f_texto[800], 30 * su, self.cor(e.get('cor_rotulo', 'primaria')), 0.16),
                    'nome': self.text_sprite(e['texto'], self.f_titulo, e.get('tamanho', 84) * su, self.cor(e.get('cor_texto', 'fundo')), 0.0)}
        if tp == 'icone':
            return self.icon(e.get('icone', 'planilha'), e.get('texto', ''))
        if tp == 'imagem':
            from PIL import Image
            p = Path(e['arquivo']); p = p if p.is_absolute() else self.cfg_path.parent / p
            im = self.np.array(Image.open(p).convert('RGBA'))
            sc = e.get('largura', 400) * su / im.shape[1]
            return self.cv2.resize(im, None, fx=sc, fy=sc, interpolation=self.cv2.INTER_AREA)
        if tp == 'grafico':
            return None
        raise SystemExit(f'tipo de elemento desconhecido: {tp}')

    def icon(self, nome, rotulo=''):
        from PIL import Image, ImageDraw
        su = self.su
        C, P, I, Wt = self.cor('fundo'), self.cor('primaria'), self.cor('tinta'), self.cor('branco')
        w, h = int(300 * su), int(330 * su)
        im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        r = int(28 * su); hb = int(78 * su)
        d.rounded_rectangle((0, 0, w - 1, h - 1), r, fill=C + (255,))
        d.rounded_rectangle((0, 0, w - 1, hb), r, fill=P + (255,)); d.rectangle((0, int(50 * su), w - 1, hb), fill=P + (255,))
        if nome == 'planilha':
            for i in range(1, 3):
                d.line((i * w / 3, hb, i * w / 3, h - 24 * su), fill=I + (90,), width=max(1, int(3 * su)))
            for j in range(1, 5):
                d.line((24 * su, hb + j * 48 * su, w - 24 * su, hb + j * 48 * su), fill=I + (90,), width=max(1, int(3 * su)))
            d.text((26 * su, 18 * su), rotulo or 'ROI', font=self.font(self.f_titulo, int(44 * su)), fill=Wt + (255,))
            d.text((w - 120 * su, 30 * su), 'R$  %', font=self.font(self.f_texto[800], int(24 * su)), fill=Wt + (255,))
        elif nome == 'calendario':
            d.text((26 * su, 18 * su), (rotulo or '').upper(), font=self.font(self.f_titulo, int(44 * su)), fill=Wt + (255,))
            for i in range(4):
                for j in range(3):
                    x0, y0 = 30 * su + i * 62 * su, hb + 30 * su + j * 70 * su
                    d.rounded_rectangle((x0, y0, x0 + 46 * su, y0 + 46 * su), int(8 * su), fill=(P if (i, j) == (2, 1) else I) + ((255,) if (i, j) == (2, 1) else (60,)))
        elif nome == 'check':
            d.text((26 * su, 18 * su), (rotulo or '').upper(), font=self.font(self.f_titulo, int(44 * su)), fill=Wt + (255,))
            cx, cy = w / 2, hb + (h - hb) / 2
            d.line((cx - 70 * su, cy, cx - 15 * su, cy + 55 * su, cx + 80 * su, cy - 60 * su), fill=P + (255,), width=int(26 * su), joint='curve')
        return self.np.array(im)

    def chart_card(self, p, titulo):
        from PIL import Image, ImageDraw
        su = self.su; E = self.EASE
        P, P2, I, C = self.cor('primaria'), self.cor('secundaria') if 'secundaria' in self.cores else self.cor('primaria'), self.cor('tinta'), self.cor('fundo')
        w, h = int(380 * su), int(300 * su)
        im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, w - 1, h - 1), int(28 * su), fill=I + (235,))
        d.text((30 * su, 26 * su), titulo, font=self.font(self.f_texto[800], int(22 * su)), fill=C + (255,))
        for i, v in enumerate([0.32, 0.5, 0.68, 0.95]):
            q = E(min(1, max(0, p * 1.6 - i * 0.18)))
            bh = int(170 * su * v * q); x = 34 * su + i * 82 * su
            d.rectangle((x, 270 * su - bh, x + 58 * su, 270 * su), fill=(P if i == 3 else (P2 if i == 2 else (90, 90, 95))) + (255,))
        if p > 0.5:
            a = E((p - 0.5) * 2)
            x1, y1 = 40 * su + int(300 * su * a), 230 * su - int(150 * su * a)
            d.line((40 * su, 230 * su, x1, y1), fill=C + (255,), width=max(2, int(8 * su)))
            d.polygon([(x1 + 14 * su, y1 - 12 * su), (x1 - 10 * su, y1 - 14 * su), (x1 + 6 * su, y1 + 10 * su)], fill=C + (255,))
        return self.np.array(im)

    def arrow(self, size, color):
        from PIL import Image, ImageDraw
        im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.line((10 * size / 90, size / 2, size - 30 * size / 90, size / 2), fill=color + (255,), width=max(2, int(14 * size / 90)))
        d.polygon([(size - 6 * size / 90, size / 2), (size - 40 * size / 90, size / 2 - 28 * size / 90), (size - 40 * size / 90, size / 2 + 28 * size / 90)], fill=color + (255,))
        return self.np.array(im)

    def _end_sprites(self):
        su = self.su; tf = self.c['tela_final']
        self.EC = []
        for it in tf.get('itens', []):
            tp = it['tipo']; s = None
            if tp == 'rotulo':
                s = self.text_sprite(it['texto'], self.f_texto[800], it.get('tamanho', 34) * su, self.cor(it.get('cor', 'primaria')), 0.16)
            elif tp == 'titulo':
                s = self.text_sprite(it['texto'], self.f_titulo, it.get('tamanho', 200) * su, self.cor(it.get('cor', 'tinta')), -0.02)
            elif tp == 'pilula':
                s = self.pill(it['texto'], self.fonte(it.get('fonte', 'titulo'), 800), it.get('tamanho', 74) * su, self.cor(it.get('cor_texto', 'fundo')),
                              self.cor(it.get('cor_fundo', 'tinta')), padx=46 * su, pady=26 * su, radius=int(it.get('raio', 20) * su))
            elif tp == 'texto':
                s = self.text_sprite(it['texto'], self.f_texto[it.get('peso', 600)], it.get('tamanho', 40) * su, self.cor(it.get('cor', 'tinta')), 0.0)
            elif tp == 'botao':
                s = self.pill(it['texto'], self.f_texto[800], it.get('tamanho', 46) * su, self.cor(it.get('cor_texto', 'branco')),
                              self.cor(it.get('cor_fundo', 'primaria')), padx=60 * su, pady=36 * su, tracking=0.08)
            elif tp == 'link':
                s = self.text_sprite(it['texto'], self.f_texto[800], it.get('tamanho', 30) * su, self.cor(it.get('cor', 'tinta')), 0.16)
            elif tp == 'faixa':  # faixa de cor de ponta a ponta (ex.: fundo escuro para o logo de fundo escuro)
                s = None
            elif tp == 'logo':
                if not self.logo:
                    continue
                from PIL import Image
                lg = self.np.array(Image.open(self.logo).convert('RGBA'))
                sc = it.get('largura', 460) * su / lg.shape[1]
                s = self.cv2.resize(lg, None, fx=sc, fy=sc, interpolation=self.cv2.INTER_AREA)
            self.EC.append({**it, '_spr': s})
        L, th = int(150 * su), max(2, int(14 * su))
        P = self.cor('primaria')
        self.ec_corners = (self.corner(L, th, P), self.corner(L, th, P)[::-1, ::-1].copy())
        self.ec_arrow = self.arrow(int(90 * su), P)

    # ---------------- camadas ----------------
    def zoom_at(self, t, k):
        tr = self.c['trechos'][k]
        z = tr.get('zoom', 1.0)
        ts = self.T0[k]; punched = False
        if tr.get('punch'):
            tp = self.resolve({'palavra': tr['punch']['palavra'], 'a_partir_do_trecho': k})
            if t >= tp:
                z = tr['punch'].get('zoom', z * 1.14); ts = tp; punched = True
        settle = 1 + 0.045 * (1 - self.prog(t, ts, 0.32, self.FAST)) if (k > 0 or punched) else 1.0
        drift = 1 + 0.02 * (t - self.T0[k]) / (self.SEGS[k][1] - self.SEGS[k][0])
        return z * settle * drift

    def warp_matrix(self, sw, sh, z):
        np = self.np
        s0 = max(self.W / sw, self.H / sh)
        cw, ch = self.W / (s0 * z), self.H / (s0 * z)
        ax, ay = sw * 0.5, sh * self.c.get('enquadramento', {}).get('rosto_y', 0.33)
        x0 = min(max(ax - cw / 2, 0), sw - cw); y0 = min(max(ay - ch * 0.33, 0), sh - ch)
        s = self.W / cw
        return np.float32([[s, 0, -x0 * s], [0, s, -y0 * s]])

    def element_draw(self, img, e, t, camada):
        tp = e['tipo']
        atras = tp == 'texto_atras'
        if (camada == 'atras') != atras:
            return
        t0, t1 = e['_t0'], e['_t1']
        if not (t0 <= t <= t1):
            return
        sx, sy, su = self.sx, self.sy, self.su
        ent = e.get('entrada', {})
        din = ent.get('duracao', self.DIN)
        o, p = self.enter_exit(t, t0, t1, din=din)
        x, y = e.get('x', 540) * sx, e.get('y', 960) * sy
        dx, dy = ent.get('dx', 0) * sx, ent.get('dy', 140 if atras else 50) * sy
        s0 = ent.get('escala', 1.08 if atras else 1.0)
        anchor = e.get('ancora', 'c')
        if tp == 'nome':
            bw = int((e['_spr']['nome'].shape[1] + 80 * su) * p)
            yb = y
            if bw > 4 and o > 0:
                bar = self.np.zeros((int(150 * su), bw, 4), self.np.uint8)
                bar[..., :3] = self.cor('tinta'); bar[..., 3] = 230; bar[:, :max(2, int(12 * su)), :3] = self.cor('primaria')
                self.place(img, bar, 0, yb, o, anchor='tl')
            o2, p2 = self.enter_exit(t, t0 + 0.15, t1)
            self.place(img, e['_spr']['rot'], 52 * sx + 30 * sx * (1 - p2), yb + 20 * sy, o2, anchor='tl')
            self.place(img, e['_spr']['nome'], 52 * sx + 30 * sx * (1 - p2), yb + 58 * sy, o2, anchor='tl')
            return
        spr = e['_spr']
        if tp == 'grafico':
            cp = min(1, max(0, (t - t0) / 1.4))
            spr = self.chart_card(cp, e.get('texto', 'SEUS RESULTADOS'))
        self.place(img, spr, x + dx * (1 - p), y + dy * (1 - p), o, scale=s0 - (s0 - 1) * p, anchor=anchor)

    def caption_sprite(self, group, t):
        from PIL import Image, ImageDraw
        leg = self.c.get('legendas', {}); su = self.su
        f = self.font(self.f_texto[800], int(leg.get('tamanho', 66) * su))
        up = leg.get('maiusculas', True)
        toks = [w.upper() if up else w for _, _, w, _ in group]
        space = f.getlength(' ')
        widths = [f.getlength(x) for x in toks]
        tw = sum(widths) + space * (len(toks) - 1)
        asc, desc = f.getmetrics()
        padx, pady = int(34 * su), int(20 * su)
        im = Image.new('RGBA', (int(tw + 2 * padx), asc + desc + 2 * pady), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        if leg.get('caixa', True):
            d.rounded_rectangle((0, 0, im.width - 1, im.height - 1), int(22 * su), fill=self.cor('tinta') + (215,))
        x = padx
        karaoke = leg.get('estilo', 'karaoke') == 'karaoke'
        for (s, e, w, key), tok, wd in zip(group, toks, widths):
            spoken = (t >= s - 0.03) or not karaoke
            col = (self.cor(leg.get('cor_destaque', 'primaria')) if key else self.cor('branco')) + ((255,) if spoken else (110,))
            d.text((x, pady - 2), tok, font=f, fill=col)
            x += wd + space
        return self.np.array(im)

    def overlay(self, img, t):
        for e in self.E:
            self.element_draw(img, e, t, 'frente')
        if self.cantoneiras is not None:
            m = int(40 * self.su)
            self.place(img, self.cantoneiras[0], m, m, 0.95, anchor='tl')
            self.place(img, self.cantoneiras[1], self.W - m, self.H - m, 0.95, anchor='br')
        leg = self.c.get('legendas', {})
        if leg.get('estilo', 'karaoke') != 'nenhuma':
            for (s, e), g in zip(self.GT, self.GROUPS):
                if s - 0.02 <= t < e:
                    o = min(1, (t - s + 0.02) / 0.12); sc = 0.94 + 0.06 * self.FAST(min(1, (t - s + 0.02) / 0.18))
                    cs = self.caption_sprite(g, t); fit = min(1.0, (leg.get('largura_max', 820) * self.sx) / cs.shape[1])
                    self.place(img, cs, self.W / 2, leg.get('y', 1390) * self.sy, o, scale=sc * fit)
                    break
        if self.c['marca'].get('barra_progresso', True):
            pw = int(self.W * min(1, t / self.T_END))
            img[0:max(2, int(8 * self.su)), :pw] = self.cor('primaria')

    def end_card(self, tc):
        np = self.np
        img = np.empty((self.H, self.W, 3), np.uint8); img[:] = self.cor(self.c['tela_final'].get('fundo', 'fundo'))
        sx, sy, su = self.sx, self.sy, self.su
        for it in self.EC:
            s = it['_spr']
            if it['tipo'] == 'faixa':
                o, p = self.enter_exit(tc, 0.3 + it.get('atraso', 0.0), 99)
                y0, y1 = int(it['de_y'] * sy), int(it['ate_y'] * sy)
                cor = np.array(self.cor(it.get('cor', 'tinta')), np.float32)
                desl = int((1 - p) * self.W)  # entra deslizando da direita
                reg = img[y0:y1, desl:].astype(np.float32)
                img[y0:y1, desl:] = (reg * (1 - o) + cor * o).astype(np.uint8)
                continue
            if s is None:
                continue
            o, p = self.enter_exit(tc, 0.35 + it.get('atraso', 0.0), 99)
            cy = it['y'] * sy + 60 * sy * (1 - p)
            self.place(img, s, self.W / 2, cy, o)
            if it['tipo'] == 'botao' and it.get('seta', True):
                oa, pa = self.enter_exit(tc, 0.9, 99)
                self.place(img, self.ec_arrow, self.W / 2 + s.shape[1] / 2 + 70 * su - 30 * su * (1 - pa), it['y'] * sy, oa, scale=0.8 + 0.2 * pa)
        o, p = self.enter_exit(tc, 0.25, 99)
        m = 60 * su
        self.place(img, self.ec_corners[0], m - 40 * su * (1 - p), m - 40 * su * (1 - p), o, anchor='tl')
        self.place(img, self.ec_corners[1], self.W - m + 40 * su * (1 - p), self.H - m + 40 * su * (1 - p), o, anchor='br')
        return img

    # ---------------- fontes de quadro ----------------
    class Leitor:
        """lê quadros de um vídeo em sequência (o seek do OpenCV não é exato)"""
        def __init__(self, cv2, path):
            self.cv2, self.path = cv2, path
            self.cap = cv2.VideoCapture(path)
            if not self.cap.isOpened():
                raise SystemExit(f'não consegui abrir o vídeo: {path}')
            self.fps = self.cap.get(5) or 30
            self.n = int(self.cap.get(7)) or 10 ** 9
            self.pos = -1; self.frame = None

        def get(self, idx):
            idx = max(0, min(idx, self.n - 1))
            if idx < self.pos:
                self.cap.release(); self.cap = self.cv2.VideoCapture(self.path); self.pos = -1
            while self.pos < idx - 1 and self.cap.grab():
                self.pos += 1
            while self.pos < idx:
                ok, f = self.cap.read()
                if not ok:
                    self.n = self.pos + 1
                    break
                self.pos += 1; self.frame = f
            return self.cv2.cvtColor(self.frame, self.cv2.COLOR_BGR2RGB)

        def at(self, sec):
            return self.get(int(round(sec * self.fps)))

    def caminho(self, p):
        p = Path(p)
        return str(p if p.is_absolute() else (self.cfg_path.parent / p))

    def open_source(self):
        import numpy as np
        self.orig = self.Leitor(self.cv2, self.video)
        self.src_fps = self.orig.fps
        # versão melhorada (ex.: upscale por IA) com o mesmo conteúdo e duração do bruto
        hd = self.c.get('video_hd')
        self.hd = self.Leitor(self.cv2, self.caminho(hd)) if hd else None
        mp = self.cfg_path.parent / 'trabalho' / 'mascaras.npy'
        self.prof = self.c.get('profundidade', {}).get('ativo', True) and mp.exists()
        self.masks = np.load(mp, mmap_mode='r') if self.prof else None
        # inserções (B-roll) em tela cheia
        self.INS = []
        for ins in self.c.get('insercoes', []):
            self.INS.append({**ins, '_t0': self.resolve(ins['de']), '_t1': self.resolve(ins['ate']),
                             '_r': self.Leitor(self.cv2, self.caminho(ins['arquivo']))})

    def get_frame(self, idx):  # compatibilidade
        return self.orig.get(idx)

    def get_mask(self, idx):
        np = self.np; M = self.masks
        idx = min(idx, len(M) - 1)
        if 0 < idx < len(M) - 1:
            return ((M[idx - 1].astype(np.uint16) + 2 * M[idx].astype(np.uint16) + M[idx + 1].astype(np.uint16)) // 4).astype(np.uint8)
        return np.array(M[idx])

    def aplicar_insercoes(self, canvas, t):
        np, cv2 = self.np, self.cv2
        for ins in self.INS:
            t0, t1 = ins['_t0'], ins['_t1']
            if not (t0 <= t < t1):
                continue
            ct = ins.get('inicio_clip', 0.0) + (t - t0)
            fr = ins['_r'].at(ct)
            sh_, sw_ = fr.shape[:2]
            z = 1.0 + ins.get('zoom_lento', 0.06) * (t - t0) / max(0.01, t1 - t0)
            s0 = max(self.W / sw_, self.H / sh_) * z
            x0, y0 = (sw_ - self.W / s0) / 2, (sh_ - self.H / s0) / 2
            A = np.float32([[s0, 0, -x0 * s0], [0, s0, -y0 * s0]])
            img = cv2.warpAffine(fr, A, (self.W, self.H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
            if ins.get('tratamento', True):  # aproxima do visual do vídeo: leve dessaturação e vinheta
                f = img.astype(np.float32); g = f.mean(axis=2, keepdims=True)
                img = np.clip((f * 0.88 + g * 0.12) * (0.75 + 0.25 * self.VIG), 0, 255).astype(np.uint8)
            tr = ins.get('transicao', 0.15)
            a = 1.0
            if tr > 0:
                a = min(1.0, (t - t0) / tr, (t1 - t) / tr)
            canvas = (canvas.astype(np.float32) * (1 - a) + img.astype(np.float32) * a).astype(np.uint8)
        return canvas

    def em_insercao(self, t):
        return any(i['_t0'] <= t < i['_t1'] for i in getattr(self, 'INS', []))

    def render_frame(self, i):
        np, cv2 = self.np, self.cv2
        t = i / self.FPS
        out = None
        if t < self.T_END:
            k = self.seg_at(t); src_t = self.SEGS[k][0] + (t - self.T0[k])
            fi = int(round(src_t * self.src_fps))
            src = self.hd.at(src_t) if self.hd else self.orig.get(fi)
            sh_, sw_ = src.shape[:2]
            z = self.zoom_at(t, k)
            A = self.warp_matrix(sw_, sh_, z)
            fr = cv2.warpAffine(src, A, (self.W, self.H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT).astype(np.float32)
            fr = np.clip(fr + 0.5 * (fr - cv2.GaussianBlur(fr, (0, 0), 1.4)), 0, 255)
            if self.prof:
                mk = self.get_mask(fi)
                r = sw_ / mk.shape[1]
                Am = A.copy(); Am[:, :2] *= r
                m = cv2.warpAffine(mk, Am, (self.W, self.H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
                m = np.clip((cv2.GaussianBlur(m, (0, 0), 1.6).astype(np.float32) / 255.0 - 0.12) / 0.7, 0, 1)[..., None]
                pf = self.c.get('profundidade', {})
                sig = 1 + (pf.get('desfoque', 10) - 1) * self.prog(t, 0.0, pf.get('rack_focus', 0.9))
                bgsrc = fr * (1 - m) + cv2.GaussianBlur(fr, (0, 0), 6) * m
                bg = cv2.GaussianBlur(bgsrc, (0, 0), sig)
                gray = bg.mean(axis=2, keepdims=True)
                bg = (bg * 0.82 + gray * 0.18) * self.VIG * 0.9
                canvas = bg.astype(np.uint8)
                for e in self.E:
                    self.element_draw(canvas, e, t, 'atras')
                canvas = np.clip(canvas.astype(np.float32) * (1 - m) + fr * m, 0, 255).astype(np.uint8)
            else:
                canvas = fr.astype(np.uint8)
                for e in self.E:  # sem recorte: texto "atrás" vira texto na frente, mais transparente
                    if e['tipo'] == 'texto_atras':
                        e2 = dict(e); e2['tipo'] = '_frente'
                        o, p = self.enter_exit(t, e['_t0'], e['_t1'])
                        self.place(canvas, e['_spr'], e.get('x', 540) * self.sx, e.get('y', 960) * self.sy + 140 * self.sy * (1 - p), o * 0.85, scale=1.08 - 0.08 * p)
            canvas = self.aplicar_insercoes(canvas, t)
            self.overlay(canvas, t)
            out = canvas
        if self.CARD > 0:
            tw = t - (self.T_END - 0.15)
            if tw > 0:
                card = self.end_card(t - self.T_END)
                if out is None:
                    out = self.last.copy()
                p1 = self.EASE(min(1, tw / 0.55)); p2 = self.EASE(min(1, max(0, tw - 0.12) / 0.55))

                def diag(p):
                    edge = self.H * (1 - p) * 1.25 - 0.25 * self.H
                    yline = edge + (self.xx[:1, :] / self.W) * 0.25 * self.H * (1 - p)
                    return (self.yy >= yline).astype(np.float32)[..., None]
                mo, mc = diag(p1), diag(p2)
                orange = np.empty_like(out); orange[:] = self.cor('primaria')
                out = out * (1 - mo) + orange * mo
                out = (out * (1 - mc) + card * mc).astype(np.uint8)
            else:
                self.last = out
        g = self.GRAIN[i % len(self.GRAIN)]
        return np.clip(out.astype(np.float32) + g * self.grain_amt, 0, 255).astype(np.uint8)

    # ---------------- áudio ----------------
    def audio(self, saida_wav):
        import numpy as np, soundfile as sf
        from scipy.signal import butter, sosfilt
        SR = 44100
        tmp = str(TRAB / 'voz_limpa.wav')
        sh(['ffmpeg', '-y', '-v', 'error', '-i', self.video, '-af',
            'highpass=f=80,afftdn=nf=-30,acompressor=threshold=-20dB:ratio=3:attack=5:release=80', '-ac', '1', '-ar', str(SR), tmp])
        v, _ = sf.read(tmp)
        voice = np.zeros(int(self.TOTAL * SR) + SR)
        fade = int(0.012 * SR); pos = 0
        for a, b in self.SEGS:
            c = v[int(a * SR):int(b * SR)].copy()
            c[:fade] *= np.linspace(0, 1, fade); c[-fade:] *= np.linspace(1, 0, fade)
            voice[pos:pos + len(c)] += c; pos += len(c)
        fx = np.zeros_like(voice)
        rng = np.random.default_rng(3)

        def whoosh(dur=0.45, gain=0.10, lo=300, hi=3500):
            n = int(dur * SR); x = rng.normal(0, 1, n); y = np.zeros(n)
            for i in range(24):
                s, e = i * n // 24, (i + 1) * n // 24
                f = lo + (hi - lo) * np.sin(np.pi * i / 24)
                sos = butter(2, [f * 0.6, min(f * 1.6, SR / 2 - 100)], btype='band', fs=SR, output='sos')
                y[s:e] = sosfilt(sos, x)[s:e]
            return y * np.sin(np.linspace(0, np.pi, n)) ** 2 / np.abs(y).max() * gain

        def pop(gain=0.12):
            n = int(0.09 * SR); tt = np.arange(n) / SR
            f = 900 * np.exp(-tt * 30) + 250
            return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 45) * gain

        def put(buf, sig, t):
            i = int(t * SR); buf[i:i + len(sig)] += sig[:len(buf) - i]
        if self.c.get('audio', {}).get('efeitos', True):
            for e in self.E:
                if e['tipo'] == 'texto_atras':
                    put(fx, whoosh(0.42, 0.07), max(0, e['_t0'] - 0.12))
            for e in self.E:
                if e['tipo'] not in ('texto_atras', 'rotulo') and e.get('som', True):
                    put(fx, pop(0.08), e['_t0'] + 0.03)
            if self.CARD > 0:
                put(fx, whoosh(0.7, 0.13, 200, 2500), self.T_END - 0.35)
                put(fx, pop(0.07), self.T_END + 0.9)
        mix = voice + fx
        tr = self.c.get('audio', {}).get('trilha')
        if tr:
            tp = Path(tr); tp = tp if tp.is_absolute() else self.cfg_path.parent / tp
            sh(['ffmpeg', '-y', '-v', 'error', '-i', str(tp), '-ac', '1', '-ar', str(SR), str(TRAB / 'trilha.wav')])
            mus, _ = sf.read(str(TRAB / 'trilha.wav'))
            ini = self.c['audio'].get('trilha_inicio', 0.0)
            mus = mus[int(ini * SR):]
            if len(mus) < len(mix):
                mus = np.tile(mus, int(np.ceil(len(mix) / max(1, len(mus)))))
            mus = mus[:len(mix)]
            win = int(0.05 * SR)
            env = np.sqrt(np.convolve(voice ** 2, np.ones(win) / win, mode='same'))
            env = np.convolve(env, np.ones(int(0.3 * SR)) / int(0.3 * SR), mode='same')
            env = np.clip(env / (env.max() + 1e-9) * 3, 0, 1)
            base = 10 ** (self.c['audio'].get('volume_trilha_db', -16) / 20)
            duck = 10 ** (-self.c['audio'].get('abaixar_sob_voz_db', 12) / 20)
            g = base * (1 - env * (1 - duck))
            if self.CARD > 0:
                g[int(self.T_END * SR):] = base * 1.6
            g[:int(0.5 * SR)] *= np.linspace(0, 1, int(0.5 * SR))
            nf = int(0.8 * SR); g[-nf:] *= np.linspace(1, 0, nf)
            mix = mix + mus / (np.abs(mus).max() + 1e-9) * 0.5 * g
        mix = mix[:int(self.TOTAL * SR)]
        raw = str(TRAB / 'mix_raw.wav')
        sf.write(raw, mix, SR)
        sh(['ffmpeg', '-y', '-v', 'error', '-i', raw, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '48000', '-ac', '2', saida_wav])

    # ---------------- saída ----------------
    def render(self):
        TRAB.mkdir(exist_ok=True)
        self.open_source()
        vid = str(TRAB / 'video_sem_audio.mp4')
        p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{self.W}x{self.H}',
                              '-r', str(self.FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', str(self.c.get('qualidade_crf', 20)),
                              '-pix_fmt', 'yuv420p', vid], stdin=subprocess.PIPE)
        for i in range(self.NF):
            p.stdin.write(self.render_frame(i).tobytes())
            if i % 60 == 0:
                print(f'quadro {i}/{self.NF}', flush=True)
        p.stdin.close(); p.wait()
        wav = str(TRAB / 'mix.wav')
        self.audio(wav)
        saida = self.c.get('saida', 'resultado/video.mp4')
        Path(saida).parent.mkdir(parents=True, exist_ok=True)
        sh(['ffmpeg', '-y', '-v', 'error', '-i', vid, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac',
            '-b:a', '192k', '-shortest', '-movflags', '+faststart', saida])
        print('done', saida)

    def previa(self, tempos):
        import numpy as np
        TRAB.mkdir(exist_ok=True)
        self.open_source()
        ims = []
        for t in tempos:
            if self.CARD > 0 and t >= self.T_END - 0.15:
                self.render_frame(int((self.T_END - 0.2) * self.FPS))
            fr = self.render_frame(int(round(t * self.FPS)))
            th = self.cv2.resize(fr, (270, int(270 * self.H / self.W)))
            self.cv2.putText(th, f'{t:.2f}s', (8, 22), self.cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            ims.append(th)
        cols = 5
        while len(ims) % cols:
            ims.append(np.zeros_like(ims[0]))
        rows = [np.hstack(ims[i:i + cols]) for i in range(0, len(ims), cols)]
        out = str(TRAB / 'previa.jpg')
        self.cv2.imwrite(out, self.cv2.cvtColor(np.vstack(rows), self.cv2.COLOR_RGB2BGR))
        print('trechos (início na saída):', [round(x, 2) for x in self.T0], 'fim da fala:', round(self.T_END, 2), 'total:', round(self.TOTAL, 2))
        print('legendas:')
        for (s, e), g in zip(self.GT, self.GROUPS):
            print(f'  {s:6.2f}-{e:6.2f} ', ' '.join(('*' + x[2] + '*') if x[3] else x[2] for x in g))
        print(out)


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == 'preparar':
        preparar(*([args] if args else []))
    elif cmd == 'analisar':
        analisar(args[0], profundidade='--sem-profundidade' not in args,
                 idioma=next((a.split('=')[1] for a in args if a.startswith('--idioma=')), 'pt'))
    elif cmd == 'referencia':
        referencia(args[0])
    elif cmd == 'previa':
        Motor(args[0]).previa([float(x) for x in args[1:]])
    elif cmd == 'render':
        Motor(args[0]).render()
    elif cmd == 'folha':
        folha(args[0], args[1] if len(args) > 1 else None)
    else:
        print(__doc__); sys.exit(1)


if __name__ == '__main__':
    main()
