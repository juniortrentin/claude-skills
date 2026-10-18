# Estudando um vídeo de referência

O objetivo é copiar a **linguagem** (ritmo, tipo de legenda, quantidade e jeito dos elementos, transições), nunca o **conteúdo** (logos, textos, personagens, trilha).

## 1. Obter o arquivo

- Arquivo anexado: use direto.
- Link de rede social: tente baixar. Se a rede do ambiente bloquear, peça o arquivo ou de 4 a 6 prints de momentos diferentes e siga sem a referência enquanto isso.

## 2. Medir

```
python scripts/editar_video.py referencia REFERENCIA.mp4
```

O comando grava em `trabalho/referencia.json` os cortes, o número de planos e a duração média de cada plano, e cria a folha `trabalho/referencia_folha.jpg`.

## 3. Olhar a folha e anotar

- **Ritmo:** duração média do plano (abaixo de 1,5 s é muito rápido; de 2 a 3 s é médio; acima de 4 s é calmo). Há zoom ou punch-in?
- **Legendas:** posição, tamanho, quantas palavras por vez, caixa ou contorno, cor de destaque, maiúsculas.
- **Elementos:** quantos por cena; texto atrás da pessoa? emojis, ícones, setas, pílulas? de onde entram?
- **Transições:** corte seco, zoom, wipe, flash (evite flash se a marca proíbe).
- **Cor:** contraste, granulado, fundo desfocado.
- **Tela final:** existe? o que mostra?
- **Áudio:** música presente? volume? efeitos sonoros?

## 4. Traduzir para o config

Resuma em 3 a 5 linhas o que vai aplicar e mostre à pessoa antes do render. Exemplo: "planos de cerca de 1,2 s com punch-in a cada frase, legenda de uma palavra por vez no centro, 2 elementos por cena, sem tela final".

Ajustes no config:

- planos curtos → `max_caracteres` menor nas legendas (6 a 8) e zooms alternando mais;
- legenda central → `legendas.y` perto de 960;
- poucos elementos → menos `texto_atras` e mais pílulas;
- sempre com as cores, fontes e logo da marca do cliente.

Se a pessoa gostar do resultado, o Passo 8 oferece guardar como estilo nomeado em `estilos.md`.
