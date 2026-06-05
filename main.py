from grammar import build_cfg
from lexer import Lexer
from parser import ParseError, Parser
from semantic import SemanticError, Semantics
from simulator import Simulator


def run_case(lexer, parser, simulator, text):
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

    semantics = Semantics()

    print("\nProducciones usadas:")
    tree.display_productions_used()
    tree.display()

    try:
        meaning = semantics.extract(tree)
    except SemanticError as error:
        print(f"Semantic error: {error}")
        return

    semantics.display(meaning)
    simulator.show(meaning)
CASOS_DEMO = [
    "crea una carpeta llamada proyectos",
    "mueve los archivos pdf a proyectos",
    "elimina la carpeta vieja",
    "copia el archivo txt a respaldo",
    "renombra la carpeta vieja llamada nueva",
    "lista los archivos",
    "lista las carpetas",
    "crea una carpeta llamada datos y mueve los archivos csv ahi",
]

def main():
    cfg = build_cfg()
    lexer = Lexer()
    parser = Parser(cfg)
    simulator = Simulator()

    print("No terminales (V):", sorted(cfg.V))
    print("Terminales (T):", sorted(cfg.T))
    print("Simbolo inicial (S):", cfg.S)

    cases = [
        "crea una carpeta llamada proyectos",
        "mueve los archivos pdf a respaldo",
        "crea una carpeta llamada datos y mueve los archivos csv a respaldo",
    ]

    for case in cases:
        run_case(lexer, parser, simulator, case)


if __name__ == "__main__":
    main()
