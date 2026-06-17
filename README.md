# SGL - Sistema de Gestao Local

Sistema em Python para console que gerencia produtos, estoque e movimentacoes
(entradas e saidas). Trabalho final da disciplina de Logica e Desenvolvimento de
Algoritmos.

## Estrutura do projeto

- `main.py` - codigo-fonte principal do sistema
- `produtos.json` - dados dos produtos cadastrados
- `movs.json` - historico de entradas e saidas de estoque
- `relatorio.txt` - relatorio exportado (gerado pela opcao 10)
- `README.md` - instrucoes de uso e casos de teste

## Como executar

1. Abra o terminal na pasta do projeto (a que contem `main.py`).
2. Execute:

```powershell
python main.py
```

3. Use o menu para cadastrar produtos, listar, buscar, registrar
   entradas/saidas, gerar relatorios, editar, exportar ou salvar e sair.

Requer apenas Python 3 (sem bibliotecas externas).

## Menu principal

```text
1 - Cadastrar produto
2 - Listar produtos (com filtro opcional por categoria)
3 - Buscar produto por nome ou ID
4 - Registrar entrada de estoque
5 - Registrar saida de estoque
6 - Relatorio de movimentacoes
7 - Relatorio gerencial
8 - Salvar e sair
9 - Editar produto (preco/categoria)
10 - Exportar relatorio em TXT
```

## Recursos implementados

- Cadastro de produtos com ID automatico (`maior ID + 1`, lista vazia comeca em 1)
- Validacao de preco (>= 0), estoque inicial (>= 0), quantidade (> 0) e opcao do menu
- Listagem de produtos ordenada por nome (`sorted`) com filtro opcional por categoria
- Busca parcial por nome (sem diferenciar maiusculas) ou por ID exato
- Registro de entrada e saida de estoque, gerando movimentacao e atualizando o estoque
- Bloqueio de saida maior que o estoque disponivel (re-pede a quantidade)
- Relatorio de movimentacoes com ID, data, tipo, ID do produto, nome, quantidade,
  observacao e totais de entrada e saida
- Relatorio gerencial: maior e menor estoque (tratando empates), valor total do
  estoque (Sigma estoque * preco), quantidade de produtos por categoria e Top 3 por
  valor em estoque
- Edicao de produto (preco e/ou categoria)
- Exportacao dos relatorios para `relatorio.txt`
- Persistencia em JSON (`produtos.json` e `movs.json`, `indent=2`)
- Tratamento de erros com `try/except`: o programa nao quebra com entrada invalida

## Dados iniciais

O projeto ja inclui 5 produtos em `produtos.json` e 8 movimentacoes em `movs.json`.
Se algum arquivo JSON nao existir, o sistema inicia a respectiva lista vazia. Ao
escolher a opcao `8` (ou ao encerrar com Ctrl+Z/Ctrl+C), todos os dados sao salvos
automaticamente.

## Casos de teste (entrada -> saida esperada)

### 1. Cadastrar produto valido

Entrada:

```text
1
Cafe
Alimento
16.90
10
```

Saida esperada: `Produto cadastrado com sucesso.` e o produto passa a aparecer na
listagem com um novo ID (6, considerando os dados iniciais).

### 2. Preco negativo durante o cadastro

Entrada (no campo Preco): `-5`

Saida esperada: `Erro: o valor deve ser maior ou igual a 0.` e o campo Preco e
solicitado novamente, sem quebrar o programa.

### 3. Buscar produto por nome parcial

Entrada:

```text
3
ar
```

Saida esperada: lista os produtos compativeis, como `Arroz` e `Aromatizador`
(busca case-insensitive).

### 4. Registrar saida maior que o estoque

Entrada (opcao 5, produto Arroz com estoque 20):

```text
5
1
999
```

Saida esperada: `Erro: nao e possivel retirar mais do que o estoque disponivel.`
seguido de `Estoque atual: 20` e nova solicitacao da quantidade. A movimentacao so
e registrada quando a quantidade for valida.

### 5. Relatorio gerencial

Entrada: `7`

Saida esperada: maior estoque (`Detergente`, 25), menor estoque (`Aromatizador`,
10), `Valor total do estoque: R$ 838.30`, quantidade por categoria
(Alimento: 2, Limpeza: 2, Outros: 1) e Top 3 por valor em estoque
(Arroz R$ 250.00, Sabao em po R$ 226.80, Aromatizador R$ 142.00).
