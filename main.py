from lexical.scanner import Scanner
from syntatic.parser import Parser

def main():
    sc = Scanner("programa_checkpoint2.mc")

    print("\nTOKENS - SCANNER\n")
    tmp = Scanner("programa_checkpoint2.mc")
    while True:
        tk = tmp.next_token()
        if not tk:
            break
        print(tk)

    print("\nANÁLISE SINTÁTICA\n")
    parser = Parser(sc, debug=True)
    try:
        parser.parse_program()
        print("\nAnálise sintática concluída.")
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()

"""
Grupo:
Lucas Alcântara Pinho da Nóbrega
Tiago Monteiro Simões Cavalcante 
Victor Medeiros Cavalcante
"""