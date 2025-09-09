from lexical.scanner import Scanner

def main():
    sc = Scanner("programa.mc")
    while True:
        tk = sc.next_token()
        if tk is None:
            break
        print(tk)

if __name__ == "__main__":
    main()


"""
Grupo:
Lucas Alcântara Pinho da Nóbrega
Tiago Monteiro Simões Cavalcante 
Victor Medeiros Cavalcante
"""