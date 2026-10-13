# Avaliações do Google respondidas

Uma skill para o Claude para quem tem negócio local com perfil no Google: ela lê as avaliações, escreve uma resposta para cada uma do jeito que você fala, separa as que pedem cuidado e mostra o que os clientes mais elogiam e mais reclamam.

## O que ela faz

1. **Lê as avaliações** do seu perfil no Google Maps (ou o texto e os prints que você mandar).
2. **Aprende o seu tom** pelas respostas antigas, ou pergunta como você fala.
3. **Escreve uma resposta para cada avaliação**, citando um detalhe do que o cliente escreveu, sem resposta copiada e colada.
4. **Separa as que pedem cuidado** (saúde, segurança, ameaça de processo, ofensa, avaliação falsa) e diz o que fazer em cada caso.
5. **Confere as respostas** antes de entregar: nada de desconto em público, telefone, número de pedido ou tom de briga.
6. **Entrega uma planilha** para você aprovar e um **relatório de 1 página**: nota por mês, o que elogiam, o que reclamam, equipe mais elogiada e as melhorias de maior impacto.
7. **Publica as aprovadas**, só se você pedir.

## O que vem no pacote

```
avaliacoes-google-respondidas/
├── SKILL.md                instruções que o Claude segue
├── README.md               este arquivo
├── LICENSE.md              uso livre, mantendo o crédito
├── references/
│   ├── coleta.md           como ler e publicar
│   ├── tom.md              tom do dono e modelos de resposta
│   ├── cuidado.md          casos delicados e como denunciar avaliação falsa
│   └── campos.md           formatos, temas e prioridades
├── exemplos/               uma pizzaria fictícia com 15 avaliações
└── scripts/
    └── avaliacoes.py       confere as respostas, gera planilha e relatório
```

## Como instalar

1. Baixe o arquivo `avaliacoes-google-respondidas.zip`.
2. No Claude, abra a área de Skills nas configurações e envie o .zip.
3. Use o Claude com acesso a navegador (ou cole as avaliações no chat).

## Como usar

> Responde as avaliações sem resposta da Pizzaria Forno Bom no Google, no mesmo tom que a gente já usa.

## Créditos

Skill gratuita da **Trentin Solutions**, criada por Ivaldo Trentin · trentinsolutions.com.br

Licença CC BY 4.0: use, adapte e compartilhe à vontade, mantendo o crédito.

## Apoie

A skill é gratuita e vai continuar assim. Se ela te ajudou, um Pix de qualquer valor ajuda a publicar as próximas.

- **Chave Pix aleatória:** `b73301d4-682f-46a0-857a-3a7653c2befb`
- **Recebedor:** Ivaldo Idalgo Trentin Junior Ltda
- **QR code:** trentinsolutions.com.br/skills/avaliacoes-google-respondidas#apoie
