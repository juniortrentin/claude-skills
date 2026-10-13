#!/usr/bin/env python3
"""Lê o QR code de fotos de cupons e notas e extrai o link da SEFAZ e a chave de acesso.

Trentin Solutions · criada por Ivaldo Trentin · trentinsolutions.com.br
Uso livre, mantendo este crédito (ver LICENSE.md).

Uso:
  python ler_qrcode.py foto1.jpg foto2.png ... [--json trabalho/qrcodes.json]
  python ler_qrcode.py --chave "3526 1012 3456 ..."   (só valida uma chave digitada)

Precisa de opencv (pip install opencv-python-headless). Sem ele, o script avisa e
a leitura do QR fica a cargo do Claude olhando a foto.
"""
import argparse
import json
import re
import sys


def dv_chave(c43):
    pesos, soma = 2, 0
    for d in reversed(c43):
        soma += int(d) * pesos
        pesos = 2 if pesos == 9 else pesos + 1
    r = soma % 11
    return 0 if r < 2 else 11 - r


def chave_valida(ch):
    ch = re.sub(r"\D", "", ch or "")
    return len(ch) == 44 and dv_chave(ch[:43]) == int(ch[43])


def extrair_chave(texto):
    for m in re.finditer(r"\d{44}", re.sub(r"[\s.]", "", texto or "")):
        if chave_valida(m.group()):
            return m.group()
    return ""


def descrever(ch):
    """UF, ano-mês, CNPJ do emitente, modelo, série e número a partir da chave."""
    ufs = {"11": "RO", "12": "AC", "13": "AM", "14": "RR", "15": "PA", "16": "AP", "17": "TO", "21": "MA",
           "22": "PI", "23": "CE", "24": "RN", "25": "PB", "26": "PE", "27": "AL", "28": "SE", "29": "BA",
           "31": "MG", "32": "ES", "33": "RJ", "35": "SP", "41": "PR", "42": "SC", "43": "RS", "50": "MS",
           "51": "MT", "52": "GO", "53": "DF"}
    return {"uf": ufs.get(ch[:2], ch[:2]), "ano_mes": f"20{ch[2:4]}-{ch[4:6]}", "cnpj": ch[6:20],
            "modelo": {"55": "NF-e", "65": "NFC-e"}.get(ch[20:22], ch[20:22]),
            "serie": str(int(ch[22:25])), "numero": str(int(ch[25:34]))}


def decodificar(caminho):
    try:
        import cv2
    except ImportError:
        return None, "opencv ausente"
    img = cv2.imread(caminho)
    if img is None:
        return [], "arquivo não abriu como imagem"
    detectores = [cv2.QRCodeDetector()]
    if hasattr(cv2, "QRCodeDetectorAruco"):  # lê QR que o detector padrão às vezes perde
        detectores.append(cv2.QRCodeDetectorAruco())
    tentativas = [img]
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    tentativas += [cinza, cv2.adaptiveThreshold(cinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 10)]
    h, w = cinza.shape
    if max(h, w) > 2000:
        f = 1600 / max(h, w)
        tentativas.append(cv2.resize(cinza, None, fx=f, fy=f))
    elif max(h, w) < 900:
        tentativas.append(cv2.resize(cinza, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC))
    achados = []
    for det in detectores:
        for t in tentativas:
            try:
                ok, textos, _, _ = det.detectAndDecodeMulti(t)
                if ok:
                    achados += [x for x in textos if x]
                if not achados:
                    texto, _, _ = det.detectAndDecode(t)
                    if texto:
                        achados.append(texto)
            except cv2.error:
                pass
            if achados:
                return list(dict.fromkeys(achados)), ""
    return [], ""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fotos", nargs="*")
    ap.add_argument("--json", help="grava o resultado neste arquivo")
    ap.add_argument("--chave", help="valida uma chave de 44 dígitos digitada")
    a = ap.parse_args()

    if a.chave:
        ch = re.sub(r"\D", "", a.chave)
        if chave_valida(ch):
            print("chave válida:", ch, json.dumps(descrever(ch), ensure_ascii=False))
        else:
            print("chave INVÁLIDA (dígito verificador não confere ou não tem 44 dígitos):", ch)
        return

    saida = []
    for foto in a.fotos:
        textos, erro = decodificar(foto)
        if textos is None:
            print("opencv não instalado: rode `pip install opencv-python-headless` ou leia o QR olhando a foto.", file=sys.stderr)
            sys.exit(2)
        if not textos:
            print(f"{foto}: nenhum QR lido{(' (' + erro + ')') if erro else ''} -> ler a nota pela foto")
            saida.append({"foto": foto, "qr": "", "chave": "", "url": ""})
            continue
        for t in textos:
            ch = extrair_chave(t)
            info = descrever(ch) if ch else {}
            url = t if t.lower().startswith("http") else ""
            print(f"{foto}: {'chave ' + ch if ch else 'QR sem chave de acesso'} {json.dumps(info, ensure_ascii=False) if info else ''}")
            saida.append({"foto": foto, "qr": t, "chave": ch, "url": url, **info})
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(saida, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
