# Formatos

## `trabalho/config.json`

```json
{"imposto": 6, "gastos_fixos_mes": 4500, "vendas_mes": 30000, "lucro": 15, "guardar_mes": 2,
 "canal_padrao": "credito",
 "canais": {"pix": {"pct": 0, "fixo": 0}, "dinheiro": {"pct": 0, "fixo": 0},
            "debito": {"pct": 1.5, "fixo": 0}, "credito": {"pct": 3.5, "fixo": 0},
            "marketplace": {"pct": 18, "fixo": 5}},
 "degrau_dias": 15}
```

- Porcentagens em número (6 = 6%).
- `gastos_fixos_mes`: aluguel, luz, água, internet, salários e encargos, pró-labore, contador, sistema. MEI: some a guia mensal aqui e use `imposto` 0.
- `canais`: os nomes são livres ("shopee", "mercado livre", "ifood"). As taxas do exemplo são só ponto de partida: confira com a maquininha e com cada plataforma.
- `guardar_mes`: quanto custa manter o produto parado por mês (padrão 2%).

## `trabalho/produtos.csv`

Separador `;` ou `,`. Números com vírgula ou ponto. Datas em `AAAA-MM-DD` ou `DD/MM/AAAA`. Também aceita `.xlsx` (primeira aba, cabeçalho na linha 1) e `.jsonl`.

| Coluna | Obrigatória | O que é |
|---|---|---|
| nome | sim | nome do produto |
| categoria | não | para filtrar depois |
| tipo | não | `duravel` (padrão), `moda` ou `validade` |
| custo | sim | quanto pagou por unidade ao fornecedor |
| frete | não | frete por unidade |
| embalagem | não | embalagem por unidade |
| quantidade | para o estoque | quantas unidades tem agora |
| data_compra | para o estoque | data da compra ou da última entrada |
| vendidos_90d | para o estoque | quantas unidades vendeu nos últimos 3 meses |
| preco_atual | para o preço | preço de venda de hoje |
| canal | não | forma de venda principal (nome igual ao do config) |
| validade | se tipo = validade | data de validade do lote |

## De onde tirar cada coisa

- **Planilha de controle ou sistema:** exporte produtos, estoque e vendas; some as vendas dos últimos 90 dias por produto.
- **Skill Cupom fiscal vira cadastro:** a aba de compras traz data e custo de cada entrada.
- **Notas fiscais de compra:** custo unitário e data.
- **Nada disso:** pergunte produto por produto, começando pelos que a pessoa acha que estão parados. Estimativas são aceitas; marque na conversa quais foram.
