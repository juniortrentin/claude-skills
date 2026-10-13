# Conexões do LinkedIn com contexto

Uma skill para o Claude que transforma as conexões novas do seu LinkedIn em contatos com contexto: empresa, cargo, porte, e-mail, telefone e uma nota de quanto cada pessoa se parece com o seu cliente ideal.

## O que ela faz

- Percorre a sua lista de conexões e pega **só as novas** desde a última rodada.
- Completa empresa, cargo, setor e porte com o LinkedIn e o Apollo, de graça.
- Busca e-mail e telefone primeiro onde é gratuito (o que a pessoa compartilhou no LinkedIn, site da empresa, CNPJ). No Apollo, **só gasta crédito com a sua aprovação**.
- Dá uma **nota de aderência** (0 a 100) pelo seu cliente ideal: cargos, setores, porte e região.
- Atualiza uma **planilha mestre** (Google Sheets, Excel ou nova) que só cresce, com abas Conexões, Resumo, Perfil ideal e Como usar.
- Opcional: rascunho de primeira mensagem para quem tem aderência alta. Nunca envia nada.

## O que vem no pacote

```
conexoes-linkedin-com-contexto/
├── SKILL.md                     instruções que o Claude segue
├── README.md                    este arquivo
├── LICENSE.md                   uso livre, mantendo o crédito
├── references/
│   ├── fontes.md                LinkedIn, Apollo, site e CNPJ, passo a passo
│   ├── campos.md                formatos, cliente ideal e nota de aderência
│   └── mensagens.md             rascunhos de primeira mensagem
└── scripts/
    └── planilha_conexoes.py     acha as novas, mescla, pontua e grava
```

## Como instalar

1. Baixe o arquivo `conexoes-linkedin-com-contexto.zip`.
2. No Claude, abra a área de Skills nas configurações e envie o .zip.
3. Use o Claude com acesso a navegador (extensão Claude in Chrome ou o navegador do app), logado no LinkedIn e, se quiser, no Apollo (plano gratuito).

## Como usar

> Enriquece minhas conexões novas do LinkedIn e atualiza a planilha. Meu cliente ideal é dono ou sócio de clínica no Paraná.

Dá para agendar uma rodada por semana: sem você por perto, ela só usa dados gratuitos e não gasta crédito.

## Créditos

Skill gratuita da **Trentin Solutions**, criada por Ivaldo Trentin · trentinsolutions.com.br

Licença CC BY 4.0: use, adapte e compartilhe à vontade, mantendo o crédito.

## Apoie

A skill é gratuita e vai continuar assim. Se ela te ajudou, um Pix de qualquer valor ajuda a publicar as próximas.

- **Chave Pix aleatória:** `b73301d4-682f-46a0-857a-3a7653c2befb`
- **Recebedor:** Ivaldo Idalgo Trentin Junior Ltda
- **QR code:** trentinsolutions.com.br/skills/conexoes-linkedin-com-contexto#apoie
