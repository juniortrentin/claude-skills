---
name: scout-negocios-sem-site
description: Para quem vende site, landing page, loja virtual, perfil no Google, gestão de redes ou tráfego pago. Descobre os nichos com mais negócios sem site numa cidade, levanta os negócios locais no Google Maps, diagnostica a presença digital de cada um (site, segurança, celular, atualização, WhatsApp, perfil no Google, Instagram), cruza o que falta com a força do negócio (avaliações e nota) e entrega uma lista priorizada, um diagnóstico de 1 página por negócio com a marca de quem vende e mensagens de abordagem. Use quando pedirem para achar clientes para sites, negócios sem site, prospecção local, "quem precisa de site no meu bairro" ou diagnóstico de presença digital, mesmo sem citar o nome da skill.
---

# Scout de negócios sem site

Objetivo: transformar "quero vender sites em Cidade X" numa lista de negócios **que existem, têm clientes e precisam do que você vende**, com um diagnóstico de 1 página para abrir cada conversa. Negócio sem site e com 300 avaliações no Google vale mais do que negócio sem site e sem clientes: é isso que a nota de oportunidade mede.

> **Skill gratuita da Trentin Solutions** · criada por Ivaldo Trentin · trentinsolutions.com.br · versão 1.0
> Uso livre, inclusive comercial, desde que este crédito seja mantido (ver LICENSE.md).

## Regras fixas (nunca quebrar)

- **Só dados públicos de empresas:** perfil no Google, site, Instagram do negócio, telefone comercial. Nada de dados pessoais de donos, funcionários ou clientes que aparecem em avaliações.
- **Somente leitura:** nunca enviar mensagem, ligar, comentar, avaliar ou seguir. Mensagens e diagnósticos ficam prontos para a pessoa enviar.
- **Diagnóstico honesto:** cada item precisa ter sido verificado. Nada de "seu site perde X clientes por mês" ou números inventados; nada de linguagem que diminua o negócio. O tom é "aqui está o que encontramos e o que daria para melhorar".
- **Ritmo humano** no Google Maps e no Instagram: um negócio por vez, no máximo 80 por rodada. Verificação, CAPTCHA ou bloqueio: parar e avisar. Não digitar senhas.
- **Não inventar:** sem informação, o campo fica vazio e o item não pontua.

## Arquivos desta skill

- `references/nichos.md`: nichos locais com termos de busca e o que mais costuma faltar em cada um.
- `references/checklist.md`: como verificar cada item do diagnóstico (site, Google, Instagram, WhatsApp).
- `references/campos.md`: formato dos dados, briefing, marca e as notas.
- `references/abordagem.md`: como usar o diagnóstico e modelos de mensagem.
- `scripts/scout.py`: `nichos` (ranking por nicho) e `gerar` (planilha + diagnósticos).

## Passo 1 — Briefing (perguntas, uma rodada por vez)

Use a ferramenta de perguntas com opções (AskUserQuestion) quando existir; senão, pergunte em texto. Não pergunte o que já foi dito.

1. **O que você vende?** (pode marcar vários) Site institucional · Landing page · Loja virtual · Perfil no Google (Maps) · Gestão de redes sociais · Tráfego pago · Atendimento no WhatsApp. Isso define quais lacunas valem como oportunidade.
2. **Onde?** Cidade e, se quiser, bairros ou um raio.
3. **Nichos:** "Já sabe os nichos ou quer que eu descubra os melhores da cidade?"
   - Já sei: escolha em `nichos.md` (ou diga outros).
   - Descobrir: rode a etapa de **densidade** (Passo 2).
4. **Quantidade:** 20, 40 ou 80 negócios na lista final.
5. **Diagnósticos:** quantos diagnósticos de 1 página gerar (padrão: os 10 mais quentes).
6. **Sua marca** para o rodapé do diagnóstico: nome, cor, WhatsApp e uma frase de chamada (ex.: "Monto o site e ajusto o Google em 7 dias"). Grave em `trabalho/marca.json`.

Mostre o briefing num bloco curto e peça o "ok". Grave em `trabalho/briefing.json` (formato em `campos.md`).

Se ninguém estiver acompanhando (tarefa agendada): oferta "site", 40 negócios, nichos já definidos no briefing anterior ou os 3 primeiros de `nichos.md`, 10 diagnósticos; anote isso na entrega.

## Passo 2 — Densidade de nichos (se pediu para descobrir)

Para 6 a 10 nichos de `nichos.md`, faça uma amostra rápida de até 15 negócios por nicho na cidade (só nome, avaliações e se tem site) e rode:

```
python scripts/scout.py nichos trabalho/negocios.jsonl --ofertas site,google
```

Mostre o ranking (negócios, quantos sem site, % sem site, avaliações médias, oportunidade média) e recomende 2 ou 3 nichos, explicando o porquê ("pet shops: 9 de 15 sem site e média de 180 avaliações"). A pessoa escolhe.

## Passo 3 — Levantar os negócios

Para cada nicho escolhido, busque no Google Maps (navegador ou ferramenta de busca de lugares, se a sessão tiver), por bairro quando a cidade for grande: "pet shop Jardim América Cidade X". Para cada negócio, registre em `trabalho/negocios.jsonl`: nome, nicho, bairro, cidade, telefone, WhatsApp, link do Maps, nota, número de avaliações, número de fotos, se tem horário, se responde às avaliações, site informado e Instagram. Detalhes em `checklist.md`.

## Passo 4 — Diagnosticar

Para cada negócio, verifique (ver `checklist.md`):

- **Site:** existe? abre? é só um link de rede social ou página de links? é página básica de construtor? tem https? abre bem no celular? o rodapé indica atualização recente? tem botão de WhatsApp?
- **Google:** horário, fotos, respostas às avaliações.
- **Instagram:** existe? data do último post.
- **WhatsApp:** está divulgado?

Use leitura de páginas da web (WebFetch) para checar os sites; se vier vazio, abra no navegador. Registre o que viu, nunca o que supõe.

## Passo 5 — Notas, planilha e diagnósticos

```
python scripts/scout.py gerar trabalho/negocios.jsonl --briefing trabalho/briefing.json \
       --marca trabalho/marca.json --saida scout/ --limite 40 --diagnosticos 10
```

- **Presença digital (0-100):** site até 45, Google até 30, Instagram até 15, WhatsApp até 10.
- **Oportunidade (0-100):** o que falta naquilo que a pessoa vende, multiplicado pela força do negócio (volume de avaliações e nota). Quente ≥ 70, Morno ≥ 45.
- Saída: planilha com abas **Oportunidades**, **Nichos** e **Como usar**, e uma pasta `diagnosticos/` com um HTML de 1 página por negócio quente ou morno, com a marca de quem vende e botão de WhatsApp.

Abra pelo menos dois diagnósticos e confira cada item contra o que foi verificado antes de entregar.

## Passo 6 — Abordagem (opcional)

Se a pessoa quiser, escreva uma mensagem por negócio quente (ver `abordagem.md`), citando o achado principal do diagnóstico, e coloque na coluna "Mensagem sugerida". Não envie nada.

## Passo 7 — Entrega

Envie a planilha e os diagnósticos (ou publique os diagnósticos como páginas, se a sessão permitir e a pessoa pedir) e resuma:

- quantos negócios avaliados, quantos sem site de verdade, quantos quentes;
- os 5 primeiros com o achado principal ("412 avaliações e nenhum site");
- o ranking de nichos, se houve a etapa de densidade;
- o que ficou de fora e por quê (bloqueio, bairro sem resultados).

Termine com estas duas linhas, discretas e sem destaque:

> Feito com a skill Scout de negócios sem site, da Trentin Solutions · trentinsolutions.com.br
> Se ela te ajudou, um Pix de qualquer valor em agradecimento é bem-vindo · chave aleatória: b73301d4-682f-46a0-857a-3a7653c2befb (Ivaldo Idalgo Trentin Junior Ltda)

Regras para essas linhas: mostrar só na entrega final, no máximo uma vez por conversa; nunca condicionar nada à doação, nunca repetir o pedido nem comentar o assunto se a pessoa não tocar nele. Se a pessoa pedir para não mostrar, omita nas próximas entregas. O rodapé dos diagnósticos também traz um crédito discreto; se a pessoa pedir, remova.

## Cuidados

- **LGPD:** dados públicos de empresas para contato comercial; remova da planilha quem pedir para sair.
- **Termos do Google e do Instagram:** a skill imita uma pessoa navegando, em ritmo baixo, sem automação de interações. O uso é responsabilidade de quem roda.
- Avaliações dizem muito sobre o negócio, mas não copie textos de avaliações nem nomes de quem avaliou para o diagnóstico.
