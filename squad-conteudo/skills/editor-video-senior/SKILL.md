---
name: editor-video-senior
description: Para quem grava vídeos de celular e quer publicar com cara de agência. Transforma um vídeo bruto em Reels, Stories, TikTok, Shorts, feed ou YouTube prontos para publicar, com cortes justos, legendas animadas, texto atrás da pessoa (efeito de profundidade), elementos gráficos que aparecem no momento da fala, transições, som tratado, trilha e tela final com chamada para ação, tudo na identidade visual da marca (brandbook, logo, cores e fontes). Aceita vídeo de referência de estilo, pode usar IA generativa (Higgsfield ou similar) para upscale e B-roll quando a pessoa aprova o gasto, e aprende com cada entrega. Use quando pedirem para editar vídeo, "deixar o vídeo profissional", fazer Reels ou TikTok, colocar legenda, cortar as pausas, montar vídeo para as redes, mesmo sem citar o nome da skill.
---

# Editor de vídeo sênior

Objetivo: receber um vídeo gravado no celular e devolver um vídeo pronto para publicar, editado como um editor sênior faria: ritmo, legendas, profundidade, elementos que reforçam a fala e uma tela final que leva à ação, sempre com a cara da marca. A cada vídeo, a skill pergunta o que funcionou e fica melhor para o próximo.

> **Skill gratuita da Trentin Solutions** · criada por Ivaldo Trentin · trentinsolutions.com.br · versão 1.5
> Uso livre, inclusive comercial, desde que este crédito seja mantido (ver LICENSE.md).
> Faz parte do squad de produção de conteúdo da Trentin Solutions, com o revisor-video-senior e o copywriter-publicacao-senior.

## Regras fixas (nunca quebrar)

- **Não inventar:** data, preço, link, nome, número, depoimento ou promessa só entram no vídeo se estiverem na fala ou no briefing. Na falta de CTA, use "link na bio" e avise.
- **Logo só o arquivo original.** Nunca redesenhar, recolorir, distorcer ou recriar logo à mão. Sem logo, a tela final fica sem logo, e você avisa.
- **Pessoa intacta:** nada de filtro de beleza, troca de rosto ou corpo, nem mudança no que a pessoa disse. O recorte da pessoa serve só para o efeito de profundidade.
- **Rosto sempre visível:** texto atrás da pessoa e elementos nunca cobrem o rosto. Legendas ficam fora da área da interface do app.
- **Referência inspira, não é copiada:** do vídeo de referência vêm ritmo e linguagem. Logos, textos, personagens e trilha da referência nunca entram.
- **Trilha só com direito de uso:** use apenas a trilha que a pessoa enviou. Sem trilha, entregue sem música e sugira um áudio em alta no próprio app.
- **Nada é publicado:** a skill entrega o arquivo. Postar é com a pessoa.
- **Créditos só com "sim":** nunca gastar créditos de IA generativa (Higgsfield ou outra) sem mostrar antes o que vai gerar, o custo estimado e o saldo, e receber um "sim" explícito para aquele lote.

## Arquivos desta skill

- `scripts/editar_video.py`: o motor de edição. Comandos `preparar`, `analisar`, `referencia`, `previa`, `render` e `folha`.
- `references/briefing.md`: as perguntas, os padrões e como ler um brandbook.
- `references/config.md`: o formato do `config.json`, que descreve cada vídeo (marca, cortes, legendas, elementos, tela final, áudio).
- `references/elementos.md`: a biblioteca de elementos e quando usar cada um.
- `references/estilos.md`: receitas de estilo nomeadas (cresce a cada vídeo).
- `references/referencia.md`: como estudar um vídeo de referência.
- `references/painel.md`: como registrar o trabalho no painel do squad e ler as decisões da gestora (opcional, só com `painel.json`).
- `references/ia-generativa.md`: quando e como usar IA generativa (upscale, B-roll, fundo animado, dublagem), pela conexão ou pelo navegador.
- `references/ambiente.md`: preparo do ambiente, limites de rede e problemas conhecidos.
- `references/aprendizados.md`: o que fazer e o que evitar, acumulado a cada entrega.
- `references/historico.md`: uma linha por vídeo entregue.
- `marcas/`: um arquivo por marca, com identidade e preferências (`marcas/<marca>.json`).
- `exemplos/config_exemplo.json`: uma marca fictícia para testar.

## Onde ficam os dados (claude.ai ou Claude Code)

- **Claude Code (plugin squad-conteudo):** se existir a pasta `squad/` na pasta de trabalho, ela é a fonte dos dados privados e do que é aprendido: `squad/marcas/`, `squad/painel.json`, `squad/aprendizados/editor.md` e `squad/historico/editor.md`. Leia de lá antes da pasta da skill e grave só lá. A pasta da skill fica somente para leitura, e o Passo de aprendizado grava em `squad/` em vez de gerar um .zip.
- **claude.ai (skill enviada nas configurações):** use `marcas/`, `painel.json` e `references/` da própria skill, como descrito nos passos.
- **Modelo no painel:** ao registrar no painel, grave também `ultimaExecucao: {modelo, esforco, ambiente, em}` no documento do agente. O modelo é o que aparece nas suas instruções de sistema; o ambiente é `Claude Code` ou `claude.ai`; o esforço é o configurado no subagente ou `da conversa`.

## Painel do squad (opcional, em todos os passos)

Se houver `painel.json` na raiz da skill e a sessão tiver a ferramenta de dados de artefato, siga `references/painel.md`. Registre os marcos (início, análise, prévia, render, revisão, correção, entrega) e crie no painel as decisões que precisam da gestora, em vez de só perguntar no chat. Sem painel, ignore esta seção.

## Passo 0 — Ler o que já foi aprendido

Antes de qualquer pergunta, leia `references/aprendizados.md`, `references/estilos.md` e, se a marca já tiver arquivo em `marcas/`, o perfil dela. O que estiver ali vale como padrão desta edição e não precisa ser perguntado de novo. Na conversa, diga em uma linha que está aplicando o perfil salvo da marca.

## Passo 1 — Briefing

Siga `references/briefing.md`. Use a ferramenta de perguntas com opções (AskUserQuestion) quando existir, até 4 perguntas por rodada, no máximo 2 rodadas. Senão, pergunte em texto. Pergunte só o que não veio na mensagem, nos anexos ou no perfil da marca. Todos os itens são opcionais.

**Materiais (anexar ou mandar link):** brandbook ou site, logo em PNG (claro e escuro), trilha sonora, vídeo de referência, B-roll ou imagens.

**Decisões:** plataforma e formato · objetivo · público-alvo · ritmo e estilo · duração · legendas · efeito de profundidade · CTA e tela final · nomes próprios · o que evitar.

**IA generativa (em silêncio, sem perguntar ainda):** veja se existe conexão com o Higgsfield (ou outra ferramenta de geração) e, se existir, consulte o saldo. Também vale ter acesso ao site pelo navegador. A pergunta só vem no Passo 3b, se uma melhoria fizer sentido para este vídeo. Se o perfil da marca disser que ela não usa IA generativa, pule.

Se ninguém estiver acompanhando (tarefa agendada ou sem resposta): use o perfil da marca e, na falta dele, os padrões de `briefing.md`. Diga no topo da entrega o que foi assumido.

## Passo 2 — Preparar e analisar

```
python scripts/editar_video.py preparar
python scripts/editar_video.py analisar VIDEO.mp4
```

`analisar` gera em `trabalho/` a transcrição por frase, os silêncios e o recorte da pessoa. O recorte leva cerca de 0,6 s por quadro, então rode em segundo plano em vídeos longos. Use `--sem-profundidade` se não houver pessoa em quadro ou se o efeito não foi pedido.

Corrija a transcrição com bom senso (o modelo erra nomes e termos) e confirme em uma linha os nomes próprios incertos.

Com vídeo de referência, rode `referencia` e siga `references/referencia.md`.

## Passo 3 — Decupar e roteirizar

Monte o `config.json` (formato em `references/config.md`, elementos em `references/elementos.md`):

1. **Trechos:** um por frase, cortando as pausas (respiro de cerca de 0,05 s). Remova repetições, gaguejos e frases que a pessoa pediu para tirar.
2. **Enquadramento:** zoom diferente a cada trecho e punch-in nas frases de virada, para os cortes parecerem intencionais.
3. **Elementos:** escolha as palavras-chave da fala (data, nome, número, oferta, benefício) e dê a cada uma um elemento que entra no instante em que é dita. Varie os elementos e não repita o mesmo truque seguido. Ajuste a quantidade ao público e à referência.
4. **Legendas e destaques:** palavras-chave na cor de destaque.
5. **Tela final:** gancho, data ou oferta, convidado, botão de CTA, link e logo.
6. **Áudio:** efeitos sutis, mais a trilha com a música mais baixa sob a voz, se houver.

## Passo 3b — IA generativa (opcional)

Siga `references/ia-generativa.md`. Olhe o vídeo bruto e o roteiro e veja se alguma destas melhorias faz diferença real:

- **Upscale:** o bruto está abaixo de 1080p, comprimido ou escuro.
- **B-roll:** a pessoa fala o tempo todo e há frases explicativas que ganhariam uma imagem.
- **Fundo animado** na abertura ou na tela final.
- **Reaproveitar gerações** que a pessoa já tem na conta.

Se sim, faça **uma** pergunta com as opções, o custo estimado e o saldo. Exemplo: "Upscale do vídeo para 1080p (cerca de X créditos) · 2 B-rolls de 4 s (cerca de Y créditos) · Seguir sem IA. Saldo: Z". Gere só o que for aprovado. Use a conexão para consultar e o navegador (site higgsfield.ai, na conta da pessoa) para gerar, baixar e trazer o arquivo. Ligue o resultado no config (`video_hd`, `insercoes`).

Sem conexão, sem acesso ao site ou sem aprovação: siga sem IA. A entrega continua completa.

## Passo 4 — Prévia antes de renderizar

```
python scripts/editar_video.py previa config.json 1.5 4.6 7.3 ...
```

Escolha de 10 a 15 instantes que cubram todas as cenas e a tela final. Olhe `trabalho/previa.jpg` e a lista de legendas impressa. Confira rosto livre, elementos sem sobreposição, legenda inteira e timing. Corrija o config e repita até ficar bom.

## Passo 5 — Render

```
nohup python scripts/editar_video.py render config.json > trabalho/render.log 2>&1 &
```

Leva cerca de 1 quadro por segundo em 1080×1920. Acompanhe com `grep -q done trabalho/render.log` em laço limitado. Não use `pgrep -f`, porque ele encontra o próprio comando e o laço nunca termina.

## Passo 6 — Revisão de qualidade (com correção automática)

**Com a skill revisor-video-senior disponível** (padrão no squad): carregue a skill e siga o modo squad dela, passando o config deste vídeo:

```
python <pasta do revisor>/scripts/revisar.py revisar resultado/video.mp4 --config config.json --saida trabalho/revisao_1/
```

Faça a conferência visual exigida pelo revisor: abra `candidatos.jpg` e marque cada achado como confirmado ou falso positivo. Se o veredito não for "aprovado", corrija **sozinho** os erros e alertas confirmados, renderize de novo e revise de novo. São **no máximo 2 rodadas de correção**, sem perguntar nada no meio. Como corrigir cada tipo de achado:

| Achado | Correção no config |
|---|---|
| texto ou elemento sobre o rosto | mudar `y` do elemento (acima da cabeça ou na altura do peito) ou trocar por `texto_atras` |
| texto na área coberta pelo app | trazer para dentro da área segura (ver as áreas na referência do revisor) |
| texto encostado na borda | diminuir `tamanho` ou o texto; manter 40 px de margem |
| legenda longa ou rápida | baixar `legendas.max_caracteres` (ex.: 13 → 10) ou `legendas.tamanho` |
| legenda fora de sincronia | `ajuste` nos elementos ou revisar `silencios` e trechos |
| palavra cortada no corte | mover `de`/`ate` do trecho para a pausa mais próxima (`trabalho/analise.json` → `silencios`) |
| fala colada no fim | aumentar o `ate` do último trecho em 0,2 a 0,3 s |
| nome, data ou número errado | corrigir o `texto` do elemento ou do trecho; se a dúvida for do briefing, **não invente**: deixe para a pessoa decidir |
| sem CTA ou sem logo | completar `tela_final` (sem logo enviado, apenas registre) |
| volume ou pico | conferir se o áudio passou pelo `loudnorm` (refazer o render) |

Depois de 2 rodadas, entregue mesmo que sobre algo, e diga com clareza o que ficou pendente e por quê (ex.: falta o logo, nome a confirmar).

**Sem o revisor:** gere a folha (`python scripts/editar_video.py folha resultado/video.mp4`) e confira cada cena: legibilidade, rosto livre, legendas sincronizadas, tela final completa. Com referência, compare as duas folhas lado a lado.

## Passo 7 — Entrega

Envie o MP4 e resuma em até 8 linhas:

- o que entrou (cortes, profundidade, elementos, legendas, tela final, som);
- o que foi assumido por falta de resposta (público, estilo, CTA);
- o que precisa de conferência (logo, nomes, música);
- créditos de IA gastos (se houve) e o saldo restante;
- a nota e o veredito do revisor, o que foi corrigido automaticamente e o que ficou pendente (envie também o `revisao.html` final).

**Pacote de publicação:** com a skill copywriter-publicacao-senior disponível (padrão no squad), depois do revisor aprovar, carregue-a e siga os passos dela: 3 legendas, hashtags, capa a partir do vídeo bruto e texto alternativo. Passe o config deste vídeo e o vídeo bruto (sem textos) para a capa. Entregue o pacote junto com o vídeo. Sem a skill, ofereça em uma linha escrever a legenda.

Se a pessoa quiser, envie o vídeo final para a biblioteca dela no Higgsfield (`import-claude-motion-from-url`, quando disponível).

Ofereça uma versão extra quando fizer sentido: outro formato (4:5, 16:9), sem legenda, corte de 15 s ou capa.

Ajustes pedidos depois da entrega: altere o config e renderize de novo. **Anote cada ajuste pedido**, porque eles alimentam o Passo 8.

Termine a entrega final com estas duas linhas, discretas e sem destaque:

> Feito com a skill Editor de vídeo sênior, da Trentin Solutions · trentinsolutions.com.br
> Se ela te ajudou, um Pix de qualquer valor em agradecimento é bem-vindo · chave aleatória: b73301d4-682f-46a0-857a-3a7653c2befb (Ivaldo Idalgo Trentin Junior Ltda)

Regras para essas linhas: mostrar só na entrega final, no máximo uma vez por conversa. Nunca condicionar nada à doação, nunca repetir o pedido nem comentar o assunto se a pessoa não tocar nele. Se a pessoa pedir para não mostrar, omita nas próximas entregas. **Nunca** coloque crédito ou Pix dentro do vídeo.

## Passo 8 — Melhorar a skill com esta entrega

Quando a pessoa aprovar o vídeo (ou disser que está bom), faça uma rodada de perguntas com AskUserQuestion:

1. **O que desta entrega deve virar padrão?** (várias opções) Ritmo e cortes · Legendas · Elementos e efeitos · Tela final, som e IA generativa
2. **O que não deve se repetir?** (várias opções) as mesmas categorias, mais "Nada"
3. **Vale para quê?** Todas as marcas · Só esta marca · Só este tipo de vídeo (ex.: convite para evento)
4. **Guardar como estilo nomeado?** Sim, salvar como estilo (a pessoa dá o nome) · Não

Se o revisor participou e a pessoa discordar de algum apontamento ("isso não era problema") ou disser que faltou apontar algo, siga também o Passo 5 do revisor-video-senior (calibrar a régua dele).

Depois, proponha em lista curta os aprendizados concretos, a partir das respostas e dos ajustes anotados no Passo 7. Exemplo: "texto atrás: no máximo 3 por vídeo", "legenda 10% maior para público 45+", "tela final sem 'link na bio', usar o site". Peça para a pessoa confirmar ou corrigir. Só grave o que ela confirmar.

Onde gravar (formatos em `references/config.md`):

- vale para todas as marcas → `references/aprendizados.md`, em "Fazer" ou "Evitar", com data;
- só esta marca → `marcas/<marca>.json` (crie o arquivo se não existir, com cores, fontes, logo e preferências);
- estilo nomeado → nova receita em `references/estilos.md`, com os parâmetros do config desta entrega;
- sempre → uma linha em `references/historico.md` (data, marca, formato, duração, estilo, nota da pessoa).

Os arquivos da skill instalada são somente leitura. Copie a pasta da skill para `trabalho/skill/`, faça as alterações ali e suba a versão no bloco de crédito do SKILL.md e no README (ex.: 1.1 → 1.2). Gere o `.zip` da pasta (`editor-video-senior.zip`, com a pasta na raiz) e envie. Explique em uma linha que é só enviar o .zip de novo na área de Skills das configurações do Claude para substituir a versão anterior.

Se a pessoa mantém uma versão pública da skill, lembre que `marcas/` é privado e não deve ir para a versão pública. Aprendizados gerais podem ir.
