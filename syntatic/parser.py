from lexical.scanner import Scanner
from util.token_type import TokenType
from lexical.token import Token

class Parser:
    def __init__(self, scanner, debug=False):
        self.scanner = scanner
        self.lookahead = None
        self.debug = debug
        self._advance()

    def log(self, msg):
        if self.debug:
            print(msg)

    def _advance(self):
        self.lookahead = self.scanner.next_token()

        if self.lookahead is None:
            self.lookahead = Token(TokenType.EOF, "EOF", -1, -1)

    def _match(self, expected_type: TokenType, expected_text: str = None):
        if self.lookahead is None:
            self.error(f"Token esperado {expected_type}, mas encontrou EOF")

        if self.lookahead.type == expected_type:
            if expected_text is None or self.lookahead.text == expected_text or (isinstance(expected_text, list) and self.lookahead.text in expected_text):
                tok = self.lookahead
                self._advance()
                return tok

        self.error(f"Token inesperado: {self.lookahead}. Esperado: {expected_type}{' com texto ' + expected_text if expected_text else ''}")

    def error(self, msg):
        raise Exception(f"Erro sintático: {msg} (token atual: {self.lookahead})")

    # ':' 'DECLARACOES' listaDeclaracoes ':' 'ALGORITMO' listaComandos
    def parse_program(self):
        self.log("Iniciando análise de programa")
        self._match(TokenType.COLON)
        self._match(TokenType.DECLARACOES)
        self.listaDeclaracoes()
        self._match(TokenType.COLON)
        self._match(TokenType.ALGORITMO)
        self.listaComandos()

        if self.lookahead.type != TokenType.EOF:
            self.error("Conteúdo extra após o fim do programa")
    
        self.log("Programa reconhecido com sucesso.")

    # listaDeclaracoes : declaracao listaDeclaracoes | declaracao;
    def listaDeclaracoes(self):
        self.declaracao()

        while self.lookahead.type == TokenType.IDENTIFIER:
            self.declaracao()

    # declaracao : VARIAVEL ':' tipoVar;
    def declaracao(self):
        self.log("Reconhecendo declaracao")

        ident = self._match(TokenType.IDENTIFIER)
        self._match(TokenType.COLON)

        tipo = self.lookahead.text
        self.tipoVar()

        self.log(f"Variável declarada: {ident.text} : {tipo}")

    def tipoVar(self):
        if self.lookahead.type == TokenType.INTEIRO:
            self._match(TokenType.INTEIRO)
        elif self.lookahead.type == TokenType.REAL:
            self._match(TokenType.REAL)
        else:
            self.error("Tipo esperado INTEIRO ou REAL")

    # listaComandos : comando listaComandos | comando;
    def listaComandos(self):
        self.comando()

        while self.lookahead.type in (TokenType.IDENTIFIER, TokenType.LER, TokenType.IMPRIMIR, TokenType.SE, TokenType.ENQUANTO, TokenType.INICIO):
            self.comando()

    # comando : comandoAtribuicao | comandoEntrada | comandoSaida | comandoCondicao | comandoRepeticao | subAlgoritmo;
    def comando(self):
        if self.lookahead.type == TokenType.IDENTIFIER:
            self.comandoAtribuicao()
        elif self.lookahead.type == TokenType.LER:
            self.comandoEntrada()
        elif self.lookahead.type == TokenType.IMPRIMIR:
            self.comandoSaida()
        elif self.lookahead.type == TokenType.SE:
            self.comandoCondicao()
        elif self.lookahead.type == TokenType.ENQUANTO:
            self.comandoRepeticao()
        elif self.lookahead.type == TokenType.INICIO:
            self.subAlgoritmo()
        else:
            self.error("Início de comando inesperado")

    # comandoAtribuicao : IDENTIFIER = expressaoAritmetica;
    def comandoAtribuicao(self):
        self._match(TokenType.IDENTIFIER)
        self._match(TokenType.ASSIGNMENT)
        self.expressaoAritmetica()

    # comandoEntrada : LER IDENTIFIER
    def comandoEntrada(self):
        self._match(TokenType.LER)
        self._match(TokenType.IDENTIFIER)

    # comandoSaida : IMPRIMIR LPAREN (IDENTIFIER | STRING) RPAREN
    def comandoSaida(self):
        self._match(TokenType.IMPRIMIR)
        self._match(TokenType.LPAREN)

        if self.lookahead.type == TokenType.IDENTIFIER:
            self._match(TokenType.IDENTIFIER)
        elif self.lookahead.type == TokenType.STRING:
            self._match(TokenType.STRING)
        else:
            self.error("IMPRIMIR espera IDENTIFIER ou STRING")

        self._match(TokenType.RPAREN)

    # 'SE' expressaoRelacional 'ENTAO' comando | 'SE' expressaoRelacional 'ENTAO' comando 'SENAO' comando;
    def comandoCondicao(self):
        self._match(TokenType.SE)
        self.expressaoRelacional()
        self._match(TokenType.ENTAO)
        self.comando()

        if self.lookahead.type == TokenType.SENAO:
            self._match(TokenType.SENAO)
            self.comando()

    # comandoRepeticao : 'ENQUANTO' expressaoRelacional comando;
    def comandoRepeticao(self):
        self._match(TokenType.ENQUANTO)
        self.expressaoRelacional()
        self.comando()

    # subAlgoritmo : 'INICIO' listaComandos 'FIM';
    def subAlgoritmo(self):
        self._match(TokenType.INICIO)

        if self.lookahead.type in (TokenType.IDENTIFIER, TokenType.LER, TokenType.IMPRIMIR, TokenType.SE, TokenType.ENQUANTO, TokenType.INICIO):
            self.listaComandos()
        
        self._match(TokenType.FIM)

    # expressaoAritmetica -> termoAritmetico ((+|-) termoAritmetico)
    def expressaoAritmetica(self):
        self.termoAritmetico()

        while self.lookahead.type == TokenType.MATH_OPERATOR and self.lookahead.text in ['+', '-']:
            self._match(TokenType.MATH_OPERATOR)
            self.termoAritmetico()

    # termoAritmetico -> fatorAritmetico ((*|/) fatorAritmetico)
    def termoAritmetico(self):
        self.fatorAritmetico()

        while self.lookahead.type == TokenType.MATH_OPERATOR and self.lookahead.text in ['*', '/']:
            self._match(TokenType.MATH_OPERATOR)
            self.fatorAritmetico()

    # fatorAritmetico -> NUMBER | IDENTIFIER | LPAREN expressaoAritmetica RPAREN
    def fatorAritmetico(self):
        if self.lookahead.type == TokenType.NUMBER:
            self._match(TokenType.NUMBER)
        elif self.lookahead.type == TokenType.IDENTIFIER:
            self._match(TokenType.IDENTIFIER)
        elif self.lookahead.type == TokenType.LPAREN:
            self._match(TokenType.LPAREN)
            self.expressaoAritmetica()
            self._match(TokenType.RPAREN)
        else:
            self.error("Fator aritmético esperado (NUMBER | IDENTIFIER | '(' expressão ')')")

    # expressaoRelacional -> termoRelacional ((E|OU) termoRelacional)
    def expressaoRelacional(self):
        self.termoRelacional()

        while self.lookahead.type in (TokenType.E, TokenType.OU):
            if self.lookahead.type == TokenType.E:
                self._match(TokenType.E)
            else:
                self._match(TokenType.OU)
                
            self.termoRelacional()

    # termoRelacional -> expressaoAritmetica REL_OP expressaoAritmetica | LPAREN expressaoRelacional RPAREN
    def termoRelacional(self):
        if self.lookahead.type == TokenType.LPAREN:
            self._match(TokenType.LPAREN)
            self.expressaoRelacional()
            self._match(TokenType.RPAREN)
        else:
            self.expressaoAritmetica()
            if self.lookahead.type == TokenType.REL_OPERATOR:
                self._match(TokenType.REL_OPERATOR)
                self.expressaoAritmetica()
            else:
                self.error("Operador relacional esperado em termoRelacional")