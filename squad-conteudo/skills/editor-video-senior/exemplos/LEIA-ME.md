# Exemplo

`config_exemplo.json` descreve um vídeo de uma marca fictícia (Café Aurora): convite para uma aula aberta, 9:16, com profundidade, legendas karaokê, elementos e tela final.

Para testar, grave um vídeo seu de cerca de 15 s falando um texto parecido e rode:

    python scripts/editar_video.py analisar meu_video.mp4
    (ajuste os trechos do config pelos tempos de trabalho/analise.json)
    python scripts/editar_video.py previa config_exemplo.json 1 3 5 7 9 11 13 16
    python scripts/editar_video.py render config_exemplo.json
