#!/usr/bin/env python3
"""Converte XML de NF-e ou NFC-e no formato de nota da skill (references/formato.md).

Trentin Solutions · criada por Ivaldo Trentin · trentinsolutions.com.br
Uso livre, mantendo este crédito (ver LICENSE.md).

Uso:
  python ler_xml_nfe.py nota1.xml [nota2.xml ...] --saida trabalho/notas
Cada XML vira trabalho/notas/<chave>.json.
"""
import argparse
import json
import os
import sys
import xml.etree.ElementTree as ET

NS = "{http://www.portalfiscal.inf.br/nfe}"


def txt(el, path, default=""):
    if el is None:
        return default
    found = el.find("/".join(NS + p for p in path.split("/")))
    return found.text.strip() if found is not None and found.text else default


def num(el, path):
    v = txt(el, path, "0")
    try:
        return round(float(v), 6)
    except ValueError:
        return 0.0


def ler(caminho):
    root = ET.parse(caminho).getroot()
    inf = root.find(f".//{NS}infNFe")
    if inf is None:
        raise ValueError("não parece um XML de NF-e/NFC-e (infNFe ausente)")
    chave = (inf.get("Id") or "").replace("NFe", "")
    ide, emit = inf.find(NS + "ide"), inf.find(NS + "emit")
    tot = inf.find(f"{NS}total/{NS}ICMSTot")
    data = (txt(ide, "dhEmi") or txt(ide, "dEmi"))[:10]
    modelo = txt(ide, "mod")
    itens = []
    for det in inf.findall(NS + "det"):
        p = det.find(NS + "prod")
        ean = txt(p, "cEAN")
        itens.append({
            "codigo": txt(p, "cProd"),
            "ean": "" if ean.upper() in ("", "SEM GTIN") else ean,
            "descricao": txt(p, "xProd"),
            "ncm": txt(p, "NCM"),
            "unidade": txt(p, "uCom"),
            "qtd": num(p, "qCom"),
            "valor_unit": num(p, "vUnCom"),
            "valor_total": num(p, "vProd"),
            "desconto": num(p, "vDesc"),
            "frete": num(p, "vFrete") + num(p, "vSeg"),
            "outros": num(p, "vOutro"),
        })
    soma = lambda k: round(sum(i[k] for i in itens), 2)
    nota = {
        "origem": "xml",
        "modelo": {"55": "NF-e", "65": "NFC-e"}.get(modelo, modelo),
        "arquivos": [os.path.basename(caminho)],
        "fornecedor": {"nome": txt(emit, "xFant") or txt(emit, "xNome"), "razao_social": txt(emit, "xNome"),
                       "cnpj": txt(emit, "CNPJ") or txt(emit, "CPF")},
        "numero": txt(ide, "nNF"),
        "serie": txt(ide, "serie"),
        "data": data,
        "chave": chave,
        "total": num(tot, "vNF"),
        # o que já está nos itens não entra de novo no nível da nota
        "desconto": round(max(0.0, num(tot, "vDesc") - soma("desconto")), 2),
        "frete": round(max(0.0, num(tot, "vFrete") + num(tot, "vSeg") - soma("frete")), 2),
        "outros": round(max(0.0, num(tot, "vOutro") - soma("outros")), 2),
        "itens": itens,
    }
    return nota


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("xmls", nargs="+")
    ap.add_argument("--saida", default="trabalho/notas")
    a = ap.parse_args()
    os.makedirs(a.saida, exist_ok=True)
    ok = 0
    for x in a.xmls:
        try:
            n = ler(x)
        except Exception as e:  # noqa: BLE001
            print(f"ERRO {x}: {e}", file=sys.stderr)
            continue
        nome = (n["chave"] or os.path.splitext(os.path.basename(x))[0]) + ".json"
        with open(os.path.join(a.saida, nome), "w", encoding="utf-8") as f:
            json.dump(n, f, ensure_ascii=False, indent=2)
        ok += 1
        print(f"{n['fornecedor']['nome']} · nota {n['numero']} · {n['data']} · {len(n['itens'])} itens · R$ {n['total']:.2f} -> {nome}")
    print(f"{ok} de {len(a.xmls)} XML convertidos")


if __name__ == "__main__":
    main()
