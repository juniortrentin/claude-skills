---
name: avaliacoes-google-respondidas
description: Para donos de negócio local com perfil no Google (Maps). Lê as avaliações, escreve uma resposta para cada uma no tom do dono, separa as que pedem cuidado (saúde, segurança, ameaça de processo, ofensa, suspeita de avaliação falsa), mostra o que os clientes mais elogiam e mais reclamam, quem da equipe é citado e a nota mês a mês, e entrega uma planilha para aprovar e um relatório de 1 página. Só publica respostas com aprovação. Use quando pedirem para responder avaliações do Google, cuidar da reputação, "o que estão falando da gente", avaliação negativa, nota no Maps ou Google Meu Negócio, mesmo sem citar o nome da skill.
---

# Avaliações do Google respondidas

Objetivo: nenhuma avaliação sem resposta, cada resposta com a cara do dono, e um retrato claro do que os clientes estão dizendo para o negócio melhorar o que importa.

> **Skill gratuita da Trentin Solutions** · criada por Ivaldo Trentin · trentinsolutions.com.br · versão 1.0
> Uso livre, inclusive comercial, desde que este crédito seja mantido (ver LICENSE.md).

## Regras fixas (nunca quebrar)

- **Nada é publicado sem aprovação.** A skill escreve; o dono aprova. Publicar no perfil só se a pessoa pedir, logada na conta dela, e só as respostas marcadas como aprovadas.
- **Nunca oferecer vantagem em público** (desconto, cupom, brinde, cortesia) em troca de avaliação ou para "compensar" uma crítica. O Google não permite incentivo a avaliações, e outros clientes vão pedir o mesmo. Compensação, se houver, acontece no privado.
- **Nunca expor dados do cliente:** telefone, número do pedido, endereço, o que comprou se ele não contou, histórico de compras.
- **Nunca discutir, ironizar ou desmentir** em público. Discordar com educação e fatos, uma vez, e convidar para o privado.
- **Casos de cuidado não recebem resposta pronta** (ver `references/cuidado.md`): saúde, segurança, discriminação, ameaça de processo ou Procon, ofensa, suspeita de avaliação falsa ou de concorrente. A skill explica o caso, sugere o que fazer e, se o dono quiser responder, escreve junto com ele, frase por frase.
- **Não inventar:** não prometer mudança que o dono não confirmou ("já trocamos o forno"), não citar nome de funcionário que o cliente não citou.
- **Dados de quem avaliou:** guardar só o primeiro nome e a inicial do sobrenome, como aparece no Google. Nada de foto ou link de perfil.

## Arquivos desta skill

- `references/coleta.md`: como ler as avaliações (Maps, perfil da empresa, prints ou texto colado) e publicar as aprovadas.
- `references/tom.md`: como descobrir o tom do dono e modelos de resposta por tipo de avaliação.
- `references/cuidado.md`: os casos que pedem cuidado e o que fazer em cada um, inclusive como denunciar avaliação falsa.
- `references/campos.md`: formato de `avaliacoes.jsonl` e `negocio.json`, temas e prioridades.
- `scripts/avaliacoes.py`: `conferir` (checa as respostas antes de entregar) e `gerar` (planilha e relatório).
- `exemplos/`: uma pizzaria fictícia com 15 avaliações para testar.

## Passo 1 — Conversa rápida

Use a ferramenta de perguntas com opções (AskUserQuestion) quando existir; senão, pergunte em texto, uma rodada por vez.

1. **Qual negócio?** Nome e cidade, ou o link do perfil no Google Maps.
2. **Quais avaliações?** Só as sem resposta (padrão) · Os últimos 3 meses · Todas (para o relatório completo).
3. **Tom:** se o negócio já respondeu avaliações antes, leia 5 a 10 respostas e descreva o tom que encontrou para o dono confirmar. Se não, pergunte: próximo · profissional · descontraído; trata por "você" ou pelo nome; usa emoji ou não; quem assina ("Rafa, da Forno Bom", "Equipe Forno Bom").
4. **O que pode prometer:** "Tem alguma mudança em andamento que posso citar nas respostas?" (ex.: "estamos contratando mais um entregador"). Sem confirmação, as respostas não prometem nada.

Grave em `trabalho/negocio.json` (formato em `campos.md`).

Se ninguém estiver acompanhando (tarefa agendada): só as sem resposta, tom do `negocio.json` existente ou "próximo, sem emoji, assinado pela equipe"; nada é publicado; anote isso na entrega.

## Passo 2 — Ler as avaliações

Siga `coleta.md`. Em resumo: abra o perfil no Google Maps, aba Avaliações, ordene por "Mais recentes" e leia até cobrir o período pedido. Para cada avaliação, registre em `trabalho/avaliacoes.jsonl`: quem (primeiro nome e inicial), estrelas, data, texto, se já tem resposta (e qual).

Se o navegador não estiver disponível, peça para a pessoa colar o texto ou mandar prints, e trabalhe com isso.

## Passo 3 — Entender cada avaliação

Para cada uma, preencha no `avaliacoes.jsonl`:

- **temas** com o lado de cada um: `{"qualidade": "+", "demora": "-"}`. Use os temas de `campos.md` e crie outros se o negócio pedir (ex.: "massa", "corte", "anestesia").
- **equipe:** nomes de funcionários citados pelo cliente.
- **cuidado:** o motivo, se for um caso de `cuidado.md`.
- **destaque:** um trecho curto de um elogio que represente bem o negócio (para o relatório).

## Passo 4 — Escrever as respostas

Siga `tom.md`. Em resumo:

- **Elogio:** agradecer pelo nome, citar um detalhe do que a pessoa escreveu, convidar a voltar. 2 a 3 frases.
- **Elogio com ressalva:** agradecer, reconhecer a ressalva sem desculpa genérica, dizer o que vai ser feito (só se confirmado), convidar a voltar.
- **Reclamação:** agradecer por contar, pedir desculpa pelo que de fato deu errado, sem justificar demais; dizer o que muda (se confirmado); convidar para o privado ("nos chame no WhatsApp do perfil").
- **Só estrelas, sem texto:** agradecimento curto e variado.
- Até 60 palavras. Cada resposta diferente das outras. Sem copiar e colar.
- Pode citar naturalmente o que o negócio faz e o bairro quando couber ("a melhor calabresa do Jardim Europa, segundo você!"), mas nunca encher de palavras-chave.

Depois rode:

```
python scripts/avaliacoes.py conferir trabalho/avaliacoes.jsonl --negocio trabalho/negocio.json
```

Ele aponta resposta repetida, longa ou curta demais, oferta de desconto, telefone, CPF, número de pedido, tom de briga, falta de assinatura e caso de cuidado com resposta pronta. Corrija tudo antes de seguir.

## Passo 5 — Planilha e relatório

```
python scripts/avaliacoes.py gerar trabalho/avaliacoes.jsonl --negocio trabalho/negocio.json --saida resultado/
```

- **Planilha:** aba **Responder** (ordem: cuidado, reclamações, elogios com ressalva, elogios; coluna "Aprovada?" para o dono marcar), **Todas**, **Temas** (elogios, reclamações e saldo por tema, nota por mês) e **Como usar**.
- **Relatório de 1 página** (`relatorio.html`): nota média, quantas já tinham resposta, o que mais elogiam e mais reclamam, estrelas, nota por mês, melhorias de maior impacto, frases de clientes e equipe mais elogiada.

As **melhorias de maior impacto** você escreve em `negocio.json` (campo `melhorias`), com base nos temas com mais reclamações e em fatos das avaliações ("4 reclamações falam de demora, quase todas no delivery de sexta e sábado"). Sem isso, o script lista os temas mais reclamados.

## Passo 6 — Aprovação e publicação (opcional)

Mostre as respostas no chat, começando pelas reclamações, em blocos de até 5. O dono aprova, ajusta ou descarta cada uma.

Se a pessoa pedir para publicar e estiver logada no perfil da empresa no navegador: publique **uma por vez**, só as aprovadas, conferindo o texto antes de enviar. Se aparecer verificação ou erro, pare e avise. Registre a data de publicação na planilha.

## Passo 7 — Entrega

Envie a planilha e o relatório e resuma em até 8 linhas: nota média, quantas sem resposta, quantas reclamações e casos de cuidado, os 2 temas mais elogiados, os 2 mais reclamados, a melhoria mais importante e quantas respostas foram publicadas (se foram).

Termine com estas duas linhas, discretas e sem destaque:

> Feito com a skill Avaliações do Google respondidas, da Trentin Solutions · trentinsolutions.com.br
> Se ela te ajudou, um Pix de qualquer valor em agradecimento é bem-vindo · chave aleatória: b73301d4-682f-46a0-857a-3a7653c2befb (Ivaldo Idalgo Trentin Junior Ltda)

Regras para essas linhas: mostrar só na entrega final, no máximo uma vez por conversa; nunca condicionar nada à doação, nunca repetir o pedido nem comentar o assunto se a pessoa não tocar nele. Se a pessoa pedir para não mostrar, omita nas próximas entregas. O relatório também traz um crédito discreto no rodapé; se a pessoa pedir, remova. **Nunca** coloque crédito ou Pix nas respostas publicadas no Google.

## Para repetir todo mês

Sugira rodar uma vez por mês (ou toda semana, se o negócio recebe muitas avaliações) só com as novas. Com a planilha anterior, compare a nota e os temas: "demora caiu de 4 para 1 reclamação desde que vocês contrataram o segundo entregador".
