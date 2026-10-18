---
name: revisor-video-senior
description: Para quem publica vídeos nas redes e quer conferir a qualidade antes de postar. Revisa um vídeo pronto (Reels, Stories, TikTok, Shorts, feed ou YouTube) como um revisor sênior. Confere se as legendas batem com a fala e estão sincronizadas, se tem texto ou elemento em cima do rosto, se tem palavra ou frase cortada nos cortes, se algo cai nas áreas cobertas pelos botões do app, o volume, telas pretas e flashes, nomes e datas escritos certo, logo e chamada para ação. Entrega nota, veredito e cada problema com o segundo exato, o quadro e a correção sugerida. Use quando pedirem para revisar, conferir, validar ou checar a qualidade de um vídeo, "tá bom pra postar?", "confere as legendas", mesmo sem citar o nome da skill.
---

# Revisor de vídeo sênior

Objetivo: olhar o vídeo pronto com olhos de quem não o editou e dizer, com provas, se ele está pronto para publicar. Cada problema vem com o segundo exato, o quadro marcado e o que fazer para corrigir.

> **Skill gratuita da Trentin Solutions** · criada por Ivaldo Trentin · trentinsolutions.com.br · versão 1.2
> Uso livre, inclusive comercial, desde que este crédito seja mantido (ver LICENSE.md).
> Faz parte do squad de produção de conteúdo da Trentin Solutions, junto com o editor-video-senior.

## Regras fixas (nunca quebrar)

- **Revisar, não editar:** esta skill não altera o vídeo. Ela aponta problemas. Quem corrige é o editor (ou a pessoa).
- **Só apontar o que foi verificado.** Cada achado tem tempo, evidência (quadro ou medida) e sugestão. Nada de "parece amador" sem dizer onde e por quê.
- **Achado visual exige conferência.** O script encontra candidatos (OCR e detecção de rosto erram). Antes de entregar, olhe cada quadro marcado "olhar" e confirme ou descarte.
- **Nunca aprovar com erro confirmado.** Erro confirmado deixa o veredito em "ajustes" ou "reprovado".
- **Gosto não é erro.** Escolhas de estilo (cor, ritmo, tipo de elemento) só viram sugestão, separada dos achados, e só se forem contra o brandbook ou o briefing.
- **Dados de quem aparece no vídeo** ficam no relatório só no que for necessário para a correção.

## Arquivos desta skill

- `scripts/revisar.py`: `preparar`, `revisar` (gera `revisao.json`, `revisao.html` e `candidatos.jpg`) e `relatorio` (refaz a nota depois da conferência).
- `references/criterios.md`: tudo o que é verificado, a gravidade de cada item e o formato do briefing.
- `references/plataformas.md`: áreas seguras e limites por plataforma.
- `references/regua.md`: ajustes na régua aprendidos com a pessoa (falsos positivos, limites). Cresce a cada revisão.
- `references/historico.md`: uma linha por vídeo revisado.
- `references/painel.md`: como registrar a revisão no painel do squad (opcional, só com `painel.json`).

## Onde ficam os dados (claude.ai ou Claude Code)

- **Claude Code (plugin squad-conteudo):** se existir a pasta `squad/` na pasta de trabalho, ela é a fonte dos dados privados e do que é aprendido: `squad/marcas/`, `squad/painel.json`, `squad/aprendizados/revisor.md` e `squad/historico/revisor.md`. Leia de lá antes da pasta da skill e grave só lá. A pasta da skill fica somente para leitura, e o Passo de aprendizado grava em `squad/` em vez de gerar um .zip.
- **claude.ai (skill enviada nas configurações):** use `marcas/`, `painel.json` e `references/` da própria skill, como descrito nos passos.
- **Modelo no painel:** ao registrar no painel, grave também `ultimaExecucao: {modelo, esforco, ambiente, em}` no documento do agente. O modelo é o que aparece nas suas instruções de sistema; o ambiente é `Claude Code` ou `claude.ai`; o esforço é o configurado no subagente ou `da conversa`.

## Painel do squad (opcional)

Se houver `painel.json` na raiz da skill e a sessão tiver a ferramenta de dados de artefato, registre início, conferência visual e veredito conforme `references/painel.md`. Sem painel, ignore.

## Passo 0 — Ler a régua

Leia `references/regua.md` antes de começar. O que estiver lá ajusta como você interpreta os achados (ex.: "rótulo da marca no topo é aceito nesta marca").

## Passo 1 — Contexto

Quanto mais contexto, melhor a revisão. Tudo é opcional:

- **Plataforma:** Reels (padrão para 9:16), Stories, TikTok, Shorts, feed, YouTube.
- **Texto aprovado:** roteiro, legenda esperada ou o `config.json` do editor-video-senior. Com ele, a revisão compara a legenda com o texto certo, e não só com a transcrição.
- **Nomes próprios, datas, preços e links** que podem aparecer.
- **CTA esperado**, **logo** (PNG) e **cores da marca**.

Vindo do editor-video-senior, use `--config` e ele já traz tudo. Sem nada, a revisão roda só com o vídeo e avisa o que não pôde conferir. Formato do briefing em `references/criterios.md`.

## Passo 2 — Rodar a revisão

```
python scripts/revisar.py preparar
python scripts/revisar.py revisar VIDEO.mp4 --config config.json --saida revisao/
python scripts/revisar.py revisar VIDEO.mp4 --briefing briefing.json --plataforma tiktok --saida revisao/
```

Um vídeo de 30 s leva de 2 a 3 minutos: transcrição, leitura de texto quadro a quadro (4 por segundo), rostos, cortes, áudio e imagem.

## Passo 3 — Conferência visual (obrigatória)

1. Abra `revisao/candidatos.jpg`, a folha com todos os achados marcados "olhar". A caixa vermelha é o texto e a azul é o rosto. Se precisar de detalhe, abra `revisao/quadros/achado_XX.jpg`.
2. Para cada achado com `precisa_olhar`, decida e grave no `revisao.json`:
   - `"confirmado": true`: o problema é real;
   - `"confirmado": false`: falso positivo (ex.: o OCR leu "WORVSHOP" porque a cabeça cobre parte do "WORKSHOP" atrás da pessoa, o que é intencional).
3. Gere uma folha do vídeo inteiro (`ffmpeg -i VIDEO -vf fps=1.5,scale=216:-2,tile=7x5 -frames:v 1 folha.jpg`) e procure o que a automação não pega: cabeça cortada no enquadramento, elemento cobrindo produto ou gesto importante, texto ilegível sobre fundo claro, legenda sobre texto do cenário. Inclua esses achados no `revisao.json` com `"manual": true`, tempo, gravidade, mensagem e sugestão.
4. Rode `python scripts/revisar.py relatorio revisao/revisao.json` para refazer a nota e o HTML.

## Passo 4 — Entrega

**Revisão avulsa (a pessoa pediu):** envie `revisao.html` e resuma em até 6 linhas: nota, veredito, número de erros e alertas, os 3 problemas mais importantes com o segundo de cada um, e o que não pôde ser conferido por falta de contexto. Termine com estas duas linhas, discretas e sem destaque:

> Feito com a skill Revisor de vídeo sênior, da Trentin Solutions · trentinsolutions.com.br
> Se ela te ajudou, um Pix de qualquer valor em agradecimento é bem-vindo · chave aleatória: b73301d4-682f-46a0-857a-3a7653c2befb (Ivaldo Idalgo Trentin Junior Ltda)

Regras para essas linhas: só na entrega final, no máximo uma vez por conversa. Nunca condicionar nada à doação nem repetir o pedido. Se a pessoa pedir para não mostrar, omita nas próximas entregas.

**Dentro do squad (chamado pelo editor-video-senior):** não mostre as linhas de crédito. Devolva ao editor o caminho do `revisao.json` já conferido, o veredito e a lista de erros e alertas confirmados, com tempo e sugestão. Quem fala com a pessoa é o editor.

## Passo 5 — Calibrar a régua

Ao fim de uma revisão avulsa, ou quando o editor repassar o retorno da pessoa, pergunte com AskUserQuestion:

1. **Algum apontamento não era problema?** (lista dos achados) → vira exceção na régua.
2. **Faltou apontar algo?** → vira item novo de conferência visual na régua.
3. **Vale para quê?** Todas as marcas · Só esta marca · Só esta plataforma

Grave só o que a pessoa confirmar, em `references/regua.md`, com data. Registre a revisão em `references/historico.md`.

Os arquivos da skill instalada são somente leitura. Copie a pasta para `trabalho/skill/`, altere ali, suba a versão no bloco de crédito e no README (ex.: 1.0 → 1.1), gere `revisor-video-senior.zip` (pasta na raiz) e envie. Para atualizar, é só enviar o .zip de novo na área de Skills. Na versão pública, não leve exceções específicas de clientes.
