#!/usr/bin/env python3
"""Copywriter de publicação sênior · Trentin Solutions · trentinsolutions.com.br

Comandos:
  preparar                       instala dependências e baixa o detector de rosto
  quadros VIDEO [--n 12] [--saida DIR]
                                 escolhe os melhores quadros para capa (nitidez, cor, rosto, sem borrão)
  capa VIDEO --tempo T --titulo "LINHA 1|LINHA 2" [--subtitulo TXT] [--marca marca.json]
       [--estilo adesivo|faixa|limpo] [--posicao auto|alto|meio|baixo] [--saida DIR]
                                 monta a capa 9:16 com o título dentro do recorte 3:4 da grade
  checar TEXTOS.json             confere tamanho, gancho, hashtags, números e datas de cada legenda
"""
import sys, os, re, json, math, argparse, subprocess, shutil, glob, unicodedata

CACHE = os.path.expanduser('~/.cache/copywriter-publicacao-senior')
YUNET_URL = 'https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx'
W, H = 1080, 1920
GRADE = (240, 1680)          # recorte 3:4 (1080x1440) que aparece na grade do perfil
SEGURO_TOPO, SEGURO_BASE = 300, 1450

def sh(cmd, **kw):
    return subprocess.run(cmd, shell=isinstance(cmd, str), check=True, **kw)

# ---------------- preparar ----------------
def preparar():
    faltam = []
    for mod, pip in (('cv2', 'opencv-python-headless'), ('PIL', 'pillow'), ('numpy', 'numpy')):
        try: __import__(mod)
        except ImportError: faltam.append(pip)
    if faltam: sh([sys.executable, '-m', 'pip', 'install', '-q', '--break-system-packages'] + faltam)
    os.makedirs(CACHE, exist_ok=True)
    yu = os.path.join(CACHE, 'yunet.onnx')
    outros = glob.glob(os.path.expanduser('~/.cache/*/yunet.onnx'))
    if not os.path.exists(yu):
        if outros: shutil.copy(outros[0], yu)
        else:
            try: sh(['curl', '-sSLf', '-o', yu, YUNET_URL])
            except Exception: print('aviso: detector de rosto não baixou; a capa segue sem desviar de rostos')
    for f in ('montserrat', 'anton'): baixar_fonte(f)
    print('pronto')

def baixar_fonte(nome):
    pasta = os.path.join(CACHE, 'fontes', nome)
    if os.path.isdir(pasta): return pasta
    os.makedirs(os.path.join(CACHE, 'fontes'), exist_ok=True)
    tmp = os.path.join(CACHE, 'tmp'); os.makedirs(tmp, exist_ok=True)
    try:
        sh(f'cd "{tmp}" && npm pack -s @fontsource/{nome} >/dev/null 2>&1 && tar xzf fontsource-{nome}-*.tgz && mv package "{pasta}" && rm -f fontsource-{nome}-*.tgz')
    except Exception:
        print(f'aviso: fonte {nome} não encontrada no @fontsource'); return None
    return pasta

def caminho_fonte(nome, peso=700):
    pasta = baixar_fonte(nome)
    if not pasta: return None
    for p in (peso, 800, 700, 600, 400):
        for ext in ('woff', 'woff2', 'ttf'):
            c = os.path.join(pasta, 'files', f'{nome}-latin-{p}-normal.{ext}')
            if os.path.exists(c): return c
    achados = sorted(glob.glob(os.path.join(pasta, 'files', f'{nome}-latin-*-normal.woff')))
    return achados[-1] if achados else None

# ---------------- utilidades de vídeo ----------------
def abrir(video):
    import cv2
    cap = cv2.VideoCapture(video)
    if not cap.isOpened(): sys.exit(f'não abri {video}')
    return cap

def detector_rosto(w, h):
    import cv2
    yu = os.path.join(CACHE, 'yunet.onnx')
    if not os.path.exists(yu):
        outros = glob.glob(os.path.expanduser('~/.cache/*/yunet.onnx'))
        if not outros: return None
        yu = outros[0]
    try: return cv2.FaceDetectorYN.create(yu, '', (w, h), 0.75)
    except Exception: return None

def rostos(det, img):
    if det is None: return []
    import cv2
    h, w = img.shape[:2]; det.setInputSize((w, h))
    _, fs = det.detect(img)
    return [] if fs is None else [tuple(float(v) for v in f[:4]) for f in fs]

# ---------------- quadros ----------------
def quadros(video, n=12, saida='capa_trabalho'):
    import cv2, numpy as np
    os.makedirs(saida, exist_ok=True)
    cap = abrir(video); fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); dur = total / fps
    passo = max(1, int(fps / 4))
    det = detector_rosto(270, 480)
    cand, ant = [], None
    for i in range(total):
        ok, f = cap.read()
        if not ok: break
        if i % passo: continue
        p = cv2.resize(f, (270, 480)); g = cv2.cvtColor(p, cv2.COLOR_BGR2GRAY)
        nit = cv2.Laplacian(g, cv2.CV_64F).var()
        b, gg, r = [c.astype(np.float32) for c in cv2.split(p)]
        rg, yb = r - gg, 0.5 * (r + gg) - b
        cor = math.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * math.sqrt(rg.mean() ** 2 + yb.mean() ** 2)
        mov = float(np.abs(g.astype(np.float32) - ant).mean()) if ant is not None else 0.0
        ant = g.astype(np.float32)
        brilho = g.mean()
        fs = rostos(det, p)
        cand.append(dict(t=round(i / fps, 2), nitidez=nit, cor=cor, movimento=mov, brilho=brilho, rostos=len(fs)))
    if not cand: sys.exit('vídeo sem quadros')
    def norm(k):
        v = np.array([c[k] for c in cand], np.float32); lo, hi = np.percentile(v, 5), np.percentile(v, 95)
        return np.clip((v - lo) / (hi - lo + 1e-6), 0, 1)
    nn, nc, nm = norm('nitidez'), norm('cor'), norm('movimento')
    for k, c in enumerate(cand):
        luz = 1 - min(1, abs(c['brilho'] - 125) / 90)
        c['nota'] = round(float(0.45 * nn[k] + 0.25 * nc[k] + 0.15 * luz + 0.15 * (1 - nm[k]) + (0.15 if c['rostos'] else 0)), 3)
        if c['t'] < 0.3 or c['t'] > dur - 0.3: c['nota'] -= 0.2      # evita início e fim (fade, preto)
    escolhidos = []
    for c in sorted(cand, key=lambda c: -c['nota']):
        if all(abs(c['t'] - e['t']) >= max(0.8, dur / (n * 2.5)) for e in escolhidos): escolhidos.append(c)
        if len(escolhidos) >= n: break
    escolhidos.sort(key=lambda c: c['t'])
    # folha
    cap = abrir(video); fr = []
    for c in escolhidos:
        cap.set(cv2.CAP_PROP_POS_MSEC, c['t'] * 1000); ok, f = cap.read()
        if not ok: continue
        f = cv2.resize(f, (270, 480))
        cv2.rectangle(f, (0, 0), (270, 26), (0, 0, 0), -1)
        cv2.putText(f, f"{c['t']:.2f}s  nota {c['nota']:.2f}", (6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
        fr.append(f)
    while len(fr) % 6: fr.append(np.zeros_like(fr[0]))
    cv2.imwrite(os.path.join(saida, 'quadros.jpg'), np.vstack([np.hstack(fr[i:i + 6]) for i in range(0, len(fr), 6)]))
    json.dump(dict(video=video, duracao=round(dur, 2), quadros=escolhidos), open(os.path.join(saida, 'quadros.json'), 'w'), ensure_ascii=False, indent=1)
    print(f'{len(escolhidos)} quadros em {saida}/quadros.jpg')
    for c in escolhidos: print(f"  {c['t']:6.2f}s  nota {c['nota']:.2f}  rostos {c['rostos']}")

# ---------------- capa ----------------
def hexrgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def carregar_marca(p):
    padrao = dict(nome='', cores=dict(primaria='#f26522', secundaria='#ffd84d', fundo='#F4EFE8', tinta='#141416', branco='#ffffff'),
                  fontes=dict(titulo=dict(nome='anton', peso=400), texto=dict(nome='montserrat', peso=800)))
    if not p: return padrao
    d = json.load(open(p))
    m = d.get('marca', d)
    for k in ('cores', 'fontes'):
        padrao[k].update(m.get(k, {}))
    padrao['nome'] = m.get('nome', '')
    padrao['capa'] = d.get('preferencias', {}).get('capa', {}) if 'preferencias' in d else {}
    return padrao

def capa(video, tempo, titulo, subtitulo='', marca=None, estilo='adesivo', posicao='auto', saida='capa_trabalho', realce=True):
    import cv2, numpy as np
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    os.makedirs(saida, exist_ok=True)
    mk = carregar_marca(marca)
    cores = {k: hexrgb(v) for k, v in mk['cores'].items()}
    ft = mk['fontes']['titulo']; fx = mk['fontes']['texto']
    f_tit = caminho_fonte(ft['nome'], ft.get('peso', 700)) or caminho_fonte('anton', 400)
    f_sub = caminho_fonte(fx['nome'], fx.get('peso', 800)) or caminho_fonte('montserrat', 800)
    cap = abrir(video); cap.set(cv2.CAP_PROP_POS_MSEC, float(tempo) * 1000); ok, f = cap.read()
    if not ok: sys.exit('não li o quadro')
    f = cv2.resize(f, (W, H), interpolation=cv2.INTER_LANCZOS4) if f.shape[1] != W else f
    if realce:  # leve ajuste de contraste e saturação, como no editor
        x = (f.astype(np.float32) - 128) * 1.06 + 131
        hsv = cv2.cvtColor(np.clip(x, 0, 255).astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32); hsv[..., 1] *= 1.12
        f = cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR)
    det = detector_rosto(W, H); fs = rostos(det, f)
    base = Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)).convert('RGBA')
    linhas = [l.strip() for l in titulo.split('|') if l.strip()]

    def sprite_linha(txt, tam, bg, fg, rot):
        fnt = ImageFont.truetype(f_tit, tam); bb = fnt.getbbox(txt)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        if estilo == 'limpo':
            M = 30; im = Image.new('RGBA', (tw + 2 * M, th + 2 * M), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            d.text((M - bb[0], M - bb[1]), txt, font=fnt, fill=cores['branco'] + (255,), stroke_width=max(4, tam // 14), stroke_fill=cores['tinta'] + (255,))
            return im
        padx, pady = int(tam * .42), int(tam * .2); w, h = tw + 2 * padx, th + 2 * pady; M = 40
        im = Image.new('RGBA', (w + 2 * M, h + 2 * M), (0, 0, 0, 0))
        sh_ = Image.new('RGBA', im.size, (0, 0, 0, 0))
        raio = h // 2 if estilo == 'adesivo' else 10
        borda = 12 if estilo == 'adesivo' else 0
        ImageDraw.Draw(sh_).rounded_rectangle([M - borda + 6, M - borda + 12, M + w + borda + 6, M + h + borda + 12], raio + borda, fill=(0, 0, 0, 120))
        im = Image.alpha_composite(im, sh_.filter(ImageFilter.GaussianBlur(9))); d = ImageDraw.Draw(im)
        if borda: d.rounded_rectangle([M - borda, M - borda, M + w + borda, M + h + borda], raio + borda, fill=cores['branco'] + (255,))
        d.rounded_rectangle([M, M, M + w, M + h], raio, fill=bg + (255,))
        d.text((M + padx - bb[0], M + pady - bb[1]), txt, font=fnt, fill=fg + (255,))
        return im.rotate(rot, Image.BICUBIC, expand=True) if rot else im

    def contraste(c): return cores['tinta'] if 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2] > 160 else cores['branco']
    paleta = [cores.get('primaria'), cores.get('secundaria') or cores.get('primaria'), cores.get('tinta')]
    tam = 150 if max(len(l) for l in linhas) <= 10 else 124 if max(len(l) for l in linhas) <= 14 else 100
    sprs = []
    for k, l in enumerate(linhas):
        bg = paleta[k % len(paleta)]
        sprs.append(sprite_linha(l.upper() if estilo != 'limpo' else l, tam, bg, contraste(bg), (-3 if k % 2 == 0 else 2) if estilo == 'adesivo' else 0))
    larg_max = 960
    for k, s in enumerate(sprs):
        if s.width > larg_max:
            r = larg_max / s.width; sprs[k] = s.resize((int(s.width * r), int(s.height * r)), Image.LANCZOS)
    sub = None
    if subtitulo:
        fnt = ImageFont.truetype(f_sub, 54); bb = fnt.getbbox(subtitulo)
        M = 24; sub = Image.new('RGBA', (bb[2] - bb[0] + 2 * M + 40, bb[3] - bb[1] + 2 * M + 24), (0, 0, 0, 0)); d = ImageDraw.Draw(sub)
        d.rounded_rectangle([M, M, sub.width - M, sub.height - M], (sub.height - 2 * M) // 2, fill=cores['tinta'] + (235,))
        d.text((M + 20 - bb[0], M + 12 - bb[1]), subtitulo, font=fnt, fill=cores['branco'] + (255,))
    bloco_h = sum(s.height - 50 for s in sprs) + (sub.height if sub else 0)

    # posição: dentro do recorte 3:4 e longe do rosto
    opcoes = {'alto': SEGURO_TOPO + 40, 'meio': (GRADE[0] + GRADE[1]) // 2 - bloco_h // 2, 'baixo': SEGURO_BASE - bloco_h}
    def sobre_rosto(y0):
        for (x, y, w, h) in fs:
            if y < y0 + bloco_h and y + h > y0 and w * h > 900: return True
        return False
    if posicao == 'auto':
        y0 = next((opcoes[k] for k in ('baixo', 'meio', 'alto') if not sobre_rosto(opcoes[k])), opcoes['baixo'])
    else:
        y0 = opcoes[posicao]
    # escurece levemente atrás do texto para leitura
    grad = Image.new('L', (1, H), 0)
    for y in range(H):
        d = 0 if not (y0 - 260 < y < y0 + bloco_h + 220) else 70 * (1 - abs((y - (y0 + bloco_h / 2)) / (bloco_h / 2 + 260)))
        grad.putpixel((0, y), int(max(0, d)))
    base = Image.alpha_composite(base, Image.merge('RGBA', [Image.new('L', (W, H), 0)] * 3 + [grad.resize((W, H))]))
    y = y0
    for k, s in enumerate(sprs):
        x = W // 2 - s.width // 2 + (-30 if k % 2 == 0 else 30) * (estilo == 'adesivo')
        base.alpha_composite(s, (max(0, x), int(y))); y += s.height - 50
    if sub: base.alpha_composite(sub, (W // 2 - sub.width // 2, int(y + 10)))
    final = base.convert('RGB')
    p9 = os.path.join(saida, 'capa_9x16.jpg'); final.save(p9, quality=93)
    p34 = os.path.join(saida, 'capa_grade_3x4.jpg'); final.crop((0, GRADE[0], W, GRADE[1])).save(p34, quality=93)
    # folha de conferência: 9:16 com linhas do recorte + recorte 3:4 + recorte 1:1
    prev = final.copy(); d = ImageDraw.Draw(prev)
    for yy, cor, rot in ((GRADE[0], (255, 220, 0), 'grade 3:4'), (GRADE[1], (255, 220, 0), ''), (420, (0, 220, 255), 'feed 1:1'), (1500, (0, 220, 255), '')):
        d.line([(0, yy), (W, yy)], fill=cor, width=6)
        if rot: d.text((20, yy + 10), rot, fill=cor, font=ImageFont.truetype(f_sub, 40))
    a = prev.resize((405, 720)); b = final.crop((0, GRADE[0], W, GRADE[1])).resize((405, 540)); c = final.crop((0, 420, W, 1500)).resize((405, 405))
    folha = Image.new('RGB', (405 * 3 + 40, 720), (20, 20, 24)); folha.paste(a, (0, 0)); folha.paste(b, (425, 90)); folha.paste(c, (850, 157))
    folha.save(os.path.join(saida, 'capa_conferencia.jpg'), quality=88)
    info = dict(tempo=float(tempo), titulo=linhas, subtitulo=subtitulo, estilo=estilo, y_titulo=int(y0), rostos=len(fs),
                rosto_coberto=bool(sobre_rosto(y0)), arquivos=[p9, p34])
    json.dump(info, open(os.path.join(saida, 'capa.json'), 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(info, ensure_ascii=False))

# ---------------- checar ----------------
LIMITES = {
    'instagram': dict(total=2200, gancho=125, hashtags=(3, 5)),
    'tiktok': dict(total=4000, gancho=100, hashtags=(3, 5)),
    'shorts': dict(total=5000, titulo=100, hashtags=(1, 3)),
    'linkedin': dict(total=3000, gancho=210, hashtags=(0, 3)),
    'facebook': dict(total=5000, gancho=125, hashtags=(0, 3)),
}
MESES = r'(?:janeiro|fevereiro|março|marco|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro|jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)'
CTA = r'\b(siga|segue|seguir|vem|venha|garanta|clique|toque|acesse|comente|compartilhe|salve|marque|chama|chame|manda|mande|confira|passa|passe|visite|reserve|inscreva|link na bio|compre|aproveite)\b'

def contar_emojis(s):
    return sum(1 for ch in s if unicodedata.category(ch) == 'So' or ord(ch) >= 0x1F300)

def checar(arq):
    d = json.load(open(arq))
    confirmados = [c.lower() for c in d.get('fatos_confirmados', [])]
    plataformas = d.get('plataformas') or [d.get('plataforma', 'instagram')]
    problemas_total = 0
    for v in d['variantes']:
        texto = v['texto']; tags = v.get('hashtags', [])
        tags_txt = re.findall(r'#\w+', texto)
        todas = [t if t.startswith('#') else '#' + t for t in tags] + tags_txt
        corpo = texto + ('\n\n' + ' '.join(t if t.startswith('#') else '#' + t for t in tags) if tags else '')
        gancho = texto.strip().split('\n')[0]
        print(f"\n== {v.get('rotulo', 'variante')} ==")
        print(f"  caracteres: {len(corpo)} · gancho: {len(gancho)} · hashtags: {len(todas)} · emojis: {contar_emojis(corpo)}")
        probs = []
        for p in plataformas:
            L = LIMITES.get(p, LIMITES['instagram'])
            if len(corpo) > L['total']: probs.append(f'[erro] passa do limite de {L["total"]} caracteres do {p}')
            if 'gancho' in L and len(gancho) > L['gancho']: probs.append(f'[alerta] gancho com {len(gancho)} caracteres: no {p} o texto é cortado em ~{L["gancho"]} ("mais")')
            lo, hi = L['hashtags']
            if len(todas) > hi: probs.append(f'[alerta] {len(todas)} hashtags; use de {lo} a {hi} no {p}')
            if p == 'shorts' and v.get('titulo') and len(v['titulo']) > L['titulo']: probs.append('[erro] título do Shorts com mais de 100 caracteres')
        low = [t.lower() for t in todas]
        if len(set(low)) < len(low): probs.append('[erro] hashtag repetida')
        for t in todas:
            if re.search(r'[^#\w]', t) or len(t) > 30: probs.append(f'[erro] hashtag inválida ou longa demais: {t}')
        if not re.search(CTA, corpo.lower()): probs.append('[alerta] sem chamada para ação clara')
        if contar_emojis(corpo) > d.get('max_emojis', 6): probs.append('[alerta] emojis demais para o tom pedido')
        # fatos a confirmar: números, datas, horários, preços, @, locais com maiúscula depois de "no/na/em"
        fatos = set(re.findall(r'\b\d{1,2}[/.]\d{1,2}(?:[/.]\d{2,4})?\b|\b\d{1,2}h\d{0,2}\b|R\$ ?\d[\d.,]*|\b\d+%|\b\d{1,2} de ' + MESES + r'\b|@[\w.]+', corpo, re.I))
        fatos |= set(m.strip() for m in re.findall(r'\b(?:no|na|em|do|da)\s+((?:[A-ZÁÉÍÓÚÂÊÔÃÕÇ][\wáéíóúâêôãõç]+\s?){1,4})', corpo))
        fatos = {f if isinstance(f, str) else f[0] for f in fatos}
        pendentes = sorted(f for f in fatos if f and f.lower().strip() not in confirmados and not any(f.lower().strip() in c for c in confirmados))
        if pendentes: probs.append('[confirmar] fatos sem confirmação no briefing: ' + ', '.join(pendentes))
        for p in probs: print('  ' + p)
        if not probs: print('  ok')
        problemas_total += sum(1 for p in probs if p.startswith('[erro]'))
    print(f'\n{problemas_total} erro(s)')
    return problemas_total

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest='cmd', required=True)
    sp.add_parser('preparar')
    q = sp.add_parser('quadros'); q.add_argument('video'); q.add_argument('--n', type=int, default=12); q.add_argument('--saida', default='capa_trabalho')
    c = sp.add_parser('capa'); c.add_argument('video'); c.add_argument('--tempo', type=float, required=True); c.add_argument('--titulo', required=True)
    c.add_argument('--subtitulo', default=''); c.add_argument('--marca'); c.add_argument('--estilo', default='adesivo', choices=['adesivo', 'faixa', 'limpo'])
    c.add_argument('--posicao', default='auto', choices=['auto', 'alto', 'meio', 'baixo']); c.add_argument('--saida', default='capa_trabalho'); c.add_argument('--sem-realce', action='store_true')
    k = sp.add_parser('checar'); k.add_argument('arquivo')
    a = ap.parse_args()
    if a.cmd == 'preparar': preparar()
    elif a.cmd == 'quadros': quadros(a.video, a.n, a.saida)
    elif a.cmd == 'capa': capa(a.video, a.tempo, a.titulo, a.subtitulo, a.marca, a.estilo, a.posicao, a.saida, not a.sem_realce)
    elif a.cmd == 'checar': sys.exit(1 if checar(a.arquivo) else 0)

if __name__ == '__main__':
    main()
