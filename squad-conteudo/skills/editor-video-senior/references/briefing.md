# Briefing

Pergunte só o que falta. Tudo é opcional: sem resposta, vale o padrão entre parênteses, e a entrega diz o que foi assumido. Se a marca tem arquivo em `marcas/`, ele substitui os padrões.

## Rodada 1 (AskUserQuestion, até 4 perguntas)

1. **Formato:** Reels/Stories/TikTok 9:16 (padrão) · Feed 4:5 · YouTube 16:9 · Quadrado 1:1
2. **Objetivo:** Inscrição ou evento (padrão quando a fala tem data) · Venda · Autoridade/educativo · Institucional
3. **Ritmo:** Dinâmico, com cortes secos e zoom (padrão) · Editorial calmo · Documental · Bem-humorado. Com vídeo de referência, a referência manda.
4. **Legendas:** Palavra por palavra com destaque (padrão) · Frase inteira · Sem legenda

## Rodada 2 (só se precisar)

5. **Público-alvo**, opcional: executivos e RH · jovens · pequenos empresários · clientes finais · outro. Sem resposta: deduzir pela fala e pela marca.
   - Executivos e 45+: ritmo mais calmo, legenda maior, menos elementos, tela final mais longa.
   - Jovens: cortes mais curtos, mais elementos, legenda com uma ou duas palavras por vez.
   - Pequenos empresários: clareza acima de tudo, números e benefícios em destaque.
6. **Efeito de profundidade** (texto atrás da pessoa e fundo desfocado): sim (padrão com pessoa em quadro) · não
7. **CTA e tela final:** o que a pessoa deve fazer, qual link ou caminho, qual data. Sem resposta: "link na bio", e avisar.
8. **Duração:** o mais curto sem perder conteúdo (padrão) · 15 s · 30 s · 60 s

IA generativa (Higgsfield ou similar) **não** entra no briefing. Ela só é oferecida no Passo 3b, com custo e saldo, se fizer diferença para o vídeo. O perfil da marca pode guardar `"ia": {"usar": true, "limite_creditos_por_video": 40}` ou `"usar": false`.

Pergunte em texto, junto com a rodada, pelos materiais que faltam: brandbook ou site, logo em PNG, trilha, vídeo de referência, B-roll. Pergunte também por nomes próprios e pelo que evitar.

## Lendo o brandbook

Com WebFetch (site) ou lendo o PDF, extraia:

- **Cores** com hex e função: primária, secundária, fundo claro, tinta (escuro), branco. No config elas viram `primaria`, `secundaria`, `fundo`, `tinta` e `branco`.
- **Fontes:** a de títulos e a de texto. O motor baixa do @fontsource pelo nome (ex.: "anton", "montserrat", "bebas-neue", "inter"). Se a fonte da marca não existir lá, use a mais parecida e avise.
- **Logo:** versões e regras (área de proteção, fundos permitidos). Se o site estiver bloqueado na rede do ambiente, peça o PNG.
- **Elementos gráficos:** setas, cantoneiras, texturas, granulado.
- **Movimento:** curvas e durações de animação, se houver. Padrão: cubic-bezier(.16,1,.3,1) com 520 ms.
- **Tom de voz:** guia o texto dos elementos e da tela final.

Sem brandbook: tire as cores do site ou do logo. Na falta dos dois, use uma paleta neutra e elegante (tinta #141416, fundo #F4EFE8, uma cor de destaque) e avise.

Depois da primeira entrega aprovada, salve a identidade em `marcas/<marca>.json` (Passo 8), para não perguntar de novo.
