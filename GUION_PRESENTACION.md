# Guion de presentación — Analizador PLN

> Duración estimada: 10-12 minutos. Ajusta según el tiempo que te den.

---

## 1. Introducción (1 min)

"Buenas, vamos a presentar un **Analizador de Lenguaje Natural en español** que toma comandos escritos como hablaría una persona y los traduce a comandos reales de sistema de archivos.

Por ejemplo, si yo escribo:

> *'crea una carpeta llamada proyectos'*

el sistema lo analiza y devuelve:

> `mkdir proyectos`

Todo el proyecto está construido aplicando teoría de lenguajes formales: autómatas finitos, gramáticas regulares, gramáticas libres de contexto, árboles de derivación, análisis semántico y resolución de ambigüedad. Básicamente, replicamos en miniatura las primeras fases de un compilador."

---

## 2. El flujo general (1 min)

"El sistema procesa cada frase en 5 etapas, cada una transformando la información en una representación más abstracta:

```
texto plano
   → LEXER        (tokeniza y clasifica palabras)
   → AMBIGUEDAD   (detecta frases con doble interpretación)
   → PARSER       (construye el árbol sintáctico)
   → SEMÁNTICA    (extrae el significado: acción, objeto, destino)
   → SIMULADOR    (genera el comando final)
```

Vamos a recorrer cada módulo en ese orden."

---

## 3. `dfa.py` — La base teórica (1 min)

"Todo arranca con la clase `DFA`, que implementa formalmente un **Autómata Finito Determinista**: la quíntupla `(Q, Σ, δ, q0, F)` — estados, alfabeto, función de transición, estado inicial y estados de aceptación.

Tiene métodos como `transition()`, que aplica la función δ, y `process()`, que recorre una cadena completa y dice si termina en un estado de aceptación.

Esta clase es genérica, no sabe nada de español ni de carpetas — es la pieza matemática que reutiliza el lexer."

---

## 4. `lexer.py` — Análisis léxico (2 min)

"El lexer convierte la frase en una lista de **tokens**. Primero define el vocabulario — listas de palabras agrupadas por categoría:

- `VERBS`: crea, mueve, elimina, copia, renombra, lista...
- `DET`: el, la, los, las, un, una...
- `TYPE`: carpeta, archivo, directorio...
- `PREP`: a, de, en, hacia...
- `CONNECTOR`: y, o, luego...
- `EXT`: pdf, txt, csv, py...
- `NAMED_AS`: llamada, llamado, nombrada...

Esto es, literalmente, una **gramática regular**: cada categoría es un conjunto cerrado de palabras.

El método `tokenizar()` hace tres cosas:
1. Normaliza el texto (minúsculas, quita signos de puntuación, colapsa espacios).
2. Separa en palabras.
3. Clasifica cada palabra: si está en algún vocabulario, le asigna su tipo y su forma normalizada (por ejemplo 'carpetas' se normaliza a 'carpeta', 'crea' a 'crear'). Si NO está en ningún vocabulario, se clasifica como `NAMING` — el 'cajón de sastre' para nombres propios de archivos y carpetas.

Resultado para 'crea una carpeta llamada proyectos':

```
[VERBS:'crea', DET:'una', TYPE:'carpeta', NAMED_AS:'llamada', NAMING:'proyectos']
```"

---

## 5. `grammar.py` — La Gramática Libre de Contexto (2 min)

"Con los tokens ya clasificados, necesitamos saber si la *secuencia* de tipos tiene sentido gramatical. Para eso definimos una **GLC**: `G = (V, T, P, S)`.

- **V** (no terminales): `S`, `CMD_COMP`, `CMD`, `OBJ`, `DEST`
- **T** (terminales): los tipos de token — VERBS, DET, TYPE, PREP, CONNECTOR, EXT, NAMED_AS, NAMING
- **S**: símbolo inicial

Las producciones más importantes son:

```
CMD  → VERBS OBJ DEST   (verbo + objeto + destino)
CMD  → VERBS OBJ        (verbo + objeto, sin destino)
OBJ  → DET TYPE EXT NAMED_AS NAMING   (ej: 'el archivo pdf llamado informe')
OBJ  → DET TYPE NAMING                 (ej: 'la carpeta vieja')
OBJ  → DET TYPE                        (ej: 'los archivos')
DEST → PREP NAMING       (ej: 'a respaldo')
```

Un detalle importante: el **orden** de estas producciones no es casual. Las más largas y específicas van primero — esto sirve como heurística de 'mejor coincidencia primero', porque el parser las prueba en ese orden."

---

## 6. `parser.py` — Descenso recursivo con backtracking (2 min)

"El parser toma los tokens y construye el **árbol de derivación** siguiendo la GLC. La estrategia es:

1. Empieza en `S`.
2. Para cada producción de `S`, intenta hacer 'match' con los tokens, símbolo por símbolo.
3. Si el símbolo es terminal, compara directamente con el token actual.
4. Si es no terminal, llama recursivamente para intentar derivarlo.
5. Si una producción falla a mitad de camino, se descarta por completo y se prueba la **siguiente** producción — esto es el *backtracking*.
6. Si ninguna producción funciona, se lanza un `ParseError` que indica exactamente qué token causó el problema.

Para 'crea una carpeta llamada proyectos', el árbol resultante es:

```
S [P1]
└── CMD [P4]
    ├── VERBS 'crea'
    └── OBJ [P9]
        ├── DET 'una'
        ├── TYPE 'carpeta'
        ├── NAMED_AS 'llamada'
        └── NAMING 'proyectos'
```"

---

## 7. `tree.py` — El árbol de derivación (30 seg)

"`TreeNode` es la estructura que representa ese árbol. Cada nodo interior tiene una etiqueta (no terminal) y la producción usada; cada hoja tiene un token. Tiene métodos para imprimir el árbol visualmente y para listar, en orden, las producciones usadas — es decir, la derivación más a la izquierda."

---

## 8. `ambiguity.py` — Detección de ambigüedad (1.5 min)

"Antes de parsear, detectamos si la frase puede interpretarse de **dos formas distintas**, aunque gramaticalmente sea válida. Manejamos dos casos:

**Caso 1**: 'elimina los archivos de documentos' — '*de documentos*' puede significar:
- (a) elimina los archivos QUE ESTÁN DENTRO de la carpeta 'documentos', o
- (b) elimina archivos cuyo nombre/tipo es 'documentos'.

**Caso 2**: 'mueve el archivo pdf informe' — sin preposición clara, 'informe' puede ser:
- (a) el nombre del destino (mover los .pdf a la carpeta 'informe'), o
- (b) el nombre del archivo mismo ('informe.pdf').

Cuando se detecta uno de estos patrones, el sistema **le pregunta al usuario** cuál interpretación es correcta, y construye directamente el significado — saltándose el parser para ese caso."

---

## 9. `semantic.py` — Análisis semántico (1.5 min)

"Si no hubo ambigüedad, el árbol pasa al módulo semántico, que lo recorre y extrae un diccionario con el **significado**:

```python
{
  'action':      'mkdir',
  'verb':        'crear',
  'object_type': 'carpeta',
  'name':        'proyectos',
  'extension':   None,
  'destination': None,
}
```

Los verbos se mapean a acciones de sistema:

| Verbo     | Acción |
|-----------|--------|
| crear     | mkdir  |
| mover     | mv     |
| eliminar  | rm     |
| copiar    | cp     |
| renombrar | mv     |
| listar    | ls     |

Para comandos compuestos como 'crea una carpeta llamada datos y mueve los archivos csv ahí', devuelve una **lista de dos diccionarios**, y además resuelve la palabra 'ahí' apuntando al destino o nombre del comando anterior — esto es resolución de referencias, un concepto típico de PLN."

---

## 10. `simulator.py` — Generación del comando final (1 min)

"Por último, el simulador toma ese diccionario y genera el string del comando real, según la acción:

| Semántica                          | Comando generado    |
|-------------------------------------|----------------------|
| mkdir + nombre 'proyectos'          | `mkdir proyectos`    |
| mv + ext 'pdf' + dest 'respaldo'    | `mv *.pdf respaldo/` |
| rm + nombre 'vieja' (carpeta)       | `rm -r vieja`        |
| cp + ext 'txt' + dest 'respaldo'    | `cp *.txt respaldo/` |
| ls + tipo 'carpeta'                 | `ls -d */`           |"

---

## 11. `main.py` — El orquestador y demo (1 min)

"`main.py` arma todas las piezas en un menú interactivo:

- Opción 1: ingresar una frase manualmente.
- Opción 2: correr 8 casos demo predefinidos.
- Opción 3: mostrar la definición formal de la gramática (V, T, P, S).
- Opción 0: salir.

Cada frase pasa por la función `run_case()`, que ejecuta el pipeline completo y muestra en pantalla: los tokens, el árbol, las producciones usadas, la semántica extraída y el comando final simulado."

---

## 12. El "motor" del proyecto — cierre (1.5 min)

"Para cerrar: el verdadero motor del proyecto es este **pipeline de transformación de representaciones**, igual que las primeras fases de un compilador:

```
texto → tokens → árbol sintáctico → significado → comando
```

Lo que sostiene todo esto es la **coherencia entre tres piezas**:

1. La **gramática** (`grammar.py`), que define qué secuencias de tokens son válidas y en qué orden probarlas (las producciones más específicas primero).
2. El **parser** (`parser.py`), que usa backtracking para encontrar la derivación correcta según ese orden.
3. La **semántica** (`semantic.py`), que asume — basándose en el ID de cada producción (P6 a P13) — en qué posición exacta del árbol está cada dato (nombre, extensión, destino).

Si cambiamos una producción de la gramática, tenemos que actualizar también el código semántico que la interpreta, porque están acopladas por convención.

Con esto demostramos en la práctica los conceptos de DFA, gramática regular, GLC, árboles de derivación, ambigüedad sintáctica y análisis semántico — todo aplicado a un caso de uso concreto y entendible: comandos de archivos en español natural."

---

## Preguntas frecuentes que te pueden hacer (preparación)

- **¿Por qué usan backtracking y no un parser más eficiente (LL/LR)?**
  → Porque el objetivo es demostrar el concepto de derivación con una gramática pequeña y ambigua a propósito; la eficiencia no es la prioridad. Con esta gramática el backtracking es perfectamente manejable.

- **¿Qué pasa si la frase no coincide con ninguna producción?**
  → El parser lanza un `ParseError` que indica qué tokens se reconocieron y cuál fue el primer token que rompió el patrón.

- **¿Cómo manejan la ambigüedad?**
  → Con un módulo previo (`ambiguity.py`) que detecta dos patrones específicos por tipo de token y le pregunta al usuario cuál interpretación aplicar, antes de llegar al parser.

- **¿Qué es 'ahí' en 'mueve los archivos csv ahí'?**
  → Es una referencia anafórica: el sistema la resuelve mirando el destino (o nombre) del comando anterior en una frase compuesta.
