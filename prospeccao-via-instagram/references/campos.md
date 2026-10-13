# Formato dos dados

Uma linha JSON por perfil em `trabalho/perfis.jsonl`. Campos ausentes podem ficar vazios ou ser omitidos.

```json
{
  "handle": "petshopamigofiel",
  "nome": "Amigo Fiel Pet Shop",
  "url": "https://www.instagram.com/petshopamigofiel/",
  "tema": "Pet shops e clínicas veterinárias",
  "cidade": "Londrina",
  "categoria": "Pet shop",
  "seguidores": 3480,
  "ultimo_post": "2026-09-28",
  "bio": "Banho, tosa e acessórios · Zona Sul",
  "link_bio": "https://linktr.ee/amigofielpet",
  "contato_publico": {"email": "", "whatsapp": "", "site": "", "fonte": "bio"},
  "sinais": [
    {"texto": "Segunda unidade abre em outubro no Centro", "fonte": "legenda", "data": "2026-09-12"}
  ],
  "pessoas": [
    {"handle": "fulana.silva", "nome": "Fulana Silva", "papel": "Proprietária"}
  ],
  "aderencia": 38,
  "sinal": 40,
  "atividade": 20,
  "motivo": "Post de 12/09 anuncia a segunda unidade no Centro em outubro.",
  "mensagem": "",
  "fonte_busca": "#petshoplondrina",
  "coletado_em": "2026-10-09"
}
```

## Regras

- `handle` sem o @ e em minúsculas. É a chave única.
- Datas no formato AAAA-MM-DD.
- `sinais` só com trechos reais e a data de onde saíram.
- `pessoas` só adultos que aparecem publicamente como responsáveis (ver Cuidados no SKILL.md).
- `contato_publico.fonte`: "bio", "botão de contato" ou "link da bio".
- Se `aderencia`, `sinal` ou `atividade` faltarem, o script assume 0 para o que falta e calcula a atividade pela data do último post.

## Colunas da aba Leads

Pontuação · @ · Nome · Cidade · Seguidores · Último post · Sinal encontrado · Motivo · E-mail · WhatsApp · Site · Mensagem sugerida · Perfil (link) · Busca de origem
