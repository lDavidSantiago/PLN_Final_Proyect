from grammar import build_cfg
from lexer import Lexer
from parser import ParseError, Parser


def run_case(lexer, parser, text):
    print("=" * 70)
    print(f"Entrada: {text}")

    tokens = lexer.tokenizar(text)
    print("Tokens:")
    for token in tokens:
        print(f"  {token.tipo:<10} -> {token.valor}")

    try:
        tree = parser.parse(tokens)
    except ParseError as error:
        error.show_error()
        return

    print("\nProducciones usadas:")
    tree.display_productions_used()
    tree.display()


def main():
    cfg = build_cfg()
    lexer = Lexer()
    parser = Parser(cfg)

    print("No terminales (V):", sorted(cfg.V))
    print("Terminales (T):", sorted(cfg.T))
    print("Simbolo inicial (S):", cfg.S)

    cases = [
        "crea una carpeta llamada proyectos",
        "mueve los archivos pdf a respaldo",
        "crea una carpeta llamada datos y mueve los archivos csv a respaldo",
    ]

    for case in cases:
        run_case(lexer, parser, case)


if __name__ == "__main__":
    main()
