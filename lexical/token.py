from util.token_type import TokenType

# Estrutura do token, armazenando tipo, texto e posição no código
class Token:
    def __init__(self, type_: TokenType, text: str, line: int, col: int):
        self.type = type_
        self.text = text
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token(type={self.type}, text='{self.text}', line={self.line}, col={self.col})"