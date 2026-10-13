#!/usr/bin/env python3
"""Mescla as conexões novas na planilha mestre, calcula a aderência ao perfil ideal e grava a planilha.

Trentin Solutions · criada por Ivaldo Trentin · trentinsolutions.com.br
Uso livre, mantendo este crédito (ver LICENSE.md).

Uso:
  python planilha_conexoes.py novos trabalho/conexoes.jsonl --mestre conexoes.xlsx
      Lista quais URLs do lote ainda não estão na planilha mestre (para saber onde parar).
  python planilha_conexoes.py gravar trabalho/conexoes.jsonl --perfil trabalho/perfil.json \
      [--mestre conexoes.xlsx] --saida conexoes.xlsx
      Acrescenta as novas no topo, preenche vazios de quem já existia, calcula a aderência e grava.

Formato de cada linha do .jsonl em references/campos.md.
"""
import argparse
import csv
import json
import os
import re
import sys
import unicodedata
from datetime import date, datetime

COLUNAS = ["Aderência", "Nota", "Nome", "Cargo", "Empresa", "Setor", "Nº de colaboradores", "Localização",
           "E-mail", "Fonte do e-mail", "Telefone", "Fonte do telefone", "Confiança", "Créditos gastos",
           "Data da conexão", "Data da consulta", "LinkedIn", "Motivo da nota", "Mensagem sugerida", "Observação"]
CHAVES = ["aderencia", "nota", "nome", "cargo", "empresa", "setor", "colaboradores", "localizacao", "email",
          "fonte_email", "telefone", "fonte_telefone", "confianca", "creditos", "data_conexao", "data_consulta",
          "url", "motivo", "mensagem", "observacao"]
DECISORES = ["socio", "socia", "fundador", "fundadora", "founder", "owner", "dono", "dona", "ceo", "cfo", "coo", "cto",
             "cmo", "diretor", "diretora", "director", "presidente", "head", "vp", "vice presidente", "gerente",
             "manager", "proprietario", "proprietaria", "empresario", "empresaria"]


def norm(s):
    s = unicodedata.normalize("NFD", str(s or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", s)).strip()


def url_chave(u):
    u = str(u or "").strip().lower().split("?")[0].rstrip("/")
    m = re.search(r"linkedin\.com/in/([^/]+)", u)
    return "in/" + m.group(1) if m else u


def ler_jsonl(caminho):
    out = []
    with open(caminho, encoding="utf-8") as f:
        for n, l in enumerate(f, 1):
            l = l.strip()
            if l:
                try:
                    out.append(json.loads(l))
                except json.JSONDecodeError as e:
                    print(f"Aviso: linha {n} ignorada ({e})", file=sys.stderr)
    return out


def ler_mestre(caminho):
    if not caminho or not os.path.exists(caminho):
        return []
    if caminho.lower().endswith((".xlsx", ".xlsm")):
        from openpyxl import load_workbook
        wb = load_workbook(caminho, data_only=True)
        ws = wb["Conexões"] if "Conexões" in wb.sheetnames else wb.active
        linhas = [list(r) for r in ws.iter_rows(values_only=True)]
    else:
        with open(caminho, encoding="utf-8-sig") as f:
            linhas = list(csv.reader(f))
    if not linhas:
        return []
    cab = [norm(c) for c in linhas[0]]
    idx = {}
    for chave, col in zip(CHAVES, COLUNAS):
        n = norm(col)
        if n in cab:
            idx[chave] = cab.index(n)
    if "url" not in idx:
        for i, c in enumerate(cab):
            if "linkedin" in c or c in ("url", "perfil"):
                idx["url"] = i
    regs = []
    for r in linhas[1:]:
        d = {k: (r[i] if i < len(r) else None) for k, i in idx.items()}
        if d.get("url"):
            for k, v in d.items():
                if isinstance(v, datetime):
                    d[k] = v.date().isoformat()
                elif isinstance(v, date):
                    d[k] = v.isoformat()
            regs.append(d)
    return regs


def faixa_porte(n):
    try:
        n = int(re.sub(r"\D", "", str(n)) or 0)
    except ValueError:
        return ""
    if not n:
        return ""
    return "1-10" if n <= 10 else "11-50" if n <= 50 else "51-200" if n <= 200 else "201-1000" if n <= 1000 else "1000+"


def pontuar(c, perfil):
    """Aderência ao perfil ideal: cargo 40 + setor 25 + porte 20 + região 15. Sem perfil, só o cargo pesa."""
    motivos, nota = [], 0
    cargo = norm(c.get("cargo"))
    alvo = [norm(x) for x in perfil.get("cargos", [])] or DECISORES
    if cargo and any(a and a in cargo for a in alvo):
        nota += 40
        motivos.append("cargo de decisão" if not perfil.get("cargos") else "cargo-alvo")
    elif cargo and any(d in cargo for d in DECISORES):
        nota += 20
        motivos.append("cargo de gestão")
    setores = [norm(x) for x in perfil.get("setores", [])]
    setor = norm(c.get("setor")) + " " + norm(c.get("empresa"))
    if setores and any(s and s in setor for s in setores):
        nota += 25
        motivos.append("setor-alvo")
    elif not setores:
        nota += 12
    portes = perfil.get("portes", [])
    fp = faixa_porte(c.get("colaboradores"))
    if portes and fp in portes:
        nota += 20
        motivos.append(f"porte {fp}")
    elif not portes and fp:
        nota += 10
    regioes = [norm(x) for x in perfil.get("regioes", [])]
    loc = norm(c.get("localizacao"))
    if regioes and any(r and r in loc for r in regioes):
        nota += 15
        motivos.append("região-alvo")
    elif not regioes:
        nota += 7
    nota = min(100, nota)
    c["nota"] = nota
    c["aderencia"] = "Alta" if nota >= 70 else "Média" if nota >= 45 else "Baixa"
    c["motivo"] = ", ".join(motivos) or "sem sinais do perfil ideal"
    return c


def mesclar(antigo, novo):
    """Nunca apaga dado antigo: só preenche vazios, atualiza cargo/empresa/data da consulta e soma créditos."""
    def num(v):
        try:
            return float(v or 0)
        except (TypeError, ValueError):
            return 0.0
    creditos = num(antigo.get("creditos")) + num(novo.get("creditos"))
    for k, v in novo.items():
        if k == "creditos" or v in (None, ""):
            continue
        if antigo.get(k) in (None, "") or k in ("data_consulta", "cargo", "empresa"):
            antigo[k] = v
    antigo["creditos"] = creditos or ""
    return antigo


def cmd_novos(a):
    lote = ler_jsonl(a.lote)
    ja = {url_chave(r.get("url")) for r in ler_mestre(a.mestre)}
    novos = [c for c in lote if url_chave(c.get("url")) not in ja]
    print(f"{len(lote)} no lote · {len(novos)} novas · {len(lote) - len(novos)} já estavam na planilha")
    for c in novos:
        print(f"  {c.get('nome', '')} · {c.get('cargo', '')} · {c.get('url', '')}")


def cmd_gravar(a):
    perfil = {}
    if a.perfil and os.path.exists(a.perfil):
        with open(a.perfil, encoding="utf-8") as f:
            perfil = json.load(f)
    mestre = ler_mestre(a.mestre)
    por_url = {url_chave(r.get("url")): r for r in mestre}
    ordem_antiga = [url_chave(r.get("url")) for r in mestre]
    novos_ordem = []
    hoje = date.today().isoformat()
    for c in ler_jsonl(a.lote):
        k = url_chave(c.get("url"))
        if not k:
            continue
        c.setdefault("data_consulta", hoje)
        if k in por_url:
            mesclar(por_url[k], c)
        else:
            por_url[k] = c
            novos_ordem.append(k)
    regs = [pontuar(por_url[k], perfil) for k in novos_ordem + ordem_antiga]
    gravar(regs, a.saida, perfil)
    altas = sum(1 for r in regs[:len(novos_ordem)] if r["aderencia"] == "Alta")
    print(f"{len(novos_ordem)} conexões novas · {len(ordem_antiga)} já existiam · {len(regs)} na planilha · {altas} novas com aderência alta -> {a.saida}")
    for r in sorted(regs[:len(novos_ordem)], key=lambda x: -x["nota"])[:5]:
        print(f"  {r['nota']:>3} {r['aderencia']:<5} {r.get('nome', '')} · {r.get('cargo', '')} · {r.get('empresa', '')}")


def gravar(regs, saida, perfil):
    if not saida.lower().endswith(".xlsx"):
        with open(saida, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(COLUNAS)
            for r in regs:
                w.writerow([r.get(k, "") for k in CHAVES])
        return
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    azul = PatternFill("solid", fgColor="3A6AB4")
    branco = Font(bold=True, color="FFFFFF", name="Arial")
    corpo = Font(name="Arial", size=10)
    cores = {"Alta": "D8F3E6", "Média": "FCEFD6", "Baixa": "ECEFF4"}
    wb = Workbook()
    wb.properties.creator = "Trentin Solutions · Conexões do LinkedIn com contexto"
    wb.properties.description = "Gerada pela skill gratuita Conexões do LinkedIn com contexto, da Trentin Solutions (trentinsolutions.com.br)."
    ws = wb.active
    ws.title = "Conexões"
    ws.append(COLUNAS)
    for r in regs:
        linha = []
        for k in CHAVES:
            v = r.get(k, "")
            if k in ("data_conexao", "data_consulta") and v:
                try:
                    v = date.fromisoformat(str(v)[:10])
                except ValueError:
                    pass
            linha.append(v)
        ws.append(linha)
    larg = [11, 7, 26, 30, 26, 20, 12, 22, 30, 14, 18, 14, 11, 10, 13, 13, 40, 30, 50, 36]
    for i, w_ in enumerate(larg, 1):
        ws.column_dimensions[get_column_letter(i)].width = w_
    for c in ws[1]:
        c.fill, c.font = azul, branco
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.font = corpo
            c.alignment = Alignment(vertical="top", wrap_text=c.column in (18, 19, 20))
        row[0].fill = PatternFill("solid", fgColor=cores.get(row[0].value, "FFFFFF"))
        row[0].font = Font(name="Arial", size=10, bold=True)
        for j in (14, 15):
            row[j].number_format = "DD/MM/YYYY"
        if row[16].value:
            row[16].hyperlink = row[16].value
            row[16].font = Font(name="Arial", size=10, color="3A6AB4", underline="single")
    ws.freeze_panes = "D2"
    ws.auto_filter.ref = ws.dimensions

    wr = wb.create_sheet("Resumo")
    wr.append(["Indicador", "Valor"])
    for c in wr[1]:
        c.fill, c.font = azul, branco
    total = len(regs)
    wr.append(["Conexões na planilha", total])
    for f in ("Alta", "Média", "Baixa"):
        wr.append([f"Aderência {f.lower()}", sum(1 for r in regs if r.get("aderencia") == f)])
    wr.append(["Com e-mail", sum(1 for r in regs if r.get("email"))])
    wr.append(["Com telefone", sum(1 for r in regs if r.get("telefone"))])
    wr.append(["Créditos gastos (total)", sum(float(r.get("creditos") or 0) for r in regs)])
    wr.append([])
    wr.append(["Empresas com mais conexões", ""])
    cont = {}
    for r in regs:
        if r.get("empresa"):
            cont[r["empresa"]] = cont.get(r["empresa"], 0) + 1
    for e, n in sorted(cont.items(), key=lambda x: -x[1])[:10]:
        wr.append([e, n])
    wr.column_dimensions["A"].width = 36
    wr.column_dimensions["B"].width = 14

    wp = wb.create_sheet("Perfil ideal")
    wp.append(["Critério", "Valores"])
    for c in wp[1]:
        c.fill, c.font = azul, branco
    for k, nome in (("cargos", "Cargos-alvo"), ("setores", "Setores"), ("portes", "Porte (colaboradores)"), ("regioes", "Regiões")):
        wp.append([nome, ", ".join(perfil.get(k, [])) or "(não definido)"])
    wp.append([])
    wp.append(["Nota", "cargo até 40 + setor até 25 + porte até 20 + região até 15. Alta ≥ 70, Média ≥ 45."])
    wp.column_dimensions["A"].width = 24
    wp.column_dimensions["B"].width = 90

    wc = wb.create_sheet("Como usar")
    for t in ["Conexões do LinkedIn com contexto · trentinsolutions.com.br", "",
              "Uma linha por pessoa; a chave é a URL do LinkedIn. Novas conexões entram no topo.",
              "Aderência: quanto a pessoa se parece com o seu cliente ideal (aba Perfil ideal).",
              "Fonte do e-mail/telefone: LinkedIn (informado pela pessoa), Apollo, site da empresa ou CNPJ.",
              "Confiança: Alta = nome + empresa batem; Média = nome + cidade/área; Baixa = só o nome (contato não revelado).",
              "Mensagem sugerida é só um rascunho. A skill nunca envia nada.",
              "LGPD: prospecção B2B por legítimo interesse. Remova quem pedir para sair.", "",
              "Skill gratuita da Trentin Solutions, criada por Ivaldo Trentin · trentinsolutions.com.br",
              "Esta planilha te ajudou? Um Pix de qualquer valor em agradecimento é bem-vindo.",
              "Chave Pix aleatória: b73301d4-682f-46a0-857a-3a7653c2befb · Ivaldo Idalgo Trentin Junior Ltda"]:
        wc.append([t])
    wc["A1"].font = Font(name="Arial", size=13, bold=True, color="3A6AB4")
    wc.column_dimensions["A"].width = 110
    wb.save(saida)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s1 = sub.add_parser("novos")
    s1.add_argument("lote")
    s1.add_argument("--mestre")
    s2 = sub.add_parser("gravar")
    s2.add_argument("lote")
    s2.add_argument("--perfil")
    s2.add_argument("--mestre")
    s2.add_argument("--saida", default="conexoes_linkedin.xlsx")
    a = ap.parse_args()
    {"novos": cmd_novos, "gravar": cmd_gravar}[a.cmd](a)


if __name__ == "__main__":
    main()
