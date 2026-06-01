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