# Seleção de produtos

## Colunas que o script reconhece

O script lê o cabeçalho e reconhece os nomes mais comuns (sem diferenciar maiúsculas e acentos). Só **Produto** e **Preço** são obrigatórias.

| Dado | Nomes aceitos |
|---|---|
| Código | código, cod, sku, referência |
| Produto | produto, nome, item, título |
| Descrição | descrição, detalhes |
| Categoria | categoria, tipo, seção, linha |
| Preço | preço de venda, preço, valor de venda |
| Preço promocional | preço promocional, promoção |
| Custo | custo médio, custo unit., custo, preço de custo |
| Estoque | estoque atual, estoque, saldo, qtd em estoque |
| Vendidos | qtd vendida, vendidos, vendas |
| Última venda | última venda |
| Última compra | última compra, última entrada, data de entrada |
| Foto | foto, imagem, URL da imagem, link da foto |
| Status | status, situação (inativo, fora de linha e descontinuado ficam de fora) |

## Critérios

Os critérios combinam na ordem em que são passados: `--criterios margem,estoque` ordena pela margem e desempata pelo estoque.

| Critério | Precisa de | Ordena por |
|---|---|---|
| `margem` | custo | (preço − custo) ÷ preço, do maior para o menor |
| `estoque` | estoque | unidades em estoque, do maior para o menor |
| `parados` | estoque + última venda ou última compra | primeiro os parados há mais de `--dias-parado` dias, com mais dinheiro empatado (estoque × custo) |
| `novidades` | última compra | data da última compra, da mais recente |
| `vendidos` | vendidos | quantidade vendida |
| `todos` | — | ordem da planilha |

Filtros: `--categorias`, `--preco-min`, `--preco-max`, `--codigos` (escolha manual), `--so-com-estoque`, `--margem-min`.

## Promoção sugerida (critério `parados`)

Para cada produto parado sem preço promocional na planilha:

1. alvo = preço × (1 − desconto), com desconto padrão de 15% (`--desconto 0.15`);
2. piso = custo ÷ (1 − margem mínima), com margem mínima padrão de 20% ou a de `--margem-min`;
3. o preço final é o maior entre alvo e piso, arredondado para um final comum (R$ 37,90; R$ 8,90);
4. se não sobra desconto acima do piso, o produto entra sem promoção e com o aviso "sem espaço para desconto".

Exemplo: caneca a R$ 45,00 com custo de R$ 22,00, desconto de 15% e margem mínima de 40%. O alvo é R$ 38,25 e o piso, R$ 36,67, então a promoção sugerida fica em **R$ 37,90**, com margem de 42%.

A promoção é sempre **sugerida**: mostre na prévia e aplique só o que a pessoa aprovar.
