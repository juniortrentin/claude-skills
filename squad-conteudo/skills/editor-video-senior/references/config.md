# Formato do config.json

Um arquivo por vídeo, ao lado do vídeo bruto. Caminhos relativos partem da pasta do config. Posições e tamanhos são em pixels de uma tela de referência 1080×1920. O motor converte para o formato de saída.

```json
{
  "video": "bruto.mp4",
  "saida": "resultado/video.mp4",
  "formato": {"largura": 1080, "altura": 1920, "fps": 30},
  "marca": {
    "nome": "Nome da marca",
    "cores": {"primaria": "#f26522", "secundaria": "#f7941d", "fundo": "#F4EFE8", "tinta": "#141416", "branco": "#ffffff"},
    "fontes": {"titulo": {"nome": "anton", "peso": 400}, "texto": {"nome": "montserrat"}},
    "logo": "logo.png",
    "granulado": 7,
    "cantoneiras": true,
    "barra_progresso": true,
    "movimento": {"curva": [0.16, 1, 0.3, 1], "duracao": 0.52}
  },
  "trechos": [
    {"de": 0.25, "ate": 4.95, "texto": "frase corrigida", "zoom": 1.0, "punch": {"palavra": "Deixa", "zoom": 1.14}}
  ],
  "silencios": [[0, 0.33], [2.93, 3.08]],
  "enquadramento": {"rosto_y": 0.33},
  "profundidade": {"ativo": true, "desfoque": 10, "rack_focus": 0.9},
  "legendas": {"estilo": "karaoke", "tamanho": 66, "y": 1390, "maiusculas": true, "caixa": true,
               "max_caracteres": 13, "largura_max": 820, "cor_destaque": "primaria", "destaques": ["roi", "27 de outubro"]},
  "elementos": [ ... ver elementos.md ... ],
  "tela_final": {"duracao": 3.6, "fundo": "fundo", "itens": [ ... ]},
  "audio": {"efeitos": true, "trilha": null, "trilha_inicio": 0, "volume_trilha_db": -16, "abaixar_sob_voz_db": 12},
  "video_hd": null,
  "insercoes": [],
  "qualidade_crf": 20
}
```

## Campos

- **trechos:** em segundos do vídeo bruto, em ordem e sem sobreposição. `texto` é a fala corrigida e vira a legenda. `zoom` vai de 1.0 a cerca de 1.2. `punch` aumenta o zoom a partir de uma palavra.
- **silencios:** se omitido, vem de `trabalho/analise.json`. Serve para distribuir as palavras no tempo.
- **enquadramento.rosto_y:** altura do rosto no quadro (0 = topo). Ajuste se a pessoa estiver muito alta ou baixa.
- **profundidade:** precisa de `trabalho/mascaras.npy` (gerado por `analisar`). Sem o arquivo, o texto "atrás" aparece na frente, mais transparente.
- **legendas.estilo:** `karaoke` (palavra falada acende) · `frase` (tudo aceso) · `nenhuma`. `destaques` aceita palavras e expressões, sem diferença entre maiúsculas e minúsculas.
- **audio.trilha:** caminho do MP3 ou WAV. A música fica mais baixa sob a voz, sobe na tela final e tem fade no início e no fim.

- **video_hd:** versão melhorada do bruto (ex.: upscale por IA), com o mesmo conteúdo e a mesma duração. A imagem vem dela, e o recorte e o tempo vêm do bruto. A taxa de quadros pode ser diferente.
- **insercoes:** B-roll em tela cheia, com a voz continuando por baixo e legendas e elementos por cima. Campos: `arquivo`, `de`, `ate`, `inicio_clip` (segundo do clipe onde começar), `transicao` (fusão em s, padrão 0,15), `zoom_lento` (padrão 0,06) e `tratamento` (leve dessaturação e vinheta para combinar com o vídeo; padrão true). Ver `ia-generativa.md`.

## Referências de tempo (campos `de` e `ate`)

- `{"tempo": 1.5}`: segundo exato no vídeo final
- `{"trecho": 3}`: início do trecho 3 (contando do 0)
- `{"trecho_fim": 3}`: fim do trecho 3
- `{"fim": true}`: fim da fala (início da tela final)
- `{"palavra": "workshop"}`: instante em que a palavra é dita. Opções: `ocorrencia` (1, 2…) e `a_partir_do_trecho`
- Todas aceitam `"ajuste": -0.1` (antecipar) ou positivo (atrasar)

## Tela final: itens

`faixa` (`de_y`, `ate_y`, `cor`: faixa de ponta a ponta, ex.: fundo escuro para o logo de fundo escuro; vem antes do logo na lista) · `rotulo` (texto pequeno espaçado) · `titulo` (fonte de título, grande) · `pilula` · `texto` · `botao` (com `seta`) · `link` · `logo` (`largura`). Cada item tem `texto`, `tamanho`, `cor` ou `cor_texto`/`cor_fundo`, `y` e `atraso` (entrada escalonada, cerca de 0,08 s entre itens).

## marcas/<marca>.json

Mesmo bloco `marca` do config, mais preferências aprendidas:

```json
{
  "marca": { ... },
  "preferencias": {
    "estilo": "nome de uma receita em estilos.md",
    "legendas": {"tamanho": 66},
    "tela_final": {"cta_padrao": "GARANTA SUA VAGA", "link_padrao": "LINK NA BIO"},
    "fazer": ["..."],
    "evitar": ["..."]
  },
  "ia": {"usar": true, "limite_creditos_por_video": 40, "ferramenta": "higgsfield"},
  "atualizado_em": "AAAA-MM-DD"
}
```
