# Fontes, na ordem de uso

Use o navegador com as contas da pessoa já logadas (Claude in Chrome ou o navegador do app), sempre numa aba nova.

## 1. LinkedIn: conexões novas

- Abra `https://www.linkedin.com/mynetwork/invite-connect/connections/` e confirme a ordenação **"Adicionados recentemente"**.
- Leia a lista pelo texto da página (nome, título, "Conexão feita em…") e pegue as URLs dos perfis.
- Percorra de cima para baixo e **pare na primeira conexão cuja URL já está na planilha**: a lista é cronológica, então tudo abaixo já foi processado.
- Se todas as visíveis forem novas, role para carregar mais até achar uma já processada ou bater o limite da rodada. As que sobrarem ficam para a próxima; avise quantas.
- URL é a chave: `linkedin.com/in/<slug>`, sem parâmetros e sem barra final.

## 2. LinkedIn: contato e empresa (gratuito)

- Abra `https://www.linkedin.com/in/<slug>/overlay/contact-info/` e leia e-mail, telefone e site que a própria pessoa compartilhou com as conexões. Fonte: **LinkedIn**.
- No perfil, anote **cargo e empresa atual** (topo e experiência mais recente) e a localização. A empresa é essencial para o próximo passo.

## 3. Apollo, aplicativo web (gratuito até revelar)

- A extensão do Apollo abre num painel lateral que não é acessível à automação; use sempre o aplicativo web.
- Busque por nome + empresa: `https://app.apollo.io/#/people?page=1&qKeywords=<Nome%20Empresa>`. Sem resultado, tente só o nome e confira empresa e cidade.
- A tabela de resultados mostra, sem gastar crédito: cargo, empresa, localização, número de colaboradores e setor.
- Classifique a correspondência:

| Confiança | Critério |
|---|---|
| Alta | Nome e empresa atual batem |
| Média | Nome bate; cidade ou área batem; empresa diferente ou ausente |
| Baixa | Só o nome bate, ou há homônimos sem como desempatar |

- **Revelar** (só depois da aprovação do Passo 5): botão de acesso ao e-mail da linha da pessoa. "Sem e-mail" também gasta a tentativa: registre "Apollo: sem e-mail". E-mail marcado como catch-all vai com a observação "não verificado". Telefone só se aprovado.
- Custos de referência: e-mail ~1 crédito, telefone ~8 créditos. Confira o saldo no topo do Apollo antes de começar.

## 4. Site da empresa

- Página de contato ou rodapé costuma trazer e-mail e telefone comerciais. Fonte: **site (comercial da empresa)**.

## 5. CNPJ (empresas brasileiras)

- Ache o CNPJ no rodapé do site ou numa busca pelo nome da empresa.
- Consulte dados públicos: `https://brasilapi.com.br/api/cnpj/v1/<cnpj>` (telefone e e-mail cadastrais, porte, CNAE). Fonte: **CNPJ**.
- Útil para fundadores de empresas pequenas, em que o contato cadastral costuma ser o do dono.

## Nada funcionou

Registre "Não encontrado" e o que foi tentado na observação. Não invente e não deduza e-mails.
