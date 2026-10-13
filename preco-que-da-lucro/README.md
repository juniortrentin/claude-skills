# Preço que dá lucro e estoque que gira

Uma skill para o Claude para pequenos negócios que vendem produtos. Ela responde, em linguagem simples, duas perguntas:

1. **Quanto eu tenho que cobrar** para pagar o produto, as taxas, as contas do mês e ainda sobrar lucro?
2. **O que fazer com o que está parado** na prateleira há meses?

## O que ela faz

- Mostra **para onde vai cada R$ 100** que entram: imposto, maquininha ou plataforma, contas do mês, lucro e o que sobra para pagar o produto.
- Calcula **três preços** para cada produto: o que só devolve o que você pagou, o mínimo que paga as contas e o sugerido, com lucro.
- Aponta os produtos **vendidos no prejuízo** sem você perceber (muito comum em marketplace).
- Faz o **raio-X do estoque**: há quanto tempo cada produto está lá, quanto tempo leva para vender tudo e quanto dinheiro está preso.
- Monta uma **liquidação em degraus** para o que está parado, e mostra quanto volta para o caixa.
- Entrega uma **planilha** com abas Resumo, Preços, Estoque, Contas (você muda os números e tudo recalcula) e Como usar.

## O que vem no pacote

```
preco-que-da-lucro/
├── SKILL.md                instruções que o Claude segue
├── README.md               este arquivo
├── LICENSE.md              uso livre, mantendo o crédito
├── references/
│   ├── contas.md           as contas explicadas em linguagem simples
│   ├── campos.md           formato dos arquivos e de onde tirar cada dado
│   └── ideias.md           o que fazer além do desconto
├── exemplos/
│   ├── config.json         contas de uma loja de exemplo
│   └── produtos.csv        11 produtos de exemplo
└── scripts/
    └── precos.py           conta rápida e planilha completa
```

## Como instalar

1. Baixe o arquivo `preco-que-da-lucro.zip`.
2. No Claude, abra a área de Skills nas configurações e envie o .zip.
3. Mande a sua planilha de produtos (ou só pergunte o preço de um produto).

## Como usar

> Paguei R$ 38 numa garrafa térmica e vendo por R$ 79,90 na Shopee. Estou tendo lucro?

> Aqui está minha planilha de estoque. Quero saber quais preços estão errados e o que fazer com o que está parado.

## Créditos

Skill gratuita da **Trentin Solutions**, criada por Ivaldo Trentin · trentinsolutions.com.br

Licença CC BY 4.0: use, adapte e compartilhe à vontade, mantendo o crédito.

A skill ajuda a decidir preço; não substitui o contador.

## Apoie

A skill é gratuita e vai continuar assim. Se ela te ajudou, um Pix de qualquer valor ajuda a publicar as próximas.

- **Chave Pix aleatória:** `b73301d4-682f-46a0-857a-3a7653c2befb`
- **Recebedor:** Ivaldo Idalgo Trentin Junior Ltda
- **QR code:** trentinsolutions.com.br/skills/preco-que-da-lucro#apoie
