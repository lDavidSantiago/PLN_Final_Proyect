"""
Tokenizador lexico DFA 


Aqui implementaremos la gramatica regular.


donde tenemos

#   VERBO   → crea | mueve | elimina | copia | renombra | lista | …
#   DET     → el | la | los | las | un | una | …
#   TIPO    → carpeta | archivo | directorio | …
#   PREP    → a | de | en | hacia | desde | …
#   CONJ    → y | o | luego | …
#   EXT     → pdf | txt | doc | py | …
#   LLLAMA   → llamada | llamado | nombrada | nombrado | …

"""
from dfa import DFA

#------------------------ Gramatica Regular ------------------------


VERBS = {
    'crea':      'crear',
    'crear':     'crear',
    'mueve':     'mover',
    'mover':     'mover',
    'elimina':   'eliminar',
    'eliminar':  'eliminar',
    'borra':     'eliminar',
    'borrar':    'eliminar',
    'copia':     'copiar',
    'copiar':    'copiar',
    'renombra':  'renombrar',
    'renombrar': 'renombrar',
    'lista':     'listar',
    'listar':    'listar',
    'muestra':   'listar',
    'mostrar':   'listar',
}

DETERMINERS = {
    'el', 'la', 'los', 'las',
    'un', 'una', 'unos', 'unas',
}

OBJECT_TYPES = {
    'carpeta':    'carpeta',
    'carpetas':   'carpeta',
    'directorio': 'carpeta',
    'directorios':'carpeta',
    'archivo':    'archivo',
    'archivos':   'archivo',
    'fichero':    'archivo',
    'ficheros':   'archivo',
}

EXTENSIONS = {
    'pdf', 'txt', 'doc', 'docx',
    'jpg', 'jpeg', 'png', 'mp3',
    'csv', 'py', 'html', 'json',
}

PREPOSITIONS = {
    'a', 'de', 'en', 'hacia', 'desde',
    'con', 'para', 'por', 'al',
}

CONNECTORS = {
    'y', 'o', 'luego', 'despues',
    'después', 'también', 'tambien',
}

NAMING_WORDS = {
    'llamada', 'llamado',
    'nombrada', 'nombrado',
}

def build_lex_dfa():
    
    """
    
    
    """
    
    
    
    
    estados = {
        'q0', 'q_verb', 'q_det', 'q_type',
        'q_prep', 'q_connector', 'q_ext', 'q_named_as',
        'q_naming', 'q_error'
    }

    # Construcción de δ: una transición por cada palabra del vocabulario
    delta = {}
    for p in VERBS:        delta[('q0', p)] = 'q_verb'
    for p in DETERMINERS:  delta[('q0', p)] = 'q_det'
    for p in OBJECT_TYPES: delta[('q0', p)] = 'q_type'
    for p in PREPOSITIONS: delta[('q0', p)] = 'q_prep'
    for p in CONNECTORS:   delta[('q0', p)] = 'q_connector'
    for p in EXTENSIONS:   delta[('q0', p)] = 'q_ext'
    for p in NAMING_WORDS: delta[('q0', p)] = 'q_named_as'

    # F = todos los estados de aceptación (excepto q0 y q_error)
    finales = {
        'q_verb', 'q_det', 'q_type', 'q_prep',
        'q_connector', 'q_ext', 'q_named_as', 'q_naming'
    }

    alfabeto = {simbolo for (_, simbolo) in delta}

    return DFA(
        states        = estados,
        alphabet      = alfabeto,
        transitions   = delta,
        initial_state = 'q0',
        final_states  = finales,
    )
    
    pass
# ─── Token ────────────────────────────────────────────────────────────────────

class Token:
    """
    Unidad léxica producida por el tokenizador.

    Atributos:
        tipo      : categoría gramatical  (VERBO, DET, TIPO, …)
        valor     : forma original de la palabra en la entrada
        valor_norm: forma canónica/normalizada (p.ej. 'crea' → 'crear')
    """

    def __init__(self, tipo, valor, valor_norm=None):
        self.tipo       = tipo
        self.valor      = valor
        self.valor_norm = valor_norm if valor_norm is not None else valor

    def __repr__(self):
        if self.valor != self.valor_norm:
            return f"Token({self.tipo}, '{self.valor}' → '{self.valor_norm}')"
        return f"Token({self.tipo}, '{self.valor}')"

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.tipo == other.tipo and self.valor_norm == other.valor_norm
        return False


# ─── Lexer ────────────────────────────────────────────────────────────────────

class Lexer:
    """
    Tokenizador léxico del sistema de archivos en español.

    Proceso:
      1. Normalización de la cadena de entrada.
      2. Separación en palabras (símbolos del alfabeto Σ).
      3. Para cada palabra: consultar vocabulario → categoría.
      4. Construir el Token correspondiente.
    """
    def __init__(self):
        self.dfa = build_lex_dfa()
    def tokenizar(self, entrada):
        texto    = self._normalizar(entrada)
        palabras = texto.split()
        return [self._clasificar(p) for p in palabras]

    def _normalizar(self, texto):
        texto = texto.lower().strip()
        for signo in ',.!?;:\'"()[]{}':
            texto = texto.replace(signo, ' ')
        while '  ' in texto:
            texto = texto.replace('  ', ' ')
        return texto

    def _clasificar(self, palabra):
        if palabra in VERBS:
            return Token('VERBS', palabra, VERBS[palabra])
        if palabra in DETERMINERS:
            return Token('DET',   palabra)
        if palabra in OBJECT_TYPES:
            return Token('TYPE',  palabra, OBJECT_TYPES[palabra])
        if palabra in PREPOSITIONS:
            return Token('PREP',  palabra)
        if palabra in CONNECTORS:
            return Token('CONNECTOR',  palabra)
        if palabra in EXTENSIONS:
            return Token('EXT',   palabra)
        if palabra in NAMING_WORDS:
            return Token('NAMED_AS', palabra)
        return Token('NAMING', palabra)

    def display_tokens(self, tokens):
        print("── Tokens reconocidos ──────────────────────────────")
        for i, tok in enumerate(tokens, 1):
            print(f"  [{i:2}] {tok}")
        print()
        
        
    def mostrar_dfa(self):
            """Delega la impresión formal del DFA."""
            self.dfa.show()

if __name__ == '__main__':
    lexer = Lexer()
    print ("" + "="*50 + "\n")

    # Mostrar definición formal del DFA
    lexer.mostrar_dfa()
    print ("" + "="*50 + "\n")
    casos = [
        "crea una carpeta llamada proyectos",
        "mueve los archivos pdf a proyectos",
        "elimina los archivos de documentos",
        "copia el archivo txt a respaldo",
        "renombra la carpeta vieja a nueva",
        "crea una carpeta llamada datos y mueve los archivos csv ahí",
    ]

    # for entrada in casos:
    #     print(f'Entrada: "{entrada}"')
    #     tokens = lexer.tokenizar(entrada)
    #     lexer.display_tokens(tokens)
    caso = "crea una carpeta llamada datos y mueve los archivos csv ahí"
    print(f'Entrada: "{caso}"')
    tokens = lexer.tokenizar(caso)
    lexer.display_tokens(tokens)