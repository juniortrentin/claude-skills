# Prospecção via LinkedIn

Uma skill para o Claude que encontra os decisores certos no público corporativo e entrega uma planilha ranqueada pela chance de estarem comprando agora.

Você escolhe o segmento (TI, RH, indústria, saúde, varejo, serviços financeiros, educação, agronegócio ou outro), os cargos (CEO, CFO, CTO, diretor, gerente, analista), o porte da empresa, a região e os sinais de compra que importam. O Claude busca, confirma os melhores no LinkedIn e explica o motivo de cada indicação.

## Você vai precisar de

- Claude com acesso a navegador (extensão Claude in Chrome ou o navegador do app), logado no LinkedIn.
- **Conta gratuita no Apollo (recomendada):** é onde a busca por segmento, cargo e porte acontece sem gastar crédito. Sem ela, a skill usa Google e LinkedIn e a lista sai menor. Crie em apollo.io.

## O que vem no pacote

```
prospeccao-via-linkedin/
├── SKILL.md                instruções que o Claude segue
├── README.md               este arquivo
├── LICENSE.md              uso livre, mantendo o crédito
├── references/
│   ├── segmentos.md        9 segmentos prontos com cargos e sinais
│   ├── fontes.md           Apollo, Google e LinkedIn em camadas
│   ├── campos.md           briefing, formato dos dados e nota
│   └── mensagens.md        nota de convite e primeira mensagem
└── scripts/
    └── montar_lista.py     pontua, ordena e grava a planilha
```

## Como instalar

1. Baixe o arquivo `prospeccao-via-linkedin.zip`.
2. No Claude, abra a área de Skills nas configurações e envie o .zip.
3. Entre no LinkedIn e no Apollo no navegador que o Claude usa.

## Como usar

> Quero prospectar CFOs e diretores financeiros de empresas de tecnologia de 50 a 500 pessoas em São Paulo.

Depois que os decisores aceitarem o seu convite, rode a skill **Conexões do LinkedIn com contexto** para completar empresa, porte e contato.

## O que ela nunca faz

- Enviar convite, mensagem, curtida ou comentário.
- Revelar contatos pagos sem a sua aprovação.
- Usar a busca do LinkedIn em volume ou tentar passar por verificações.

## Créditos

Skill gratuita da **Trentin Solutions**, criada por Ivaldo Trentin · trentinsolutions.com.br

Licença CC BY 4.0: use, adapte e compartilhe à vontade, mantendo o crédito.

## Apoie

A skill é gratuita e vai continuar assim. Se ela te ajudou, um Pix de qualquer valor ajuda a publicar as próximas.

- **Chave Pix aleatória:** `b73301d4-682f-46a0-857a-3a7653c2befb`
- **Recebedor:** Ivaldo Idalgo Trentin Junior Ltda
- **QR code:** trentinsolutions.com.br/skills/prospeccao-via-linkedin#apoie
