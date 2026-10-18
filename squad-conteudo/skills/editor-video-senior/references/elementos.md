# Biblioteca de elementos

Cada elemento entra no instante em que a palavra é dita e sai com fade curto. Campos comuns: `tipo`, `de`, `ate`, `x`, `y`, `ancora` (`c`, `tl`, `tr`, `bl`, `br`), `entrada` (`dx`, `dy`, `escala`, `duracao`) e `som` (pop na entrada, ligado por padrão).

| tipo | Para quê | Campos próprios | Entrada padrão |
|---|---|---|---|
| `texto_atras` | Palavra gigante atrás da pessoa: o gancho, a data, o tema, o "bora" | `texto`, `tamanho` (300 a 760), `cor` | sobe 140 px e assenta de 108% |
| `rotulo` | Assinatura discreta no topo ("NOME DA MARCA") | `texto`, `tamanho`, `cor`, `espacamento` | sobe 50 px |
| `pilula` | Tema, data, oferta, selos ("ONLINE", "GRÁTIS") | `texto`, `fonte` (`titulo`/`texto`), `tamanho`, `cor_texto`, `cor_fundo`, `padx`, `pady`, `raio` | sobe 50 px |
| `nome` | Lower third com nome de convidado ou especialista | `rotulo` ("COM"), `texto`, `tamanho`, `y` | barra cresce da esquerda |
| `icone` | Reforço visual de um objeto citado | `icone` (`planilha`, `calendario`, `check`), `texto` | sobe 50 px |
| `grafico` | "Resultados", "crescimento", "retorno": barras que sobem e uma seta | `texto` (título do cartão) | sobe 50 px |
| `imagem` | PNG enviado pela pessoa (produto, print, selo) | `arquivo`, `largura` | sobe 50 px |

Fora da lista `elementos`, o config também aceita **inserções** (`insercoes`): B-roll em tela cheia com fusão curta. Use para 1,5 a 3 s no meio de uma frase explicativa, nunca no gancho nem na chamada para ação. Ver `config.md` e `ia-generativa.md`.

## Boas práticas (de editor)

- **Gancho nos 2 primeiros segundos:** um `texto_atras` com a palavra mais forte da primeira frase e uma `pilula` com o tema.
- **Um elemento por ideia.** Se a frase tem data e nome, a data vai numa cena e o nome na seguinte.
- **No máximo 3 ou 4 `texto_atras` por vídeo de 30 s,** alternando cores (primária e fundo), para não cansar.
- **Posições seguras em 9:16:** topo útil a partir de y ≈ 120. Legendas em y ≈ 1390. Evite x > 940 (botões do app) e y > 1600 (descrição do post).
- **`texto_atras` fica na altura da cabeça e dos ombros** (y entre 450 e 720), para a pessoa "recortar" a palavra. Confira na prévia se o rosto ficou livre.
- **Pílulas em dupla** (ex.: ONLINE + GRATUITO) entram de lados opostos, com 0,1 a 0,2 s de diferença.
- **Elemento dura enquanto a ideia dura:** do instante da palavra até o fim do trecho, ou um pouco mais se o próximo trecho continua o assunto.
- **Tela final:** gancho em 2 linhas (uma na cor primária, outra na tinta), a informação-chave numa pílula, o convidado em texto, o botão com seta, o link e o logo embaixo.

## Elemento novo

Se um vídeo pedir algo que não está aqui (contador, mapa, depoimento), crie no `scripts/editar_video.py`. Acrescente um tipo em `make_sprite` (desenho) e, se for animado, em `element_draw`. Documente nesta tabela. Elementos novos que forem aprovados entram na próxima versão da skill pelo Passo 8.
