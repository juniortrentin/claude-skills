# Formatos e marca

## O que sai em cada formato

| Formato | Arquivo | Para que serve |
|---|---|---|
| Página | `catalogo.html` | Uma página só, leve, com busca, filtro por categoria e carrinho. O cliente escolhe as quantidades e toca em "Enviar pedido no WhatsApp": abre a conversa com a lista e o total prontos. |
| PDF | `catalogo_<loja>.pdf` | A4, 6 produtos por página. Cada produto é clicável e abre o WhatsApp com o nome dele. Bom para mandar a quem pede catálogo. |
| Status / Stories | `status_NN_<produto>.png` | 1080 × 1920, um produto por imagem, com preço grande e o botão "Peça pelo WhatsApp". |
| Carrossel | `post_01_capa.png`, `post_02.png`… | 1080 × 1350 (formato do feed). Capa com o título e 3 fotos; depois 4 produtos por tela. |
| Texto | `catalogo_whatsapp.txt` | Lista por categoria com *negrito* e ~riscado~ do WhatsApp, pronta para colar. |

A página também traz dados estruturados (schema.org) dos produtos, o que ajuda buscadores e IAs a entenderem o catálogo se ele for publicado.

## Marca (`trabalho/marca.json`)

```json
{
  "nome": "Ateliê Lume",
  "titulo": "Catálogo de outubro",
  "cor": "#2F5D50",
  "cor2": "#1E3D34",
  "logo": "logo.png",
  "whatsapp": "14999990000",
  "whatsapp_exibir": "(14) 99999-0000",
  "instagram": "@atelielume",
  "chamada": "Peça pelo WhatsApp",
  "validade": "31/10/2026",
  "mostrar_preco": true
}
```

- `cor`: cor principal (fundo do Status, preços, botões). `cor2` é opcional e faz o degradê do Status.
- `logo`: PNG com fundo transparente fica melhor. Sem logo, o nome da loja entra em texto.
- `whatsapp`: só números, com DDD (o script põe o 55 do Brasil se faltar).
- `mostrar_preco: false` gera tudo sem preço ("consulte").
- `fonte_titulo` e `fonte_texto` (opcionais): caminhos para arquivos .ttf ou .otf da marca.

## Fotos

- Nome do arquivo igual ao código do produto (`VL01.jpg`) ou ao nome (`vela-aromatica-lavanda.jpg`).
- A skill corta no centro: produto centralizado, com respiro, fundo liso e luz natural de janela dão o melhor resultado.
- Fotos de celular servem. Evite fundo bagunçado e reflexo de flash.
- Sem foto, o produto ganha um cartão com as iniciais na cor da marca e entra na lista "fotografar".
