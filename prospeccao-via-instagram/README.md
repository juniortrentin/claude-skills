# Prospecção via Instagram

Uma skill para o Claude que encontra potenciais clientes no Instagram e entrega uma planilha ranqueada pela chance de estarem comprando agora.

Você escolhe o tema (pet shops e veterinárias, noivas, academias, clínicas, restaurantes, lojas, imobiliárias, eventos ou um tema seu), a região, o sinal de compra que importa e a profundidade. O Claude busca, lê os perfis públicos, pontua cada um e explica o motivo de cada indicação.

## O que vem no pacote

```
prospeccao-via-instagram/
├── SKILL.md                  instruções que o Claude segue
├── LICENSE.md                uso livre, mantendo o crédito
├── references/
│   ├── temas.md              8 temas prontos com termos, hashtags e sinais
│   ├── campos.md             formato dos dados coletados
│   └── mensagens.md          modelos de primeira mensagem
└── scripts/
    └── montar_planilha.py    gera a planilha final (Leads, Pessoas, Buscas, Como usar)
```

## Como instalar

1. Baixe o arquivo `prospeccao-via-instagram.zip`.
2. No Claude, abra a área de Skills nas configurações e envie o .zip.
3. Para a navegação no Instagram, use o Claude com acesso a navegador (extensão Claude in Chrome ou o navegador do app), logado na sua conta.

## Como usar

Peça algo como:

> Quero prospectar pet shops em Londrina pelo Instagram.

O Claude faz as perguntas do briefing, mostra o plano de busca e, depois do seu ok, monta a planilha.

## O que ela nunca faz

- Seguir, curtir, comentar ou mandar mensagem para alguém.
- Coletar contas privadas, dados sensíveis ou pessoas menores de idade.
- Tentar passar por verificações ou CAPTCHAs do Instagram.

## Créditos

Skill gratuita da **Trentin Solutions**, criada por Ivaldo Trentin · trentinsolutions.com.br

Licença CC BY 4.0: use, adapte e compartilhe à vontade, mantendo o crédito.

## Apoie

A skill é gratuita e vai continuar assim. Se ela te ajudou, um Pix de qualquer valor ajuda a publicar as próximas.

- **Chave Pix aleatória:** `b73301d4-682f-46a0-857a-3a7653c2befb`
- **Recebedor:** Ivaldo Idalgo Trentin Junior Ltda
- **QR code:** trentinsolutions.com.br/skills/prospeccao-via-instagram#apoie
