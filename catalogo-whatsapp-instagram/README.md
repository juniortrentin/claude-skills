# Catálogo para WhatsApp e Instagram

Uma skill para o Claude que transforma a sua planilha de produtos num catálogo que vende: escolhe os produtos certos e gera os arquivos com a cara da sua marca.

## Quais produtos entram

Você escolhe o objetivo, e a skill seleciona e explica cada escolha:

- **Mais lucro:** produtos com maior margem.
- **Girar estoque:** o que tem muito em estoque.
- **Desovar parados:** estoque sem venda há semanas, com preço promocional sugerido que nunca fica abaixo da sua margem mínima.
- **Novidades:** o que chegou por último.
- **Mais vendidos:** quando a planilha tem vendas.
- Além disso: categorias, faixa de preço e escolha manual.

## O que ela gera

- **Página de catálogo** com carrinho: o cliente monta o pedido e envia pelo WhatsApp com a lista e o total prontos.
- **PDF** para mandar no WhatsApp, com cada produto clicável.
- **Imagens para Status e Stories**, um produto por imagem.
- **Carrossel para o feed** do Instagram.
- **Lista em texto** para colar no WhatsApp.

## O que vem no pacote

```
catalogo-whatsapp-instagram/
├── SKILL.md                instruções que o Claude segue
├── README.md               este arquivo
├── LICENSE.md              uso livre, mantendo o crédito
├── references/
│   ├── selecao.md          critérios, colunas e cálculo da promoção
│   └── formatos.md         formatos, marca e dicas de foto
└── scripts/
    └── catalogo.py         seleciona os produtos e gera os arquivos
```

## Como instalar

1. Baixe o arquivo `catalogo-whatsapp-instagram.zip`.
2. No Claude, abra a área de Skills nas configurações e envie o .zip.
3. Mande a planilha de produtos (link do Google Sheets, Excel ou CSV) e as fotos.

## Como usar

> Monta um catálogo para o Status com os produtos parados, com promoção, sem baixar a margem de 35%.

Funciona direto com a planilha gerada pela skill **Cupom fiscal vira cadastro**.

## Créditos

Skill gratuita da **Trentin Solutions**, criada por Ivaldo Trentin · trentinsolutions.com.br

Licença CC BY 4.0: use, adapte e compartilhe à vontade, mantendo o crédito.

## Apoie

A skill é gratuita e vai continuar assim. Se ela te ajudou, um Pix de qualquer valor ajuda a publicar as próximas.

- **Chave Pix aleatória:** `b73301d4-682f-46a0-857a-3a7653c2befb`
- **Recebedor:** Ivaldo Idalgo Trentin Junior Ltda
- **QR code:** trentinsolutions.com.br/skills/catalogo-whatsapp-instagram#apoie
