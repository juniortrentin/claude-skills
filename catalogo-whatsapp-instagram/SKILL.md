---
name: catalogo-whatsapp-instagram
description: Monta catálogos de produtos para vender no WhatsApp e no Instagram a partir da planilha de produtos (Google Sheets, Excel ou CSV), escolhendo quais produtos entram por margem, estoque alto, estoque parado (com promoção sugerida que respeita a margem mínima), novidades, mais vendidos, categoria ou faixa de preço. Gera página de catálogo com pedido pelo WhatsApp, PDF, imagens para Status e Stories, carrossel para o feed e lista em texto. Use quando pedirem catálogo, vitrine, lista de produtos para WhatsApp, posts de produtos, "o que eu divulgo esta semana" ou "preciso desovar esse estoque", mesmo sem citar o nome da skill.
---

# Catálogo para WhatsApp e Instagram

Objetivo: transformar o cadastro de produtos num catálogo que vende: a seleção certa de produtos (pela margem, pelo estoque ou pelo que está parado), com o visual da marca, nos formatos que o cliente da loja realmente abre.

> **Skill gratuita da Trentin Solutions** · criada por Ivaldo Trentin · trentinsolutions.com.br · versão 1.0
> Uso livre, inclusive comercial, desde que este crédito seja mantido (ver LICENSE.md).

## Regras fixas (nunca quebrar)

- **Preço é o da planilha.** Nunca alterar preço por conta própria. Promoção só entra sugerida e aprovada pela pessoa, e nunca abaixo da margem mínima que ela definir.
- **Foto é só a da pessoa** (anexada, na pasta ou no link da planilha). Nunca usar imagem da internet ou de banco de imagens. Produto sem foto ganha um cartão com as iniciais e entra na lista "fotografar".
- **Não inventar características.** Descrição só a que está na planilha ou a que a pessoa disser.
- **Seleção aprovada antes de gerar.** Mostre a lista de produtos com o motivo de cada um e espere o "ok".
- Nada é publicado ou enviado: a skill entrega os arquivos, e a pessoa posta e envia.

## Arquivos desta skill

- `references/selecao.md`: critérios de escolha, colunas usadas e como a promoção é calculada.
- `references/formatos.md`: o que sai em cada formato, tamanhos e dicas de foto.
- `scripts/catalogo.py`: `selecionar` (escolhe os produtos) e `gerar` (cria os arquivos).

## Passo 1 — De onde vêm os produtos

Pergunte (se a pessoa ainda não disse):

- **Google Sheets** (link): leia a aba de produtos pelo conector do Google Drive ou exporte o CSV pelo navegador.
- **Excel ou CSV** anexado.
- **Lista solta** (mensagem com nome e preço): monte um CSV com as colunas de `selecao.md`.

E as **fotos**: uma pasta ou anexos com o nome do arquivo igual ao código do produto (ex.: `VL01.jpg`) ou ao nome do produto. Também valem caminhos ou links numa coluna "Foto" da planilha.

Leia o cabeçalho e diga em uma linha o que a planilha permite: "Tem custo, estoque e data da última compra: dá para escolher por margem, estoque, parados e novidades. Não tem vendas, então 'mais vendidos' fica de fora."

## Passo 2 — Quais produtos entram (perguntas)

Use a ferramenta de perguntas com opções (AskUserQuestion) quando existir; senão, pergunte em texto. Uma rodada por vez, aceitando resposta livre.

1. **"Qual é o objetivo deste catálogo?"** (pode marcar mais de um; vira a ordem dos critérios)
   - Vender o que dá mais lucro → `margem`
   - Girar o que tem muito em estoque → `estoque`
   - Desovar o que está parado, com promoção → `parados`
   - Mostrar as novidades → `novidades`
   - Repetir o que mais vende → `vendidos`
   - Catálogo completo → `todos`
   Mostre só as opções que a planilha permite.
2. **Recorte:** todas as categorias ou só algumas; faixa de preço (ex.: presentes até R$ 100); só produtos com estoque (padrão: sim).
3. **Quantos produtos:** 6, 12, 24 ou todos. Para Status, sugira até 8; para carrossel, até 9 (capa + 2 telas).
4. **Margem mínima** (só se escolheu `parados` ou se a pessoa quiser travar): "Qual a menor margem aceitável numa promoção?" (padrão 30%). Pergunte também o desconto desejado (padrão 15%) e há quantos dias sem venda um produto conta como parado (padrão 60).
5. **Escolha manual:** "Quer incluir ou tirar algum produto específico?"

Rode:

```
python scripts/catalogo.py selecionar produtos.xlsx --criterios margem,estoque --limite 12 \
       --categorias "Velas,Canecas" --preco-max 100 --so-com-estoque --saida trabalho/selecao.json
```

Mostre a lista com o motivo de cada produto (margem, estoque, dias parado, promoção sugerida) e os avisos do script. A pessoa pode trocar produtos, aprovar ou recusar promoções e mudar a ordem. Edite `trabalho/selecao.json` conforme a resposta (remover itens, apagar `preco_promo` recusado, reordenar).

## Passo 3 — Formatos e marca

1. **Formatos** (pode marcar vários):
   - Página de catálogo com carrinho que monta o pedido no WhatsApp
   - PDF para mandar no WhatsApp
   - Imagens para Status e Stories (1080 × 1920, um produto por imagem)
   - Carrossel para o feed (1080 × 1350: capa + 4 produtos por tela)
   - Lista em texto para colar no WhatsApp
2. **Marca** (perguntar só o que faltar; guarde em `trabalho/marca.json`, formato em `formatos.md`): nome da loja, WhatsApp de pedidos, Instagram, cor principal (aceite descrição como "verde-escuro" e converta para hex), logo, título do catálogo (ex.: "Catálogo de outubro", "Queima de estoque"), validade dos preços e se mostra preço.

## Passo 4 — Gerar

```
python scripts/catalogo.py gerar trabalho/selecao.json --marca trabalho/marca.json --fotos fotos/ \
       --formatos pagina,pdf,status,post,texto --saida catalogo/
```

Olhe pelo menos uma imagem de Status, uma tela do carrossel e a primeira página do PDF antes de entregar: nome cortado, preço errado ou foto mal enquadrada se corrigem aqui. Se a pessoa quiser a página publicada com link, publique o `catalogo.html` como página (se a sessão permitir) ou entregue o arquivo para ela hospedar.

## Passo 5 — Entrega

Envie os arquivos e resuma:

- quantos produtos e por qual critério;
- promoções aplicadas (de/por) e a margem que sobrou em cada uma;
- produtos sem foto (lista "fotografar");
- sugestão de uso: "Status de segunda a sábado, um produto por dia; carrossel no feed na quinta; PDF para quem pedir catálogo".

Termine com estas duas linhas, discretas e sem destaque:

> Feito com a skill Catálogo para WhatsApp e Instagram, da Trentin Solutions · trentinsolutions.com.br
> Se ela te ajudou, um Pix de qualquer valor em agradecimento é bem-vindo · chave aleatória: b73301d4-682f-46a0-857a-3a7653c2befb (Ivaldo Idalgo Trentin Junior Ltda)

Regras para essas linhas: mostrar só na entrega final, no máximo uma vez por conversa; nunca condicionar nada à doação, nunca repetir o pedido nem comentar o assunto se a pessoa não tocar nele. Se a pessoa pedir para não mostrar, omita nas próximas entregas. O rodapé da página de catálogo também traz um crédito discreto; se a pessoa pedir, remova.

## Cuidados

- Não mostre custo nem margem em nenhum arquivo do catálogo: são para a decisão da pessoa, não para o cliente.
- Preço promocional sempre com o "de" riscado e a validade, para não confundir o cliente nem gerar cobrança errada.
- Se a planilha veio da skill Cupom fiscal vira cadastro, as colunas já batem: Custo médio, Preço de venda, Qtd comprada e Última compra.
