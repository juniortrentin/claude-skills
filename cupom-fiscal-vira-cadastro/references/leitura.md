# Como ler cada tipo de nota

Ordem de confiança: **XML > QR code (página da SEFAZ) > foto**. Use sempre a fonte mais confiável disponível para cada nota.

## 1. XML (NF-e ou NFC-e)

- Fornecedores costumam mandar o XML por e-mail junto com o boleto. Peça quando a nota for grande.
- Rode `python scripts/ler_xml_nfe.py arquivos/*.xml --saida trabalho/notas`.
- O XML traz código do fornecedor, EAN, NCM, unidade, quantidades e descontos exatos. Não precisa conferir a leitura, só o casamento com o cadastro.

## 2. Cupom com QR code (NFC-e)

1. Rode `python scripts/ler_qrcode.py fotos/*.jpg --json trabalho/qrcodes.json`. O script devolve o link da consulta e a chave de acesso.
2. Abra o link da consulta pública:
   - tente primeiro a leitura de páginas da web (WebFetch);
   - se vier vazia ou bloqueada, abra no navegador (Claude in Chrome ou o navegador do app) e leia o texto da página;
   - se a SEFAZ pedir CAPTCHA, **não tente resolver**: leia os itens pela foto (seção 3) e anote a chave.
3. A página lista itens com código, descrição, quantidade, unidade e valor. Transcreva para o formato de `formato.md` com `origem: "qrcode"`.
4. Se o QR não for lido pelo script (foto torta, amassada, reflexo), procure a chave de 44 dígitos impressa abaixo do QR e valide com `ler_qrcode.py --chave "..."`. A consulta também funciona pela chave no portal da SEFAZ do estado.

## 3. Nota ou cupom sem QR code (foto)

Vale para cupom antigo, DANFE de NF-e, nota de talão, pedido de atacado ou recibo.

1. **Junte as fotos da mesma nota.** Cupons longos vêm em várias fotos. Sinais de continuação: a foto seguinte começa onde a anterior parou, o rodapé com o total só aparece na última, o mesmo número de nota ou o mesmo cabeçalho de loja.
2. **Descarte fotos repetidas** (mesma nota fotografada duas vezes). O `lancar.py conferir` também acusa notas repetidas pelo número, data e total.
3. **Transcreva linha a linha**: código (se houver), descrição como impressa, quantidade, valor unitário e total da linha. Não arredonde.
4. **Confira na hora**: qtd × unitário = total da linha. Se não bater, olhe de novo a foto: o erro costuma ser leitura de vírgula, de 1 e 7 ou de 0 e 8.
5. Leia o rodapé: subtotal, desconto, acréscimo/frete e total. Desconto da nota inteira vai em `desconto`, não nos itens.
6. Trechos ilegíveis: não invente. Marque o item com a descrição `"[ilegível] ..."` e pergunte à pessoa.

## 4. Compra sem nota

Foto do produto com legenda (nome, qtd, valor, fornecedor, data) ou só a mensagem da pessoa. Grave com `origem: "sem_nota"`, `numero` vazio e o total informado. Quando não estiver claro se o valor é por unidade ou por pacote, pergunte.

## Kits e embalagens fechadas

Descrições como "CX 12UN", "KIT C/6", "PCT 10", "DZ" indicam que vários itens vêm juntos. Pergunte uma vez por produto: "Você vende o kit fechado ou por unidade?". Se for por unidade, coloque `fator` com o número de unidades. O script multiplica a quantidade e divide o custo.

## Compra ou despesa

Mercadoria para revender é compra. Embalagem, sacola, material de limpeza, de escritório e o que é usado no próprio negócio é despesa (`"tipo": "despesa"`). Numa nota mista, separe por item. Na dúvida, pergunte.
