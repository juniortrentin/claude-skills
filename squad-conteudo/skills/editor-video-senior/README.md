# Editor de vídeo sênior

Uma skill para o Claude para quem grava vídeo no celular e quer publicar com cara de agência. Você manda o vídeo bruto e, se tiver, o brandbook, o logo, a trilha e um vídeo de referência. Ela devolve o vídeo pronto para Reels, Stories, TikTok, Shorts, feed ou YouTube.

Faz parte do squad de produção de conteúdo da Trentin Solutions.

## O que ela faz

1. **Conversa rápida:** pergunta só o que falta (formato, objetivo, público, ritmo, legendas, CTA). Tudo é opcional.
2. **Transcreve e corta as pausas,** com zoom alternado para os cortes ficarem naturais.
3. **Recorta a pessoa do fundo** para o efeito de profundidade: fundo desfocado e palavras gigantes atrás de quem fala.
4. **Coloca elementos no instante da fala:** data, nome do convidado, selos, ícones, gráfico, pílulas.
5. **Legenda palavra por palavra,** com as palavras-chave na cor da marca.
6. **Trata o som:** voz limpa e no volume certo para as redes, efeitos sutis e a trilha mais baixa sob a voz.
7. **Monta a tela final** com a chamada para ação e o logo.
8. **Segue o vídeo de referência,** se você mandar um: copia o ritmo e o estilo, nunca o conteúdo.
9. **Usa IA generativa quando vale a pena** (opcional): com conta no Higgsfield ou similar, sugere upscale do vídeo, cenas de apoio (B-roll) ou fundo animado. Mostra o custo em créditos e só gera com o seu "sim".
10. **Passa pelo revisor antes de te entregar:** com a skill revisor-video-senior instalada, o vídeo é revisado (legendas, rosto, cortes, áreas do app, som) e corrigido sozinho até 2 vezes.
11. **Prepara o post** (opcional): com a skill copywriter-publicacao-senior instalada, entrega junto com o vídeo as legendas, as hashtags e a capa.
12. **Aparece no painel do squad** (opcional): registra cada etapa e pede as decisões importantes na mesa da gestora.
13. **Aprende com cada entrega:** no fim, pergunta o que deve virar padrão e o que evitar, e guarda por marca ou para todas.

## O que vem no pacote

```
editor-video-senior/
├── SKILL.md                instruções que o Claude segue
├── README.md               este arquivo
├── LICENSE.md              uso livre, mantendo o crédito
├── scripts/
│   └── editar_video.py     motor de edição (analisar, prévia, render, revisão)
├── references/
│   ├── briefing.md         perguntas, padrões e leitura do brandbook
│   ├── config.md           formato do arquivo de cada vídeo
│   ├── elementos.md        biblioteca de elementos gráficos
│   ├── estilos.md          receitas de estilo (crescem a cada vídeo)
│   ├── referencia.md       como estudar um vídeo de referência
│   ├── painel.md           registro no painel do squad (opcional)
│   ├── ia-generativa.md    upscale, B-roll e fundos com IA (opcional)
│   ├── ambiente.md         preparo, rede e problemas conhecidos
│   ├── aprendizados.md     o que fazer e o que evitar
│   └── historico.md        vídeos já entregues
├── marcas/                 perfis de marca (privado, criado com o uso)
└── exemplos/
    └── config_exemplo.json uma marca fictícia para testar
```

## Como instalar

1. Baixe o arquivo `editor-video-senior.zip`.
2. No Claude, abra a área de Skills nas configurações e envie o .zip.
3. Use o Claude com execução de código ligada. O vídeo é editado no próprio ambiente do Claude, sem programa de edição. Assinatura extra só se você quiser a camada de IA generativa (Higgsfield ou similar).

## Como usar

> Edita esse vídeo para o Reels da minha marca. Segue o brandbook e o logo. Quero algo no estilo desse vídeo de referência.

Um vídeo de 20 a 30 s leva de 15 a 25 minutos entre análise, prévia e render.

## Créditos

Skill gratuita da **Trentin Solutions**, criada por Ivaldo Trentin · trentinsolutions.com.br · versão 1.5

Licença CC BY 4.0: use, adapte e compartilhe à vontade, mantendo o crédito.

## Apoie

A skill é gratuita e vai continuar assim. Se ela te ajudou, um Pix de qualquer valor ajuda a publicar as próximas.

- **Chave Pix aleatória:** `b73301d4-682f-46a0-857a-3a7653c2befb`
- **Recebedor:** Ivaldo Idalgo Trentin Junior Ltda
- **QR code:** trentinsolutions.com.br/skills/editor-video-senior#apoie
