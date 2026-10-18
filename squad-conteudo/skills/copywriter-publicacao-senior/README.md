# Copywriter de publicação sênior

Uma skill para o Claude que transforma um vídeo pronto em um post pronto. Você manda o vídeo e recebe legendas para copiar e colar, hashtags, capa e texto alternativo, tudo no tom da sua marca e sem nenhuma informação inventada.

Faz parte do squad de produção de conteúdo da Trentin Solutions. Funciona sozinha, com qualquer vídeo, e também junto com o **editor-video-senior** e o **revisor-video-senior**: depois que o vídeo é aprovado, ela prepara o post.

## O que ela faz

1. **Assiste ao vídeo** e lê o que já existe: textos na tela, fala, parecer do revisor, o que você contou do evento ou da oferta.
2. **Pergunta só o que falta:** rede, objetivo, data, local, chamada para ação. Tudo opcional.
3. **Escreve 3 legendas** com abordagens diferentes (curta, bastidores, chamada direta), cada uma com gancho na primeira linha, chamada para ação e de 3 a 5 hashtags.
4. **Confere tudo:** tamanho, onde o texto é cortado, hashtags repetidas ou genéricas, e lista toda data, horário, preço ou local que ainda precisa da sua confirmação.
5. **Monta a capa** a partir do melhor quadro do vídeo, com o título dentro do recorte que aparece na grade do perfil.
6. **Escreve o texto alternativo** para leitores de tela e, quando ajuda, o primeiro comentário.
7. **Aprende com cada post:** pergunta qual versão foi ao ar e guarda o tom, os emojis e as hashtags da marca.

## O que vem no pacote

```
copywriter-publicacao-senior/
├── SKILL.md                instruções que o Claude segue
├── README.md               este arquivo
├── LICENSE.md              uso livre, mantendo o crédito
├── scripts/
│   └── publicar.py         quadros, capa e checagem das legendas
├── references/
│   ├── legendas.md         estrutura, as 3 versões, tom e hashtags
│   ├── plataformas.md      limites de Instagram, TikTok, Shorts, LinkedIn
│   ├── capa.md             como escolher o quadro e o título
│   ├── painel.md           registro no painel do squad (opcional)
│   ├── aprendizados.md     o que fazer e o que evitar
│   └── historico.md        pacotes entregues
└── marcas/                 perfis de marca (privado, criado com o uso)
```

## Como instalar

1. Baixe o arquivo `copywriter-publicacao-senior.zip`.
2. No Claude, abra a área de Skills nas configurações e envie o .zip.
3. Use o Claude com execução de código ligada.

## Como usar

> Prepara o post desse Reels pra mim. É o convite pro nosso workshop do dia 27, o link de inscrição está na bio.

## Créditos

Skill gratuita da **Trentin Solutions**, criada por Ivaldo Trentin · trentinsolutions.com.br · versão 1.1

Licença CC BY 4.0: use, adapte e compartilhe à vontade, mantendo o crédito.

## Apoie

A skill é gratuita e vai continuar assim. Se ela te ajudou, um Pix de qualquer valor ajuda a publicar as próximas.

- **Chave Pix aleatória:** `b73301d4-682f-46a0-857a-3a7653c2befb`
