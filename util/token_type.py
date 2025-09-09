from enum import Enum

class TokenType(Enum):
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    REL_OPERATOR = "REL_OPERATOR"
    MATH_OPERATOR = "MATH_OPERATOR"
    ASSIGNMENT = "ASSIGNMENT"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"

    # Palavras Reservadas
    INT = "INT"
    FLOAT = "FLOAT"
    PRINT = "PRINT"
    IF = "IF"
    ELSE = "ELSE"