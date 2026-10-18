# O que é verificado

Gravidade: **erro** (precisa corrigir antes de publicar, -12 pontos), **alerta** (vale corrigir, -4 pontos), **info** (só registro). Nota inicial 100.

Veredito:

- **aprovado:** nenhum erro e nota 85 ou mais;
- **ajustes:** até 2 erros e nota 60 ou mais;
- **reprovado:** o resto.

Achados marcados como falso positivo (`"confirmado": false`) não contam.

| Categoria | Verificação | Gravidade | Como o script mede |
|---|---|---|---|
| formato | proporção, resolução, duração máxima, fps, codec | erro/alerta | ffprobe e tabela de `plataformas.md` |
| som | volume médio fora de -14 LUFS ±2 (±4 vira erro) | alerta/erro | ebur128 |
| som | pico acima de -0,5 dBFS (estouro) | erro | ebur128 true peak |
| cortes | fala começa no primeiro quadro | alerta | energia nos primeiros 30 ms |
| cortes | fala colada no fim (última palavra cortada) | erro | fim da transcrição a menos de 0,12 s do fim |
| cortes | emenda no meio da fala (palavra cortada) | alerta | corte de cena com fala dos dois lados e um "buraco" de energia de 10-30 ms no corte |
| cortes | estalo no corte | alerta | salto de amostra muito acima do normal |
| imagem | tela preta | erro (alerta no começo) | blackdetect |
| imagem | imagem parada por mais de 1,2 s (fora da tela final) | alerta | freezedetect |
| imagem | 3 ou mais flashes por segundo | erro | luminância quadro a quadro |
| legibilidade | texto encostado ou cortado na borda | erro (alerta se decorativo) | caixas do OCR |
| plataforma | texto na área coberta pela interface do app | alerta | caixas do OCR e `plataformas.md` |
| pessoas | texto ou elemento sobre o rosto | erro | rosto (YuNet) com caixa de texto, quando a cor do texto ocupa mais de 15% da área do rosto |
| pessoas | rosto some por alguns quadros com texto na tela | alerta | sequência de quadros sem rosto |
| legendas | cobertura: palavras faladas que aparecem na legenda (abaixo de 60% é erro; abaixo de 90%, alerta) | erro/alerta | texto aprovado alinhado à transcrição e OCR numa janela de ±0,8 s |
| legendas | sincronia: atraso mediano acima de 0,35 s | alerta | primeira aparição na tela menos o tempo da fala |
| legendas | nome próprio escrito diferente (em 2 ou mais quadros) | erro | similaridade com os nomes do briefing |
| legendas | palavra diferente do texto aprovado (em 2 ou mais quadros) | alerta | similaridade com o vocabulário aprovado |
| legendas | velocidade acima de 25 caracteres/s | alerta | mudanças de texto na faixa de legenda |
| conteudo | número ou data na tela que não está na fala nem no briefing | alerta | OCR |
| marca | CTA ausente nos últimos 5 s | alerta | OCR e lista de CTA do briefing (ou palavras de ação) |
| marca | logo ausente no último segundo | alerta | comparação de imagem com o PNG do logo |
| marca | texto em cor fora da paleta | alerta | cor dominante do texto comparada à paleta |

## Limites conhecidos (por isso existe a conferência visual)

- O OCR ignora acentos e confunde O/0, I/1 e S/5. Palavra "diferente" pode ser só erro de leitura.
- Texto gigante atrás da pessoa aparece cortado pelo OCR (de propósito). Ele fica fora da checagem de grafia.
- Texto do cenário (camiseta, placa) é separado quando aparece em mais de 20% dos quadros no mesmo jeito.
- A detecção de rosto pode falhar de perfil ou com pouca luz.
- O tempo de cada palavra é estimado dentro das frases. A sincronia é aproximada (±0,2 s).

## Formato do briefing (sem o config do editor)

```json
{
  "plataforma": "reels",
  "fala_esperada": "texto do roteiro ou da legenda aprovada",
  "nomes_proprios": ["Marina Costa"],
  "fatos": ["27 de outubro", "R$ 97", "link na bio"],
  "textos_aprovados": ["WORKSHOP · ROI DE TREINAMENTO"],
  "cta": ["GARANTA SUA VAGA", "LINK NA BIO"],
  "logo": "logo.png",
  "cores": ["#f26522", "#F4EFE8", "#141416"],
  "legendas": true,
  "lufs_alvo": -14,
  "exigir_logo": true
}
```
