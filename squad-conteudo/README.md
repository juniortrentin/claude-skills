# Squad de conteúdo · plugin para o Claude Code

Um time de agentes que transforma o vídeo gravado no celular em post pronto para o Instagram, TikTok ou Shorts. Você conversa só com o produtor. Ele faz o briefing, distribui o trabalho, garante que nada passa sem revisão e entrega tudo junto: vídeo editado, parecer de qualidade, legendas, hashtags e capa.

Cada agente roda com o modelo que combina com o trabalho dele.

| Agente | O que faz | Modelo · esforço |
|---|---|---|
| **Produtor** (skill `produtor-conteudo-senior`) | Conversa com você, faz o briefing, chama os agentes na ordem, cuida das correções e dos aprendizados | o da sua sessão |
| **Editor** (`squad-conteudo:editor-video`) | Corta as pausas, legenda, recorta a pessoa para o efeito de profundidade, coloca elementos no tempo da fala, trata o som e monta a tela final | Opus · alto |
| **Revisor** (`squad-conteudo:revisor-video`) | Confere legendas, rosto, cortes, áreas do app, som e marca, e confirma cada problema olhando o quadro | Sonnet · médio |
| **Copywriter** (`squad-conteudo:copywriter-publicacao`) | Escreve 3 legendas, escolhe as hashtags, monta a capa e o texto alternativo, sem inventar dados | Sonnet · médio |

O revisor e o copywriter rodam num modelo diferente do editor de propósito: quem revisa não é quem fez.

## Instalar

No Claude Code (aba Code do app do Claude, no navegador ou no terminal):

```
/plugin marketplace add juniortrentin/claude-skills
/plugin install squad-conteudo@trentin-solutions
```

Para editar vídeo no seu computador, ele precisa de **Python 3** e **ffmpeg**. Na primeira vez, o editor confere e mostra o comando de instalação para o seu sistema.

## Usar

Abra uma pasta de trabalho no Claude Code (por exemplo, "Squad de conteúdo"), coloque o vídeo nela e peça:

> Edita esse vídeo para o Reels da minha marca e prepara o post. É o convite para a nossa lojinha no colégio.

O produtor cria na pasta:

```
squad/        perfis de marca, aprendizados, histórico e o link do painel (privado)
projetos/     uma pasta por vídeo: bruto/, trabalho/ e entrega/
```

A pasta `squad/` é sua: guarda o que o time aprende com você a cada entrega. Não publique essa pasta.

## Trocar o modelo de um agente

O modelo e o esforço ficam no topo de cada arquivo em `agents/` (campos `model` e `effort`). Para uma produção só, peça na conversa: "usa Opus no copywriter desta vez".

## Painel do squad (opcional)

Se você tiver um painel do squad publicado como artefato no Claude, salve o link em `squad/painel.json` (`{"url": "…", "nome": "Central do squad"}`). Cada agente mostra lá o que está fazendo, com qual modelo e esforço, e as entregas aparecem com o vídeo, o parecer e o post.

## Também no claude.ai

As quatro skills funcionam sozinhas no claude.ai: compacte a pasta da skill em `skills/` e envie na área de Skills das configurações. Lá, todas rodam no modelo da conversa, porque as skills enviadas não escolhem modelo.

## Créditos

Plugin gratuito da **Trentin Solutions**, criado por Ivaldo Trentin · trentinsolutions.com.br · versão 1.0

Licença CC BY 4.0: use, adapte e compartilhe à vontade, mantendo o crédito.

## Apoie

O plugin é gratuito e vai continuar assim. Se ele te ajudou, um Pix de qualquer valor ajuda a publicar os próximos.

- **Chave Pix aleatória:** `b73301d4-682f-46a0-857a-3a7653c2befb`
