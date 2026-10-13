# Formatos

## Uma conexão por linha em `trabalho/conexoes.jsonl`

```json
{"nome": "Ana Exemplo", "cargo": "Sócia-fundadora", "empresa": "Clínica Viva Bem", "setor": "Saúde e estética",
 "colaboradores": "18", "localizacao": "Curitiba, PR", "email": "ana@vivabem.com.br", "fonte_email": "LinkedIn",
 "telefone": "", "fonte_telefone": "", "confianca": "Alta", "creditos": 0, "data_conexao": "2026-10-08",
 "url": "https://www.linkedin.com/in/ana-exemplo/", "mensagem": "", "observacao": ""}
```

- `url` é obrigatório e é a chave única.
- `fonte_email` / `fonte_telefone`: `LinkedIn`, `Apollo`, `Apollo: sem e-mail`, `site (comercial da empresa)`, `CNPJ` ou `Não encontrado`.
- `confianca`: `Alta`, `Média` ou `Baixa` (tabela em `fontes.md`).
- `creditos`: créditos do Apollo gastos com a pessoa nesta rodada (o script soma com os anteriores).
- Datas no formato AAAA-MM-DD.

## Cliente ideal em `trabalho/perfil.json`

```json
{"cargos": ["dono", "sócio", "fundador", "diretor comercial"],
 "setores": ["saúde", "estética", "varejo"],
 "portes": ["11-50", "51-200"],
 "regioes": ["PR", "SP", "Curitiba"]}
```

Portes aceitos: `1-10`, `11-50`, `51-200`, `201-1000`, `1000+`. Todos os campos são opcionais.

## Nota de aderência (0 a 100)

| Parte | Pontos | Quando |
|---|---|---|
| Cargo | 40 | cargo contém um dos cargos-alvo (ou, sem perfil, um cargo de decisão) |
| | 20 | cargo de gestão, mas fora da lista |
| Setor | 25 | setor ou nome da empresa contém um setor-alvo (12 se não houver setores definidos) |
| Porte | 20 | número de colaboradores na faixa escolhida (10 se não houver portes definidos) |
| Região | 15 | localização contém uma região-alvo (7 se não houver regiões definidas) |

Faixas: **Alta** ≥ 70 · **Média** ≥ 45 · **Baixa** abaixo disso.

## Colunas da aba Conexões

Aderência · Nota · Nome · Cargo · Empresa · Setor · Nº de colaboradores · Localização · E-mail · Fonte do e-mail · Telefone · Fonte do telefone · Confiança · Créditos gastos · Data da conexão · Data da consulta · LinkedIn · Motivo da nota · Mensagem sugerida · Observação

Novas conexões entram no topo. Dados antigos nunca são apagados: uma rodada nova só preenche vazios e atualiza cargo, empresa e data da consulta.
