# Formato da nota

Cada nota do lote vira um arquivo `trabalho/notas/<nome>.json`. O `ler_xml_nfe.py` gera esse formato sozinho; para notas lidas pela foto ou pela página da SEFAZ, escreva o JSON neste formato.

```json
{
  "origem": "foto",
  "arquivos": ["IMG_0412.jpg", "IMG_0413.jpg"],
  "fornecedor": {"nome": "Papelaria Beta", "razao_social": "Beta Comércio de Papéis Ltda", "cnpj": "12345678000190"},
  "numero": "88",
  "serie": "1",
  "data": "2026-10-06",
  "chave": "",
  "total": 95.00,
  "desconto": 5.00,
  "frete": 0,
  "outros": 0,
  "itens": [
    {"codigo": "", "ean": "", "descricao": "Caderno espiral 96 folhas", "unidade": "UN",
     "qtd": 4, "valor_unit": 8.00, "valor_total": 32.00, "desconto": 0},
    {"codigo": "", "descricao": "Kit 6 marca texto pastel", "qtd": 3, "valor_unit": 15.00,
     "valor_total": 45.00, "fator": 6},
    {"codigo": "", "descricao": "Sacola kraft", "qtd": 1, "valor_unit": 23.00, "valor_total": 23.00,
     "tipo": "despesa"}
  ]
}
```

## Campos

| Campo | Obrigatório | Observação |
|---|---|---|
| `origem` | sim | `xml`, `qrcode` (página da SEFAZ), `foto` ou `sem_nota` |
| `arquivos` | sim | fotos ou arquivos de onde a nota saiu (uma nota pode ter várias fotos) |
| `fornecedor.nome` | sim | nome fantasia, como a pessoa chama a loja |
| `fornecedor.cnpj` | se houver | só números |
| `numero`, `serie` | se houver | número da nota ou do cupom (COO/CCF em cupom antigo) |
| `data` | sim | AAAA-MM-DD |
| `chave` | se houver | 44 dígitos; valide com `ler_qrcode.py --chave` |
| `total` | sim | valor total impresso na nota |
| `desconto`, `frete`, `outros` | se houver | só o que é da nota inteira e **não** está nos itens |
| `itens[].qtd`, `valor_unit`, `valor_total` | sim | como impresso; o script confere qtd × unitário |
| `itens[].desconto`, `frete`, `outros` | se houver | valores do próprio item |
| `itens[].fator` | quando for kit | unidades por kit, se a pessoa vende avulso (a skill pergunta) |
| `itens[].tipo` | quando não for revenda | `despesa` para embalagens, material de uso interno etc. |
| `itens[].descricao_original` | opcional | texto da nota quando você limpou a descrição |
| `liberada` | opcional | `true` quando a pessoa mandou lançar mesmo com divergência |

## Configuração (`trabalho/config.json`)

```json
{"markup": 2.0, "arredondar": true, "precos": [3, 4, 5, 6, 8, 10, 12, 15, 18, 20, 25, 30],
 "ratear_desconto": true, "ratear_frete": true, "tolerancia": 0.05}
```

- `markup`: preço sugerido = custo unitário × markup.
- `arredondar` e `precos`: arredonda para cima até o próximo preço da lista (acima do último, para a dezena seguinte).
- `ratear_desconto` / `ratear_frete`: espalha o desconto e o frete da nota nos itens, na proporção do valor de cada um, para o custo refletir o que foi pago.
- `tolerancia`: diferença máxima aceita entre a soma dos itens e o total impresso, em reais.

Se a planilha da pessoa tiver uma aba **Config**, leia os valores de lá e grave este arquivo antes de rodar o script.
