# Gravar nas planilhas

## Planilha nova

`python scripts/lancar.py planilha trabalho/proposta.json --saida estoque.xlsx` cria a planilha modelo já preenchida:

| Aba | O que tem |
|---|---|
| Produtos | Código, Produto, EAN, Fornecedor, Unidade, **Custo médio** (fórmula), Preço de venda, **Markup** (fórmula), **Qtd comprada** (fórmula), **Última compra** (fórmula), Status, Observações |
| Compras | uma linha por item: ID compra, Data, Fornecedor, Nº nota, Código, Produto, Qtd, Custo unit., **Custo total** (fórmula), Chave de acesso, Origem, Observações |
| Fornecedores | CNPJ, nome, razão social, primeira compra |
| Despesas | itens que não são revenda |
| Conferência | cada nota: soma dos itens, desconto, frete, total impresso, diferença e status |
| Config | markup, arredondamento, rateio e tolerância usados |
| Como usar | explicação das abas |

O custo médio é ponderado: soma de todos os custos do produto ÷ soma das quantidades compradas.

Se a pessoa quer a planilha nova **no Google Sheets**: gere o .xlsx e importe pelo conector do Google Drive (criar arquivo convertendo para planilha Google). Sem conector, entregue o .xlsx e diga para abrir no Google Drive com "Abrir com Planilhas Google".

## Excel existente

1. Peça o arquivo. Trabalhe numa **cópia**; a original nunca é alterada.
2. Se a planilha estiver no formato modelo (veio desta skill), rode `lancar.py planilha ... --base original.xlsx --saida original_atualizada.xlsx`.
3. Se a estrutura for outra, faça o **mapa de colunas** (abaixo) e acrescente as linhas com openpyxl, usando os CSV que o script gera em `csv/`. Devolva o arquivo atualizado.

## Google Sheets existente (link)

1. Peça o link e confirme que a pessoa tem permissão de edição.
2. **Leitura:** use o conector do Google Drive (exportar como .xlsx ou CSV). Sem conector, abra no navegador e use a exportação CSV pública da aba:
   `https://docs.google.com/spreadsheets/d/<ID>/gviz/tq?tqx=out:csv&headers=1&sheet=<Aba>`
   Use sempre `headers=1`; sem isso a primeira linha some.
3. Rode `lancar.py casar` com `--catalogo produtos.csv --compras compras.csv` exportados da planilha.
4. **Escrita, nesta ordem de preferência:**
   - conector do Google Drive ou Sheets, se ele permitir acrescentar linhas;
   - navegador: vá até a primeira linha vazia da aba (caixa de nome, canto superior esquerdo), selecione a primeira coluna que recebe dado e cole as linhas como texto separado por tabulação. Cole em blocos que pulem as colunas de fórmula;
   - sem nenhum dos dois: entregue os CSV e explique como colar.
5. Outras pessoas podem estar editando ao mesmo tempo. Nunca desfaça mudanças que não foram suas.

## Mapa de colunas (planilha com estrutura própria)

Antes de gravar, leia o cabeçalho das abas e monte o mapa, por exemplo:

| Dado da skill | Coluna na planilha |
|---|---|
| Código | Produtos!A "Cód." |
| Preço de venda | Produtos!F "Preço" |
| Custo médio | Produtos!I (fórmula: não escrever) |

Mostre o mapa à pessoa na primeira vez e guarde-o numa aba **Config** ou numa nota da planilha, para não perguntar de novo.

Regras para planilhas existentes:

- **Nunca** escrever em célula com fórmula, nem apagar ou reordenar linhas.
- Acrescentar sempre depois da última linha preenchida; conferir a linha antes de colar.
- Seguir o padrão das últimas linhas: formato do ID da compra, formato da data, nomes de fornecedores já usados (e listas de validação, se houver).
- Códigos só com números: no Google Sheets, cole com apóstrofo (`'2305`) para não virarem número.
- Se uma aba tem limite de linhas nas fórmulas (ex.: fórmulas até a linha 1000), avise quando faltar menos de 10%.
