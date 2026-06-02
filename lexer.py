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
            return Token('VERBO', palabra, VERBS[palabra])
        if palabra in DETERMINERS:
            return Token('DET',   palabra)
        if palabra in OBJECT_TYPES:
            return Token('TIPO',  palabra, OBJECT_TYPES[palabra])
        if palabra in PREPOSITIONS:
            return Token('PREP',  palabra)
        if palabra in CONNECTORS:
            return Token('CONJ',  palabra)
        if palabra in EXTENSIONS:
            return Token('EXT',   palabra)
        if palabra in NAMING_WORDS:
            return Token('LLAMA', palabra)
        return Token('NOMBRE', palabra)

    def mostrar_tokens(self, tokens):
        print("── Tokens reconocidos ──────────────────────────────")
        for i, tok in enumerate(tokens, 1):
            print(f"  [{i:2}] {tok}")
        print()