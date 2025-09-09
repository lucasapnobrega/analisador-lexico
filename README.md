# Analisador Léxico em Python

Este projeto implementa um **analisador léxico** em Python, responsável por **ler um código-fonte** (no arquivo `programa.mc`), **analisar caractere por caractere** e **retornar os tokens reconhecidos**, como identificadores, números, operadores, palavras reservadas e símbolos especiais.

## 👥 Equipe
- Lucas Alcântara Pinho da Nóbrega - RGM: 29319161
- Tiago Monteiro Simões Cavalcante - RGM: 31638228
- Victor Medeiros Cavalcante - RGM: 30004772

## 📂 Estrutura do Projeto

```
COMPILADOR-PROJETO/
│── lexical/
│ ├── scanner.py # Implementação do analisador léxico (scanner)
│ ├── token.py # Estrutura de dados do Token
│
│── util/
│ ├── token_type.py # Enum com os tipos de tokens
│
│── programa.mc # Programa de entrada a ser analisado
│── main.py # Arquivo principal (executa o analisador)
```

## Exemplo de Entrada (programa.mc)
```
float y = 3.14
/* comentário
de várias 
linhas */
z != 20
# comentário de uma linha
123.456
1.
int x = 10;
if (x >= y) {
    print(x)
}
```

## Saída Esperada (tokens)
```
Token(type=TokenType.FLOAT, text='float', line=1, col=6)
Token(type=TokenType.IDENTIFIER, text='y', line=1, col=8)
Token(type=TokenType.ASSIGNMENT, text='=', line=1, col=10)
Token(type=TokenType.NUMBER, text='3.14', line=1, col=15)
Token(type=TokenType.IDENTIFIER, text='z', line=5, col=2)
Token(type=TokenType.REL_OPERATOR, text='!=', line=5, col=5)
Token(type=TokenType.NUMBER, text='20', line=5, col=8)
Token(type=TokenType.NUMBER, text='123.456', line=7, col=8)
.
.
.
Exception: Erro léxico (linha 8, coluna 3): Número inválido: 1.
```

## Funcionalidades Implementadas

1) Reconhecimento de Identificadores: (a-z | A-Z | _)(a-z | A-Z | _ | 0-9)*

2) Operadores Matemáticos: soma (+), subtração (-), multiplicação (*) e divisão (/)

3) Operador de Atribuição: =

4) Operadores Relacionais: >, >=, <, <=, !==, ==

5) Parênteses

6) Números (decimal ou não): 123, 123.456, .456

7) Palavras Reservadas: int, float, print, if, else

8) Comentários de linha única (#) ou de múltiplas linhas (/* ... */)

9) Tratamento de Erros Léxicos: Mensagem com linha e coluna do erro (exemplo: Erro léxico (linha 4, coluna 8): Caractere inválido: '@')

