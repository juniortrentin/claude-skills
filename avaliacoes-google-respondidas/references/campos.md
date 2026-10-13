# Formatos

## `trabalho/negocio.json`

```json
{"nome": "Pizzaria Forno Bom", "assinatura": "Rafa, da Forno Bom", "cor": "#b5442c",
 "tom": "próximo", "emoji": false,
 "pode_citar": ["estamos contratando mais um entregador para sexta e sábado"],
 "melhorias": ["Tempo de entrega no fim de semana: 4 reclamações falam de demora..."]}
```

- `assinatura`: o script avisa se alguma resposta não tem.
- `cor`: cabeçalho do relatório.
- `pode_citar`: mudanças confirmadas pelo dono que podem aparecer nas respostas.
- `melhorias`: até 3 frases para o relatório, escritas com base nas avaliações.

## `trabalho/avaliacoes.jsonl` (uma avaliação por linha)

```json
{"id": "r2", "autor": "Carlos M.", "estrelas": 2, "data": "2026-10-04",
 "texto": "Pedi pelo delivery numa sexta e demorou 1h40. Chegou fria. Uma pena porque a pizza é boa.",
 "respondida": false, "resposta_existente": "",
 "temas": {"demora": "-", "entrega": "-", "qualidade": "+"}, "equipe": [],
 "cuidado": "", "destaque": "", "resposta": "Carlos, obrigado por contar..."}
```

| Campo | O que é |
|---|---|
| `autor` | primeiro nome e inicial, como no Google |
| `data` | AAAA-MM-DD; se aproximada, `"data_aproximada": true` |
| `respondida` / `resposta_existente` | se já tem resposta do proprietário |
| `temas` | `{"tema": "+"}` para elogio, `"-"` para reclamação. Também aceita lista (o lado vem das estrelas) |
| `equipe` | funcionários citados pelo cliente |
| `cuidado` | motivo, se for caso de `cuidado.md`; vazio se não |
| `destaque` | trecho curto de elogio para o relatório |
| `resposta` | resposta sugerida |

Se `temas` vier vazio, o script marca por palavras-chave (reserva, menos precisa).

## Temas comuns

atendimento · demora · preço · qualidade · limpeza · ambiente · entrega · estacionamento · agendamento · pós-venda

Crie temas do negócio quando ajudarem a decidir: "massa", "sabor", "corte", "anestesia", "tamanho da porção", "Wi-Fi". Mantenha o mesmo nome do tema de um mês para o outro.

## Prioridade na aba Responder

1. **Cuidado:** casos de `cuidado.md`.
2. **Reclamação:** 1 ou 2 estrelas. Responder em até 2 dias.
3. **Elogio com ressalva:** 3 estrelas, ou 4 e 5 com algum tema "-".
4. **Elogio.**
