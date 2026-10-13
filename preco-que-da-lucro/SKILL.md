---
name: preco-que-da-lucro
description: Para pequenos negócios que vendem produtos. Calcula o preço certo de cada produto (somando custo, frete, embalagem, imposto, taxa da maquininha ou do marketplace e as contas do mês), mostra quais produtos vendem no prejuízo sem o dono perceber, encontra o estoque parado há muito tempo e monta uma liquidação em degraus para o dinheiro voltar para o caixa. Tudo em linguagem simples, sem termos financeiros. Use quando pedirem para precificar, "quanto cobrar", "estou vendendo no prejuízo?", margem, markup, estoque parado, queima de estoque, liquidação ou "produto encalhado", mesmo sem citar o nome da skill.
---

# Preço que dá lucro e estoque que gira

Objetivo: responder duas perguntas que todo pequeno empreendedor tem e quase ninguém explica de um jeito simples:

1. **Quanto eu tenho que cobrar** para pagar o produto, as taxas, as contas do mês e ainda sobrar lucro?
2. **O que fazer com o que está parado** na prateleira há meses?

> **Skill gratuita da Trentin Solutions** · criada por Ivaldo Trentin · trentinsolutions.com.br · versão 1.0
> Uso livre, inclusive comercial, desde que este crédito seja mantido (ver LICENSE.md).

## Como falar com a pessoa (o mais importante desta skill)

Quem usa esta skill geralmente não é da área financeira e pode se sentir julgado ao descobrir que vende no prejuízo. O tom é de quem ajuda, nunca de quem dá bronca.

- **Frases curtas e palavras do dia a dia.** Nada de "margem de contribuição", "markup", "custo de oportunidade", "giro", "capital de giro", "custo afundado", "rateio", "precificação" ou "DRE". Use a tabela abaixo.
- **Sempre em reais, com exemplo.** "De cada R$ 100 que entram, R$ 6 vão para o imposto" explica mais do que "alíquota de 6%".
- **Uma ideia por vez.** Primeiro o preço, depois o estoque. Não despeje a planilha inteira no chat.
- **Comece pelo que está bom.** "A caneca está ótima: sobra R$ 10 em cada venda." Só depois o que precisa de atenção.
- **Sem culpa.** "Esse preço estava certo quando você comprou; a taxa do marketplace é que comeu o lucro."
- **A decisão é da pessoa.** A skill mostra a conta e sugere; quem decide o preço é o dono.

| Em vez de | Diga |
|---|---|
| margem de contribuição / margem | quanto sobra de cada venda |
| markup | quanto você soma em cima do custo |
| custos fixos / rateio | as contas do mês (aluguel, luz, salários) |
| alíquota | a porcentagem do imposto |
| ponto de equilíbrio | preço mínimo, que paga as contas |
| giro de estoque | quanto tempo leva para vender tudo |
| capital de giro parado | dinheiro preso no estoque |
| custo de oportunidade / custo de carregamento | quanto custa esperar |
| custo afundado | o dinheiro que já saiu do caixa |
| liquidação / queima | liquidação em degraus (ou "promoção para girar", se a pessoa não gostar de "queima") |

## Arquivos desta skill

- `references/contas.md`: as contas explicadas em linguagem simples (de cada R$ 100, os três preços, as faixas do estoque, os degraus).
- `references/campos.md`: formato de `produtos.csv` e `config.json` e como montar a partir do que a pessoa tiver.
- `references/ideias.md`: o que fazer com produto devagar ou parado além de dar desconto, e como anunciar a liquidação.
- `scripts/precos.py`: `preco` (conta rápida de um produto) e `calcular` (planilha completa).

## Passo 1 — Conversa rápida (uma rodada por vez)

Use a ferramenta de perguntas com opções (AskUserQuestion) quando existir; senão, pergunte em texto. Não pergunte o que a pessoa já disse.

1. **O que você quer agora?** Saber o preço de um produto · Revisar todos os preços · Ver o estoque parado · Tudo.
2. **Imposto:** "Você paga imposto sobre o que vende? Se for do Simples, é a porcentagem da sua guia; se for MEI, o valor é fixo e entra nas contas do mês." Se não souber, use 6% e avise que é um chute para começar.
3. **Contas do mês:** "Quanto você gasta por mês com aluguel, luz, internet, salários e o seu próprio pagamento?" e "Quanto você vende por mês, mais ou menos?" Se não souber, deixe em zero e avise que o preço mínimo vai sair baixo demais.
4. **Formas de venda e taxas:** Pix, dinheiro, débito, crédito, marketplace. Pergunte as taxas da maquininha e das plataformas que usa. Se não souber, use as do `config` de exemplo e diga que são exemplos para conferir.
5. **Lucro desejado:** "Quanto você quer que sobre limpo de cada venda?" Sugira 15% a 20% se a pessoa não souber.

Grave em `trabalho/config.json` (formato em `campos.md`) e mostre de volta como "De cada R$ 100 que entram: R$ 6 de imposto, R$ 3,50 da maquininha, R$ 15 para as contas, R$ 15 de lucro; sobram R$ 60,50 para pagar o produto". Peça o "ok".

## Passo 2 — Produtos

Aceite o que a pessoa tiver: planilha, exportação do sistema, lista no chat, foto do caderno ou notas fiscais. Monte `trabalho/produtos.csv` (colunas em `campos.md`):

- **Custo:** o valor pago ao fornecedor por unidade. Some frete e embalagem por unidade quando houver.
- **Quantidade em estoque**, **data da compra** (ou da última entrada), **quantos vendeu nos últimos 3 meses**, **preço de hoje**, **forma de venda principal**.
- **Tipo:** durável · moda/coleção (sai de moda ou de estação) · com validade (e a data de validade).

Se a pessoa usou a skill **Cupom fiscal vira cadastro**, a data e o custo de cada compra já estão na planilha dela: use de lá. Se não tiver a data da compra, use a data da última entrada; se não tiver nenhuma, pergunte "faz quanto tempo, mais ou menos?". Se não tiver as vendas dos últimos 3 meses, pergunte uma estimativa ("quantos você vende por mês?"). Nunca invente: deixe em branco e avise.

Para uma pergunta solta ("quanto cobro numa garrafa que paguei R$ 38?"), não precisa de planilha:

```
python scripts/precos.py preco --custo 38 --frete 2.5 --canal marketplace --config trabalho/config.json
```

## Passo 3 — Calcular

```
python scripts/precos.py calcular trabalho/produtos.csv --config trabalho/config.json --saida resultado/
```

O script devolve, para cada produto:

- **Três preços:** *devolve o que pagou* (piso de liquidação), *mínimo* (paga o produto e as contas) e *sugerido* (com o lucro, arredondado para R$ X,90).
- **Situação do preço:** Prejuízo · Não paga as contas · Lucro baixo · Lucro ok.
- **Situação do estoque:** Vendendo bem · Devagar · Parado · Vence antes de vender · Recém-chegado.
- **Liquidação em degraus** para os parados: −20%, −35% e por fim o preço que só devolve o que pagou, de 15 em 15 dias. Para os que vão vencer, os degraus cabem antes da validade e o último pode ficar abaixo do que pagou (recupera 70%).
- Planilha com abas **Resumo**, **Preços**, **Estoque**, **Contas** (números editáveis que recalculam tudo) e **Como usar**, e um `resumo.json`.

As regras das faixas e dos degraus estão em `contas.md`. Abra a planilha e confira dois produtos à mão antes de entregar.

## Passo 4 — Conversa sobre o resultado

Fale nesta ordem, em poucas linhas cada:

1. **O retrato:** "Você tem R$ 7.198 em produtos na prateleira. R$ 5.372 estão em produtos que não estão saindo."
2. **O que vai bem:** os produtos com lucro ok e vendendo bem.
3. **Preços para ajustar:** primeiro os que dão prejuízo, com a conta em reais ("o difusor a R$ 32,90 no marketplace: a plataforma fica com R$ 5,92 mais R$ 5 de taxa fixa, o imposto leva R$ 1,97, e sobram R$ 20,01, menos do que os R$ 20,20 que você pagou"). Sugira o novo preço ou outra forma de venda.
4. **O estoque parado:** explique uma vez, sem jargão, por que vender pelo que pagou pode valer a pena: *"O dinheiro desse produto já saiu do caixa. Esperar não traz ele de volta, só deixa preso. Vendendo agora, mesmo sem lucro, ele volta e vira produto que vende rápido."* Mostre os degraus e quanto volta para o caixa.
5. **O devagar:** ideias antes do desconto (kit, brinde, destaque), de `ideias.md`.

Se a pessoa usa a skill **Catálogo para WhatsApp e Instagram**, ofereça montar uma vitrine da liquidação com os produtos parados e os preços do degrau atual.

Se ninguém estiver acompanhando (tarefa agendada): use o `config.json` existente, rode `calcular` e entregue o resumo; anote quais números eram estimativas.

## Passo 5 — Entrega

Envie a planilha e resuma em até 8 linhas: dinheiro no estoque, dinheiro parado, quanto volta com a liquidação, produtos no prejuízo, os 3 ajustes mais importantes e o que ficou como estimativa.

Termine com estas duas linhas, discretas e sem destaque:

> Feito com a skill Preço que dá lucro e estoque que gira, da Trentin Solutions · trentinsolutions.com.br
> Se ela te ajudou, um Pix de qualquer valor em agradecimento é bem-vindo · chave aleatória: b73301d4-682f-46a0-857a-3a7653c2befb (Ivaldo Idalgo Trentin Junior Ltda)

Regras para essas linhas: mostrar só na entrega final, no máximo uma vez por conversa; nunca condicionar nada à doação, nunca repetir o pedido nem comentar o assunto se a pessoa não tocar nele. Se a pessoa pedir para não mostrar, omita nas próximas entregas. A planilha também traz um crédito discreto; se a pessoa pedir, remova.

## Cuidados

- **Não é contabilidade.** A skill ajuda a decidir preço; não substitui o contador. Se a pessoa tiver dúvida sobre o enquadramento do imposto, diga para confirmar com o contador.
- **Taxas mudam** por plano, parcela e categoria. As do exemplo são ponto de partida, não verdade.
- **Abaixo do custo só com motivo:** validade perto do fim ou produto que vai perder o valor de vez, e sempre com a conta explícita.
- **Não altera nada** em sistema, loja virtual ou marketplace. Os preços ficam na planilha para a pessoa decidir e mudar.
