# Revisor de vídeo sênior

Uma skill para o Claude que confere um vídeo pronto antes de você postar. Ela olha o vídeo como um revisor que não participou da edição e aponta, com o segundo exato e o quadro marcado, tudo o que pode atrapalhar.

Faz parte do squad de produção de conteúdo da Trentin Solutions. Funciona sozinha, para qualquer vídeo (CapCut, editor externo, gravação direta), e também junto com o **editor-video-senior**, que manda o vídeo para revisão e corrige os problemas antes de te entregar.

## O que ela confere

- **Legendas:** batem com a fala? Estão sincronizadas? Algum nome ou palavra escrito errado? Dá tempo de ler?
- **Pessoas:** tem texto ou elemento em cima do rosto?
- **Cortes:** alguma palavra cortada no meio? Estalo no áudio? A fala termina colada no fim?
- **Plataforma:** algo cai embaixo dos botões do app (curtir, comentar, descrição)? Formato, resolução e duração estão certos?
- **Som:** volume no padrão das redes? Algum estouro?
- **Imagem:** tela preta, imagem congelada, flashes que incomodam pessoas fotossensíveis?
- **Conteúdo e marca:** data ou número na tela que ninguém confirmou? Tem chamada para ação? Logo na tela final? Cores da marca?

## O que você recebe

Um relatório de 1 página com nota de 0 a 100, veredito (aprovado, ajustes ou reprovado) e cada problema com o segundo do vídeo, o quadro marcado e como corrigir. Antes de entregar, o Claude confere cada apontamento olhando os quadros, para não te mandar alarme falso.

## O que vem no pacote

```
revisor-video-senior/
├── SKILL.md                instruções que o Claude segue
├── README.md               este arquivo
├── LICENSE.md              uso livre, mantendo o crédito
├── scripts/
│   └── revisar.py          revisão automática e relatório
└── references/
    ├── criterios.md        o que é verificado e o peso de cada item
    ├── plataformas.md      áreas seguras de Reels, TikTok, Shorts, feed
    ├── painel.md           registro no painel do squad (opcional)
    ├── regua.md            ajustes aprendidos com você
    └── historico.md        vídeos revisados
```

## Como instalar

1. Baixe o arquivo `revisor-video-senior.zip`.
2. No Claude, abra a área de Skills nas configurações e envie o .zip.
3. Use o Claude com execução de código ligada.

## Como usar

> Revisa esse vídeo antes de eu postar no Reels. O convidado é o Marina Costa e o evento é dia 27 de outubro.

## Créditos

Skill gratuita da **Trentin Solutions**, criada por Ivaldo Trentin · trentinsolutions.com.br · versão 1.2

Licença CC BY 4.0: use, adapte e compartilhe à vontade, mantendo o crédito.

## Apoie

A skill é gratuita e vai continuar assim. Se ela te ajudou, um Pix de qualquer valor ajuda a publicar as próximas.

- **Chave Pix aleatória:** `b73301d4-682f-46a0-857a-3a7653c2befb`
- **Recebedor:** Ivaldo Idalgo Trentin Junior Ltda
- **QR code:** trentinsolutions.com.br/skills/revisor-video-senior#apoie
