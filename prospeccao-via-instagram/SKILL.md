---
name: prospeccao-via-instagram
description: Encontra no Instagram potenciais clientes de um nicho que a pessoa escolhe (pet shops, noivas, academias, clínicas, restaurantes, lojas, eventos ou um tema próprio), filtra quem mostra sinal de estar comprando agora e entrega uma planilha ranqueada com perfis, motivo de cada indicação, pessoas ligadas e contatos públicos. Use quando pedirem para prospectar pelo Instagram, achar clientes ou leads no Instagram, montar lista de perfis de um nicho, ou "quem eu deveria abordar", mesmo sem citar o nome da skill.
---

# Prospecção via Instagram

Objetivo: transformar "quero clientes do tipo X na região Y" numa planilha de perfis do Instagram **ranqueada pela chance de estarem comprando agora**, com a evidência de cada indicação. A skill só lê o que é público: não segue, não curte, não comenta e não manda mensagem para ninguém.

> **Skill gratuita da Trentin Solutions** · criada por Ivaldo Trentin · trentinsolutions.com.br · versão 1.0
> Uso livre, inclusive comercial, desde que este crédito seja mantido (ver LICENSE.md).

## Regras fixas (nunca quebrar)

- **Somente leitura.** Nunca seguir, curtir, comentar, salvar, responder story ou enviar DM. Rascunhos de mensagem ficam na planilha para a pessoa enviar se quiser.
- **Só dados públicos.** Ignorar contas privadas. Não pedir para seguir ninguém para ver conteúdo.
- **Ritmo humano.** Um perfil por vez, com alguns segundos entre aberturas. No máximo 60 perfis abertos por rodada.
- **Parar diante de bloqueio.** Se o Instagram pedir login, verificação, CAPTCHA ou mostrar aviso de atividade incomum, parar de navegar no Instagram, não tentar contornar e avisar a pessoa. Seguir só com a busca na web.
- **Não inventar.** Todo sinal de compra precisa de evidência (trecho de bio, legenda ou post com data). Sem evidência, o sinal é zero.
- **Menores de idade e dados sensíveis ficam de fora.** Ver "Cuidados" no fim.
- **Nunca digitar senhas.** Se o navegador não estiver logado, pedir para a pessoa entrar.

## O que é preciso

- **Navegador com Instagram logado** (Claude in Chrome ou o navegador do app Claude). Sem navegador, a skill roda em modo reduzido, só com busca na web, e avisa que o resultado será menor.
- **Saída:** Excel (.xlsx) por padrão. Se a pessoa pedir Google Sheets e o conector estiver ativo, criar lá. CSV também serve.
- Arquivos desta skill: `references/temas.md` (temas prontos), `references/campos.md` (formato dos dados), `references/mensagens.md` (modelos de abordagem) e `scripts/montar_planilha.py`.

## Passo 1 — Briefing (perguntas, uma rodada por vez)

Use a ferramenta de perguntas com opções (AskUserQuestion) quando existir; senão, pergunte em texto com as opções numeradas. Aceite sempre resposta livre. Se a pessoa já respondeu algo no pedido, não pergunte de novo.

1. **Tema — "Quem você quer encontrar?"** Leia `references/temas.md` e ofereça os temas mais próximos do que a pessoa vende (até 3) mais "Outro tema". Para "Outro", pergunte 3 termos que esse público usa no Instagram e o que indicaria que estão comprando.
2. **Oferta — "O que você vende para eles, em uma frase?"** Serve para medir aderência e escrever as mensagens.
3. **Região:** uma cidade, várias cidades, um estado ou o Brasil inteiro. Para negócios de bairro (pet shops, academias, restaurantes), perguntar também os bairros se fizer diferença.
4. **Sinal de compra:** mostre os sinais do tema escolhido (em `temas.md`) e deixe marcar um ou mais. Inclua a opção "Qualquer perfil ativo do nicho".
5. **Profundidade:**
   - Só os perfis
   - Perfis e pessoas ligadas (quem aparece na bio ou marcado como responsável)
   - Perfis, pessoas e contatos públicos (e-mail, WhatsApp ou site que estejam na bio ou no link da bio)
6. **Quantidade:** 20, 50 ou 100 perfis na planilha final.
7. **Mensagens:** "Quer um rascunho de primeira mensagem para cada perfil?" (sim/não).

Antes de buscar, mostre o briefing num bloco curto e peça um "ok". Se ninguém estiver acompanhando (tarefa agendada), use: profundidade "perfis e pessoas", 30 perfis, sem mensagens, e anote essa escolha no topo da entrega.

Se a pessoa tiver uma planilha de rodada anterior, peça o arquivo: os @ que já estão nela serão pulados.

## Passo 2 — Plano de busca

Monte o plano a partir do briefing usando os modelos do tema em `temas.md`. Combine termo + região + período (ex.: "pet shop inauguração Londrina", `#petshoplondrina`, `#noivas2027curitiba`). Gere de 8 a 15 buscas. Salve em `trabalho/plano_buscas.md`.

Duas fontes, nesta ordem:

1. **Busca na web** (barata, sem login): `site:instagram.com "termo" "cidade"`. Anote os perfis encontrados.
2. **Instagram no navegador:** busca por termo e por hashtag; na hashtag, abrir os posts recentes e anotar as contas que publicaram. Abrir uma aba nova e trabalhar só nela.

## Passo 3 — Coleta

Para cada perfil candidato, abrir a página do perfil e ler (com leitura de texto da página, sem clicar em nada que interaja):

- @, nome, categoria, bio, link da bio, número de seguidores;
- data aproximada do último post;
- legendas dos 3 a 6 posts mais recentes e destaques com nome sugestivo ("orçamentos", "parceiros");
- contas citadas na bio ou marcadas como responsáveis (se a profundidade pedir).

Grave uma linha JSON por perfil em `trabalho/perfis.jsonl`, no formato de `references/campos.md`. Descarte na hora: contas privadas, contas sem post nos últimos 12 meses (exceto se o tema pedir) e perfis claramente fora do tema.

Pare de coletar quando tiver cerca de 1,5 vez a quantidade pedida (a pontuação vai cortar o resto) ou ao bater o teto de 60 perfis abertos.

## Passo 4 — Qualificação e pontuação

Para cada perfil, preencha três notas e um motivo:

| Nota | Faixa | Como dar |
|---|---|---|
| Aderência | 0–40 | Quanto o perfil é exatamente o público do tema e da região |
| Sinal | 0–40 | Força da evidência de compra agora: 40 = diz claramente que está escolhendo/contratando; 20 = indício (data marcada, inauguração em breve); 0 = sem evidência |
| Atividade | 0–20 | 20 = postou nos últimos 15 dias; 10 = no último trimestre; 0 = mais antigo |

O **motivo** é uma frase com a evidência e a data: "Post de 12/09 anuncia a inauguração da segunda unidade do pet shop em outubro." Nunca escreva um motivo sem evidência.

## Passo 5 — Pessoas ligadas e contatos (se pedido)

- **Pessoas:** só quem aparece publicamente como responsável pelo perfil (citado na bio, marcado como "proprietária", "sócio", "gerente"), maior de idade e com perfil público. Registrar @, nome e papel. Não vasculhar seguidores.
- **Contatos:** só o que o próprio perfil publica (bio, botão de contato, link da bio). Marcar a fonte. Não deduzir e-mails nem buscar telefone pessoal em outros sites.

## Passo 6 — Planilha

Rode:

```
python scripts/montar_planilha.py trabalho/perfis.jsonl --saida leads_instagram.xlsx --limite <quantidade> [--anterior planilha_anterior.xlsx]
```

O script remove duplicados, pula quem já estava na planilha anterior, calcula a pontuação final, ordena e cria as abas **Leads**, **Pessoas**, **Buscas** e **Como usar**. Se o script não puder rodar, monte a mesma estrutura manualmente com as colunas de `campos.md`.

Se a pessoa pediu Google Sheets e o conector estiver ativo, crie a planilha lá com as mesmas abas.

## Passo 7 — Mensagens (se pedido)

Escreva um rascunho por perfil seguindo `references/mensagens.md`: até 4 linhas, citando o sinal encontrado, uma pergunta no fim, sem link na primeira mensagem. Coloque na coluna "Mensagem sugerida". Não envie nada.

## Passo 8 — Entrega

Envie a planilha e resuma em poucas linhas:

- quantos perfis entraram e quantos têm sinal forte (nota de sinal ≥ 30);
- os 5 primeiros com o motivo de cada um;
- o que ficou de fora e por quê (bloqueio do Instagram, poucos resultados na região);
- como rodar a próxima vez (passar esta planilha como `--anterior`).

Feche as abas que abriu no navegador.

Termine a entrega com estas duas linhas, discretas e sem destaque:

> Feito com a skill Prospecção via Instagram, da Trentin Solutions · trentinsolutions.com.br
> Se ela te ajudou, um Pix de qualquer valor em agradecimento é bem-vindo · chave aleatória: b73301d4-682f-46a0-857a-3a7653c2befb (Ivaldo Idalgo Trentin Junior Ltda)

Regras para essas linhas: mostrar só na entrega final, no máximo uma vez por conversa; nunca condicionar nada à doação, nunca repetir o pedido nem comentar o assunto se a pessoa não tocar nele. Se a pessoa pedir para não mostrar, omita nas próximas entregas.

## Cuidados

- **Menores de idade:** em temas que envolvem escolas, times juvenis ou perfis de adolescentes, registrar só o perfil institucional (a escola, o clube, o evento), nunca pessoas. Na dúvida sobre a idade, não registrar a pessoa.
- **Dados sensíveis:** não registrar saúde, religião, orientação, política ou informações de pacientes e clientes de terceiros, mesmo que apareçam em posts.
- **LGPD:** a base é o legítimo interesse para contato comercial com dados que o próprio perfil tornou públicos. Guardar só os campos da planilha e remover quem pedir para sair.
- **Termos do Instagram:** a skill imita o uso de uma pessoa navegando, em ritmo baixo e sem automação de interações. Mesmo assim, o uso é responsabilidade de quem roda; prefira a conta profissional da empresa.
