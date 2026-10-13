# Formatos

## Briefing em `trabalho/briefing.json`

```json
{
  "oferta": "software de gestão de benefícios",
  "segmentos": ["tecnologia", "software"],
  "cargos": [
    {"termo": "cfo", "peso": "principal"},
    {"termo": "diretor financeiro", "peso": "principal"},
    {"termo": "head de pessoas", "peso": "secundario"}
  ],
  "senioridades": ["C-level", "Diretoria"],
  "portes": ["51-200", "201-500"],
  "regioes": ["SP", "São Paulo"],
  "sinais": ["vagas", "crescimento", "novo_no_cargo"]
}
```

- Portes: `1-10`, `11-50`, `51-200`, `201-500`, `501-1000`, `1001-5000`, `5000+`.
- Senioridades: `C-level`, `Diretoria`, `Gerência`, `Coordenação`, `Especialista`, `Analista`.
- Sinais: `vagas`, `crescimento`, `novo_no_cargo`, `post`, `investimento`, `expansao`.

## Um decisor por linha em `trabalho/pessoas.jsonl`

```json
{"nome": "Marina Exemplo", "cargo": "CFO", "empresa": "Nuvem Ágil Software",
 "segmento": "Tecnologia da informação", "colaboradores": "180", "localizacao": "São Paulo, SP",
 "sinais": [{"tipo": "vagas", "evidencia": "3 vagas abertas em Financeiro (out/2026)"},
            {"tipo": "crescimento", "evidencia": "+22% de funcionários em 6 meses (Apollo)"}],
 "no_cargo_desde": "2026-07", "fonte": "Apollo", "confirmado": true,
 "url": "https://www.linkedin.com/in/marina-exemplo/", "site": "https://nuvemagil.example",
 "nota_convite": "", "observacao": ""}
```

- `url` é a chave única (o script normaliza www, barra final e parâmetros).
- `sinais` só com `evidencia` preenchida contam na nota.
- `fonte`: `Apollo`, `Google` ou `LinkedIn`. `confirmado: true` quando o perfil foi aberto e conferido.

## Nota (0 a 100)

| Parte | Pontos |
|---|---|
| Cargo | 35 se bate com um cargo principal; 20 se secundário; 15 se só a senioridade bate. Sem cargos no briefing, pela senioridade (C-level 35, Diretoria 30, Gerência 22, Coordenação 15). |
| Segmento | 20 se o setor ou o nome da empresa contém um segmento-alvo (10 se não houver segmentos definidos) |
| Porte | 15 se o número de funcionários está numa faixa escolhida (7 se não houver portes definidos) |
| Região | 10 se a localização contém uma região-alvo (5 se não houver regiões definidas) |
| Sinais | 10 por sinal escolhido com evidência, até 20 |

Prioridade: **Alta** ≥ 70 · **Média** ≥ 45 · **Baixa** abaixo disso.
