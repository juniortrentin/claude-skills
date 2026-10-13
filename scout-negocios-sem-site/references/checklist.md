# Checklist de verificação

Registre só o que foi verificado. Na dúvida, deixe o campo vazio.

## Google Maps (perfil da empresa)

| Campo | Como verificar |
|---|---|
| `maps_url` | link do perfil no Maps |
| `nota`, `avaliacoes` | estrelas e número de avaliações no topo do perfil |
| `fotos_maps` | número de fotos (aba Fotos) |
| `horario` | horário de funcionamento preenchido (true/false) |
| `responde_avaliacoes` | o dono respondeu a alguma das 10 avaliações mais recentes? (true/false) |
| `telefone`, `whatsapp` | telefone do perfil; WhatsApp se aparecer como botão ou no texto |
| `site` | endereço do campo "site" do perfil (pode estar vazio) |

## Site

Classifique em `site_status`:

| Valor | Quando |
|---|---|
| `sem_site` | o perfil não tem site e uma busca por nome + cidade não encontra página própria |
| `so_rede_social` | o "site" é um link de Instagram, Facebook, página de links ou só WhatsApp |
| `erro` | o endereço não abre, mostra erro, domínio expirado ou página de hospedagem |
| `construtor_basico` | página gratuita de construtor com subdomínio (ex.: `nome.wixsite.com`, `sites.google.com/...`) e pouco conteúdo |
| `ok` | site próprio que abre normalmente |

Para `ok`, verifique também:

- `https`: o endereço abre com https, sem aviso de não seguro.
- `mobile`: a página tem `<meta name="viewport">` e o texto não fica minúsculo no celular (abra no navegador em largura de celular, se possível).
- `ano_rodape`: o ano mais recente que aparece no rodapé ou em posts e notícias do site (número, ex.: 2019).
- `whatsapp_no_site`: há botão ou link de WhatsApp (`wa.me` ou `api.whatsapp.com`).

Use a leitura de páginas da web (WebFetch). Se vier vazia (site feito só em JavaScript), abra no navegador.

## Instagram

- `instagram`: @ do perfil do negócio (link no Maps, no site ou busca "nome + cidade instagram").
- `insta_ultimo_post`: data do post mais recente (AAAA-MM-DD). Abra só o perfil; não curta nem siga.

## Ritmo e bloqueios

Um negócio por vez, no máximo 80 por rodada. Se o Google ou o Instagram pedirem verificação, pare a navegação naquele site e siga com o que já tem.
