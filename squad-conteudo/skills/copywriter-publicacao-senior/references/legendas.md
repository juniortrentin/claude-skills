# Como escrever as legendas

## Estrutura de cada versão

1. **Gancho (primeira linha):** até 125 caracteres. É o que aparece antes do "mais". Diga a novidade, o benefício ou a curiosidade. Nunca comece com "Olá, pessoal" ou com hashtag.
2. **Corpo (1 a 4 linhas curtas):** completa o vídeo. O vídeo mostra, a legenda explica o porquê, dá o detalhe prático ou conta o bastidor. Uma ideia por linha.
3. **Chamada para ação:** um pedido só, claro e no imperativo. Exemplos: "Siga @marca", "Marca aqui quem vai com você", "Comenta qual foi o seu favorito", "Passa lá", "Link na bio".
4. **Hashtags:** no fim, de 3 a 5. Uma da marca, uma ou duas do nicho e uma ou duas do tema do post.

## As 3 versões (abordagens diferentes)

| Versão | Quando funciona | Forma |
|---|---|---|
| **Curta** | quem rola rápido; vídeo que já se explica | gancho + 1 ou 2 linhas + chamada |
| **Bastidores / história** | marcas próximas, pequenos negócios, eventos | começa por um momento ou sentimento, conta o "como", fecha com convite |
| **Chamada direta** | evento, oferta, lançamento | a informação principal primeiro, depois a chamada, curta e objetiva |

Outras abordagens para trocar uma das três, conforme o objetivo:

- **Pergunta:** puxa comentário ("Qual dessas cores é a sua?").
- **Lista:** "3 motivos para…", boa para conteúdo educativo.
- **Prova:** número ou resultado confirmado, nunca inventado.
- **Urgência:** só com prazo real ("só até sábado").

## Tom

- Siga `tom` do perfil da marca. Sem perfil: marcas de varejo, infantil e papelaria → leve, próximo, com 1 a 3 emojis; B2B e educação corporativa → direto, sem gírias, no máximo 1 emoji; LinkedIn → primeira pessoa e frases completas.
- Reaproveite o bordão e a assinatura da marca quando existirem (ex.: "Vem se encantar!").
- Escreva como a marca fala com o cliente no balcão, não como um anúncio.
- Português do Brasil, sem erros. "Pra" e "tá" só se a marca fala assim.

## Hashtags

- Prefira as específicas ao gigantes: #papelariafofa é melhor que #love.
- Não repita a mesma lista em todo post. Mantenha 1 ou 2 fixas da marca (`hashtags_fixas`) e varie o resto pelo tema.
- Hashtag de cidade, bairro ou evento só com o local confirmado.
- Sem acento, sem espaço, sem pontuação: `#materialescolar`, não `#material-escolar`.

## Texto alternativo

Uma ou duas frases que descrevem o que aparece, para quem usa leitor de tela: quem, onde, o quê. Sem hashtags e sem chamada para ação.

## Formato do textos.json (para o `checar`)

```json
{
  "marca": "Nome",
  "plataformas": ["instagram"],
  "fatos_confirmados": ["nome do local", "27 de outubro", "@marca"],
  "max_emojis": 4,
  "variantes": [
    {"rotulo": "Curta", "texto": "Gancho\nCorpo\nChamada", "hashtags": ["marca", "nicho", "tema"]},
    {"rotulo": "Shorts", "titulo": "Título até 100 caracteres", "texto": "...", "hashtags": ["marca"]}
  ]
}
```

`fatos_confirmados` lista o que veio da pessoa, do briefing ou do próprio vídeo (texto na tela, banner, fala). O `checar` aponta como `[confirmar]` toda data, horário, preço, porcentagem, @ ou local que não estiver ali.
