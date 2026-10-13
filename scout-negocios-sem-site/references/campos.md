# Formatos e notas

## Briefing em `trabalho/briefing.json`

```json
{"cidade": "Cidade Exemplo", "bairros": ["Centro", "Jardim"], "nichos": ["Pet shops", "Padarias"],
 "ofertas": ["site", "google"], "quantidade": 40}
```

Ofertas: `site`, `landing`, `loja`, `google`, `redes`, `trafego`, `whatsapp`. `nichos` vazio = todos os levantados.

## Marca em `trabalho/marca.json`

```json
{"nome": "Agência Exemplo", "cor": "#3a6ab4", "whatsapp": "(14) 99999-0000",
 "chamada": "Monto o site e ajusto o Google em 7 dias."}
```

## Um negócio por linha em `trabalho/negocios.jsonl`

```json
{"nome": "Padaria Pão Dourado", "nicho": "Padarias", "bairro": "Centro", "cidade": "Cidade Exemplo",
 "telefone": "(14) 3000-0001", "whatsapp": "", "maps_url": "https://maps.google.com/?cid=1",
 "nota": 4.7, "avaliacoes": 412, "fotos_maps": 35, "horario": true, "responde_avaliacoes": false,
 "site": "", "site_status": "sem_site", "https": null, "mobile": null, "ano_rodape": null,
 "whatsapp_no_site": null, "instagram": "@paodourado", "insta_ultimo_post": "2026-09-02",
 "mensagem": "", "observacoes": ""}
```

O script remove duplicados (mesmo nome e telefone).

## Presença digital (0 a 100)

| Parte | Pontos |
|---|---|
| Site | sem site 0 · só rede social ou com erro 5 · página básica 15 · site ok 25, +5 https, +5 celular, +5 atualizado (ano do rodapé ≥ ano passado), +5 WhatsApp no site (máx. 45) |
| Google | perfil 10, +5 horário, +5 dez ou mais fotos, +5 responde avaliações, +5 vinte ou mais avaliações (máx. 30) |
| Instagram | post nos últimos 30 dias 15 · perfil parado 7 · sem perfil 0 |
| WhatsApp | divulgado 10 |

## Oportunidade (0 a 100)

- **Lacuna** (0 a 1): quanto falta na parte que a pessoa vende. Site e landing olham o site; Google olha o perfil; redes olham o Instagram; tráfego olha site e Google; loja olha site e Instagram. Com várias ofertas, vale a maior lacuna.
- **Força do negócio** (0 a 1): volume de avaliações (escala logarítmica até 300) com peso 0,7, mais a nota (4,5+ vale 0,3; 4,0+ vale 0,2).
- **Oportunidade = 100 × lacuna^0,8 × (0,2 + 0,8 × força).**

Assim, um negócio forte com lacuna clara fica na frente de um negócio fraco em que falta tudo.

Prioridade: **Quente** ≥ 70 · **Morno** ≥ 45 · **Frio** abaixo disso.
