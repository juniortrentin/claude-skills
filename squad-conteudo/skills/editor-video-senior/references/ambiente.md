# Ambiente, rede e problemas conhecidos

## Preparar

`python scripts/editar_video.py preparar` instala os pacotes Python (numpy, opencv, pillow, soundfile, scipy, onnxruntime, sherpa-onnx). Também baixa para `~/.cache/editor-video-senior/`:

- **Transcrição:** Whisper small da sherpa-onnx (cerca de 640 MB), dos GitHub releases:
  `https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.tar.bz2`
- **Recorte da pessoa:** `u2net_human_seg.onnx` (cerca de 170 MB), do rembg:
  `https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net_human_seg.onnx`
- **Fontes:** do npm (`@fontsource/<nome>`). Os arquivos `.woff` abrem direto no PIL.

Também precisa de `ffmpeg` e `npm` instalados.

## Rede

Em ambientes de nuvem, muitas vezes só os registros de pacotes (pip, npm) e o GitHub estão liberados:

- HuggingFace bloqueado: por isso os modelos vêm do GitHub.
- CDN do Higgsfield (cloudfront) bloqueado: arquivos gerados chegam pelo computador da pessoa (pasta conectada), por anexo, ou liberando o domínio nas configurações de rede do Claude. Ver `ia-generativa.md`.
- Site da marca bloqueado: o brandbook pode ser lido com WebFetch, mas imagens (logo) não baixam. Peça o PNG.
- Não tente extrair imagem pelo navegador em base64: a saída é truncada ou bloqueada e gasta muito contexto.
- Se um download for recusado, não insista com outro comando. Avise e peça o arquivo.

## Desempenho e memória

- O recorte leva cerca de 0,6 s por quadro em 2 CPUs. As máscaras ficam em `trabalho/mascaras.npy`, com até 720 px de largura e em uint8.
- O render leva cerca de 1 quadro por segundo em 1080×1920. O motor lê o vídeo em sequência, sem carregar tudo na memória.
- Ao somar arrays uint8, converta para uint16 antes. Com `2*M` em uint8 a conta transborda e a máscara fica transparente, deixando o texto aparecer por cima da pessoa.
- Rode render e recorte em segundo plano (`nohup ... &`) e acompanhe pelo log com laço limitado. `pgrep -f nome_do_script` encontra o próprio comando e o laço nunca termina.

## Problemas conhecidos

| Sintoma | Causa | Correção |
|---|---|---|
| Texto aparece por cima da pessoa | máscara fraca (cabelo, roupa da cor do fundo) | subir `texto_atras.y` para longe do rosto, ou desligar a profundidade nessa cena |
| Legenda cortada nas bordas | grupo longo demais | o motor reduz a escala sozinho; se ficar pequena, baixe `max_caracteres` |
| Palavra destacada no tempo errado | timing proporcional estimado | use `ajuste` na referência do elemento |
| Nome escrito errado | transcrição | corrija `trechos[].texto` |
| Pessoa cortada no enquadramento | `rosto_y` errado | ajuste `enquadramento.rosto_y` (0,25 a 0,45) |
| Halo em volta da pessoa | fundo muito diferente do corpo | aumente o desfoque ou reduza o zoom do trecho |
