# Cupom fiscal vira cadastro

Uma skill para o Claude que dá entrada nas suas compras: você manda as fotos dos cupons e notas, de um ou vários fornecedores, e ele cadastra os produtos, soma as reposições, calcula o custo médio e sugere o preço de venda na sua planilha.

## O que ela lê

- Cupom fiscal com **QR code** (NFC-e): consulta a nota na SEFAZ.
- Nota ou cupom **sem QR code**: lê pela foto, linha por linha, e confere as contas.
- **XML** de NF-e ou NFC-e, o arquivo que o fornecedor manda por e-mail.
- Compra **sem nota**: foto ou mensagem com nome, quantidade e valor.

Pode mandar tudo junto: várias fotos, vários fornecedores, misturados.

## Onde ela grava

- Numa planilha do **Google Sheets** que você já usa (é só mandar o link).
- Num **Excel** que você já tem (ela devolve uma cópia atualizada).
- Numa **planilha nova**, com abas Produtos, Compras, Fornecedores, Despesas, Conferência e Config.

## O que vem no pacote

```
cupom-fiscal-vira-cadastro/
├── SKILL.md                  instruções que o Claude segue
├── README.md                 este arquivo
├── LICENSE.md                uso livre, mantendo o crédito
├── references/
│   ├── leitura.md            como ler cada tipo de nota, kits, compra × despesa
│   ├── formato.md            formato dos dados e da configuração
│   └── planilhas.md          planilha nova, Excel, Google Sheets e mapa de colunas
└── scripts/
    ├── ler_xml_nfe.py        lê XML de NF-e e NFC-e
    ├── ler_qrcode.py         lê o QR code das fotos e valida a chave de acesso
    └── lancar.py             confere, casa com o cadastro e grava a planilha
```

## Como instalar

1. Baixe o arquivo `cupom-fiscal-vira-cadastro.zip`.
2. No Claude, abra a área de Skills nas configurações e envie o .zip.
3. Para gravar no Google Sheets, conecte o Google Drive no Claude ou use o Claude com acesso a navegador.

## Como usar

> Lança essas notas na minha planilha de estoque: [fotos] [link da planilha]

O Claude pergunta onde gravar e qual markup você usa, confere cada nota, mostra a prévia e só grava depois do seu ok.

## Créditos

Skill gratuita da **Trentin Solutions**, criada por Ivaldo Trentin · trentinsolutions.com.br

Licença CC BY 4.0: use, adapte e compartilhe à vontade, mantendo o crédito.

## Apoie

A skill é gratuita e vai continuar assim. Se ela te ajudou, um Pix de qualquer valor ajuda a publicar as próximas.

- **Chave Pix aleatória:** `b73301d4-682f-46a0-857a-3a7653c2befb`
- **Recebedor:** Ivaldo Idalgo Trentin Junior Ltda
- **QR code:** trentinsolutions.com.br/skills/cupom-fiscal-vira-cadastro#apoie
