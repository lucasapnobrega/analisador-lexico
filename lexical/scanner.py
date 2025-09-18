from util.token_type import TokenType
from lexical.token import Token

# Scanner responsável por analisar caractere por caractere do código-fonte (programa.mc) e retornar os tokens reconhecidos.
class Scanner:
    def __init__(self, filename: str):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            self.source_code = list(content)
            self.pos = 0
            self.line = 1 
            self.col = 1
        except Exception as e:
            print("Erro ao abrir arquivo:", e)
            self.source_code = []
            self.pos = 0

        # Tabela de palavras reservadas
        self.reserved_words = {
            "int": TokenType.INT,
            "float": TokenType.FLOAT,
            "print": TokenType.PRINT,
            "if": TokenType.IF,
            "else": TokenType.ELSE,
        }

    def next_token(self):
        content = ""
        state = 0

        while True:
            if self.is_eof():
                return None

            current_char = self.next_char()

            # Ignora espaços, tab e quebra de linha
            if current_char in [' ', '\t', '\r']:
                continue
            if current_char == '\n':
                self.line += 1
                self.col = 1
                continue

            # Comentário de linha única: #
            if current_char == "#":
                while not self.is_eof() and self.peek_char() != '\n':
                    self.next_char()
                continue

            # Comentário de múltiplas linhas: /* ... */
            if current_char == "/" and self.peek_char() == "*":
                self.next_char()
                while not self.is_eof():
                    c = self.next_char()

                    if c == "\n":
                        self.line += 1
                        self.col = 1

                    if c == "*" and self.peek_char() == "/":
                        self.next_char()
                        break
                continue

            # Identificadores E Palavras Reservadas
            if self.is_letter(current_char) or current_char == "_":
                content = current_char
                while self.is_letter(self.peek_char()) or self.is_digit(self.peek_char()) or self.peek_char() == "_":
                    content += self.next_char()

                # Se for palavra reservada, retorna o tipo
                if content in self.reserved_words:
                    return Token(self.reserved_words[content], content, self.line, self.col)
                return Token(TokenType.IDENTIFIER, content, self.line, self.col)

            # Números com ou sem ponto decimal
            # Expressão regular: ((0-9)*.)?(0-9)+
            if self.is_digit(current_char) or (current_char == "." and self.is_digit(self.peek_char())):
                content = current_char
                has_dot = current_char == "."
                
                # Se começou com dígito, pode ter mais dígitos
                if self.is_digit(current_char):
                    while self.is_digit(self.peek_char()):
                        content += self.next_char()
                    
                    # Pode ter um ponto seguido de dígitos
                    if self.peek_char() == "." and self.is_digit_at_position(self.pos + 1):
                        content += self.next_char()  # adiciona o ponto
                        while self.is_digit(self.peek_char()):
                            content += self.next_char()
                
                # Se começou com ponto, deve ter pelo menos um dígito após
                else:  # começou com "."
                    while self.is_digit(self.peek_char()):
                        content += self.next_char()
                
                return Token(TokenType.NUMBER, content, self.line, self.col)

            # Operadores Matemáticos
            if current_char in ['+', '-', '*', '/']:
                return Token(TokenType.MATH_OPERATOR, current_char, self.line, self.col)

            # Operadores de Atribuição
            if current_char == "=":
                if self.peek_char() == "=":
                    self.next_char()
                    return Token(TokenType.REL_OPERATOR, "==", self.line, self.col)
                return Token(TokenType.ASSIGNMENT, "=", self.line, self.col)

            # Operadores Relacionais
            if current_char == ">":
                if self.peek_char() == "=":
                    self.next_char()
                    return Token(TokenType.REL_OPERATOR, ">=", self.line, self.col)
                return Token(TokenType.REL_OPERATOR, ">", self.line, self.col)

            if current_char == "<":
                if self.peek_char() == "=":
                    self.next_char()
                    return Token(TokenType.REL_OPERATOR, "<=", self.line, self.col)
                return Token(TokenType.REL_OPERATOR, "<", self.line, self.col)

            if current_char == "!":
                if self.peek_char() == "=":
                    self.next_char()
                    return Token(TokenType.REL_OPERATOR, "!=", self.line, self.col)
                else:
                    self.error("Operador '!' inválido, esperava '!='")

            # Parênteses
            if current_char == "(":
                return Token(TokenType.LPAREN, "(", self.line, self.col)
            if current_char == ")":
                return Token(TokenType.RPAREN, ")", self.line, self.col)

            # Ponto e vírgula
            if current_char == ";":
                return Token(TokenType.SEMICOLON, ";", self.line, self.col)

            # Chaves
            if current_char == "{":
                return Token(TokenType.LBRACE, "{", self.line, self.col)
            if current_char == "}":
                return Token(TokenType.RBRACE, "}", self.line, self.col)

            # Operadores lógicos
            if current_char == "&":
                if self.peek_char() == "&":
                    self.next_char()
                    return Token(TokenType.LOG_OPERATOR, "&&", self.line, self.col)
                else:
                    self.error("Operador '&' inválido, esperava '&&'")

            # Erro Léxico
            error_line = self.line
            error_col = self.col - 1  # Ajusta para mostrar a posição correta
            self.error(f"Caractere inválido: '{current_char}'")

    # Funções Auxiliares
    def is_letter(self, c: str) -> bool:
        return c.isalpha()

    def is_digit(self, c: str) -> bool:
        return c.isdigit()

    def next_char(self) -> str:
        ch = self.source_code[self.pos]
        self.pos += 1
        self.col += 1
        return ch

    def peek_char(self) -> str:
        if self.is_eof():
            return "\0"
        return self.source_code[self.pos]

    def is_eof(self) -> bool:
        return self.pos >= len(self.source_code)

    def is_digit_at_position(self, pos: int) -> bool:
        if pos >= len(self.source_code):
            return False
        return self.source_code[pos].isdigit()

    def error(self, message: str):
        raise Exception(f"Erro léxico (linha {self.line}, coluna {self.col}): {message}")
