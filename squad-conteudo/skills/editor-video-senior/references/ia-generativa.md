# Camada de IA generativa (Higgsfield ou similar)

É opcional. A edição completa funciona sem ela. Use só quando uma melhoria fizer diferença real para aquele vídeo e a pessoa aprovar o gasto.

## Quando vale a pena

| Situação | Melhoria | Tipo de modelo (Higgsfield, out/2026) |
|---|---|---|
| Vídeo bruto abaixo de 1080p, comprimido pelo WhatsApp ou escuro | **Upscale e limpeza** do bruto antes de editar | `bytedance_video_upscale` (preset `ugc`), `topaz_video`, `video_upscale` |
| Vídeo com uma pessoa falando o tempo todo | **B-roll:** 2 ou 3 cenas de 3 a 5 s que ilustram a fala | texto para vídeo: `kling3_0`, `seedance_2_0`, `cinematic_studio_video_v2` |
| Abertura ou tela final sem impacto | **Fundo animado** na cor da marca, sem texto | texto ou imagem para vídeo, com `generate_audio` desligado |
| Vídeo para outro idioma | **Dublagem** com sincronização labial | `dubbing`, `sync_so` |
| Cenário ruim (bagunça, luz feia) | **Troca de cenário ou edição por texto** | `kling_video_edit`, `flux_3_video_edit` |
| A pessoa já gerou algo antes | **Reaproveitar gerações** da conta, sem gastar crédito | `show_generations` |

O catálogo muda com frequência. Confira sempre com `models_list` e `models_get` antes de sugerir.

## Regras

- **Nunca gastar crédito sem um "sim" explícito.** Antes de gerar, mostre: o que vai gerar, com qual modelo, a duração, a resolução, o custo estimado em créditos (o site mostra antes de confirmar) e o saldo atual (`balance`).
- Um "sim" vale para o lote que foi mostrado. Gerar de novo ou gerar mais pede outro "sim".
- Se o perfil da marca tiver `ia.limite_creditos_por_video`, respeite o limite. Acima dele, pergunte.
- **Não gerar pessoas reais,** logos, marcas de terceiros nem texto dentro do vídeo gerado. Textos e logo entram pela edição.
- B-roll sempre **sem áudio** (`generate_audio: false`, `sound: off`), no formato do vídeo final (9:16, 4:5…) e com a paleta da marca descrita no prompt.
- Anote os créditos gastos na entrega e em `historico.md`.

## Como acessar

### 1. Conexão (MCP do Higgsfield), quando existir

- `balance`: saldo e plano.
- `models_list` e `models_get`: catálogo e parâmetros.
- `show_generations`: gerações já feitas, para reaproveitar.
- `import-claude-motion-from-url`: manda o vídeo final para a biblioteca de mídia da pessoa no Higgsfield.

A conexão **não gera** mídia nem recebe upload de arquivos. Para gerar, use o navegador.

### 2. Navegador (site higgsfield.ai, na conta da pessoa)

Use o navegador preferido da pessoa. Antes do primeiro passo, leia a skill do navegador, se estiver listada.

1. Abra higgsfield.ai. Se não estiver logado, peça para a pessoa entrar. Nunca digite senha.
2. Escolha o modelo, envie a mídia de entrada (o vídeo bruto ou um quadro dele) e preencha o prompt e os parâmetros.
3. **Pare antes de clicar em gerar:** mostre o custo que o site exibe e o saldo, e espere o "sim".
4. Gere, espere terminar e baixe o resultado. Baixar arquivo também pede permissão: diga o nome e o tamanho.

### 3. Trazer o arquivo gerado para a edição

Os arquivos do Higgsfield ficam num CDN que o ambiente do Claude normalmente não acessa. Caminhos, do mais simples ao mais trabalhoso:

- Se o computador da pessoa estiver conectado, com uma pasta liberada (ex.: Downloads), traga o arquivo baixado pelo navegador.
- Peça para a pessoa anexar o arquivo na conversa.
- Se a pessoa liberar o domínio do CDN nas configurações de rede do Claude, baixe direto pela URL de `show_generations`.

## Prompts de B-roll (modelo)

```
Vertical 9:16, 4 seconds, cinematic, shallow depth of field, soft natural light.
[cena concreta que ilustra a frase: ex. "close-up of hands filling a spreadsheet on a laptop in a modern office"].
Color palette: [cores da marca em palavras: warm orange accents, cream and charcoal tones].
No text, no logos, no faces in focus, slow camera push-in. Silent.
```

Escreva o prompt em inglês (os modelos rendem melhor). Descreva a cena, não a mensagem. Evite pedir rostos nítidos de pessoas, para não parecer um personagem falso no vídeo de alguém real.

## No config

- Upscale: `"video_hd": "bruto_hd.mp4"`. Ele substitui a imagem do bruto, mas o recorte e o tempo continuam vindo do bruto original. Use a mesma duração e o mesmo enquadramento do bruto.
- B-roll: `"insercoes": [{"arquivo": "broll1.mp4", "de": {...}, "ate": {...}, "inicio_clip": 0, "transicao": 0.15, "zoom_lento": 0.06}]`. A voz continua por baixo, e legendas e elementos ficam por cima. Bom para 1,5 a 3 s, no meio de uma frase explicativa, nunca no gancho nem na chamada para ação.
