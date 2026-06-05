from grammar import build_cfg
from ambiguity import AmbiguityResolver
from lexer import Lexer
from parser import ParseError, Parser
from semantic import SemanticError, Semantics
from simulator import Simulator


BOX_WIDTH = 70


def print_box(title, lines=None):
    lines = lines or []
    border = "+" + "-" * (BOX_WIDTH - 2) + "+"

    print(border)
    print(f"| {title:^{BOX_WIDTH - 4}} |")
    if lines:
        print("|" + "-" * (BOX_WIDTH - 2) + "|")
        for line in lines:
            print(f"| {line:<{BOX_WIDTH - 4}} |")
    print(border)


def show_welcome():
    print_box(
        "Analizador PLN",
        [
            "Ingresa comandos en lenguaje natural para analizarlos.",
            "Ejemplo: crea una carpeta llamada proyectos",
        ],
    )


def show_menu():
    print()
    print("[1] Ingresar frase")
    print("[2] Ejecutar casos demo")
    print("[3] Ver informacion de la gramatica")
    print("[0] Salir")


def show_grammar_info(cfg):
    print_box("Gramatica")
    print("No terminales (V):", sorted(cfg.V))
    print("Terminales (T):", sorted(cfg.T))
    print("Simbolo inicial (S):", cfg.S)


def run_case(lexer, parser, simulator, ambiguity_resolver, text):
    print("=" * 70)
    print(f"Entrada: {text}")

    tokens = lexer.tokenizar(text)
    print("Tokens:")
    for token in tokens:
        print(f"  {token.tipo:<10} -> {token.valor}")

    semantics = Semantics()
    resolved_meaning = ambiguity_resolver.verify_and_resolve(tokens)
    if resolved_meaning is not None:
        semantics.display(resolved_meaning)
        simulator.show(resolved_meaning)
        return

    try:
        tree = parser.parse(tokens)
    except ParseError as error:
        error.show_error()
        return

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
    ambiguity_resolver = AmbiguityResolver()

    show_welcome()

    while True:
        show_menu()
        option = input("Selecciona una opcion > ").strip().lower()

        if option == "1":
            text = input("Frase > ").strip()
            if not text:
                print("Ingresa una frase para analizar.")
                continue
            run_case(lexer, parser, simulator, ambiguity_resolver, text)
        elif option == "2":
            for case in CASOS_DEMO:
                run_case(lexer, parser, simulator, ambiguity_resolver, case)
        elif option == "3":
            show_grammar_info(cfg)
        elif option in {"0", "salir", "exit", "q"}:
            print("Hasta luego.")
            break
        else:
            print("Opcion no valida. Intenta de nuevo.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nHasta luego.")