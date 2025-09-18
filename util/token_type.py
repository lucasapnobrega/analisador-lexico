from enum import Enum

class TokenType(Enum):
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    REL_OPERATOR = "REL_OPERATOR"
    MATH_OPERATOR = "MATH_OPERATOR"
    ASSIGNMENT = "ASSIGNMENT"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    SEMICOLON = "SEMICOLON"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LOG_OPERATOR = "LOG_OPERATOR"

    # Palavras Reservadas
    INT = "INT"
    FLOAT = "FLOAT"
    PRINT = "PRINT"
    IF = "IF"
    ELSE = "ELSE"