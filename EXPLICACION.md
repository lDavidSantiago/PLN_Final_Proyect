# Explicación completa del proyecto — Analizador PLN

## ¿Qué hace el proyecto?

Es un **Analizador de Lenguaje Natural (PLN)** en español. El usuario escribe comandos como:

> *"crea una carpeta llamada proyectos"*

Y el sistema los convierte en comandos reales del sistema operativo:

> `mkdir proyectos`

---

## Flujo general

```
frase de texto
     ↓
  [Lexer]         → convierte palabras en Tokens
     ↓
  [Parser]        → construye el Árbol Sintáctico
     ↓
  [Semantic]      → extrae el significado (acción, objeto, destino)
     ↓
  [Simulator]     → genera el comando del sistema (mkdir, mv, rm...)
```

Y hay un módulo extra que corre **antes** del parser:

```
  [Ambiguity]     → detecta frases ambiguas y pregunta al usuario
```

---

## Módulo por módulo

### 1. `dfa.py` — Autómata Finito Determinista

La clase base `DFA` modela un autómata con:

- **Q**: conjunto de estados (`q0`, `q_verb`, `q_det`, etc.)
- **Σ**: alfabeto (las palabras del vocabulario)
- **δ**: función de transición `(estado, símbolo) → siguiente_estado`
- **F**: estados de aceptación

El método clave es `transition(symbol)`: mueve el autómata de un estado a otro. Si no existe transición, va a `q_error`.

---

### 2. `lexer.py` — Analizador Léxico (Gramática Regular)

Es la primera etapa. Toma la frase cruda y la convierte en una lista de **Tokens**.

**Vocabulario definido:**

| Categoría  | Ejemplos                                   |
|------------|--------------------------------------------|
| `VERBS`    | crea, mueve, elimina, copia, renombra, lista |
| `DET`      | el, la, los, las, un, una                  |
| `TYPE`     | carpeta, archivo, directorio               |
| `PREP`     | a, de, en, hacia                           |
| `CONNECTOR`| y, o, luego                               |
| `EXT`      | pdf, txt, csv, py                          |
| `NAMED_AS` | llamada, llamado, nombrada                 |
| `NAMING`   | cualquier otra palabra (nombre libre)      |

El **DFA léxico** (`build_lex_dfa`) mapea cada palabra a un estado de aceptación. Si la palabra está en el vocabulario → Token tipado. Si no → Token tipo `NAMING` (nombre de archivo/carpeta).

**Ejemplo:**

```
"crea una carpeta llamada proyectos"
→ [VERBS:'crea', DET:'una', TYPE:'carpeta', NAMED_AS:'llamada', NAMING:'proyectos']
```

---

### 3. `grammar.py` — Gramática Libre de Contexto (GLC)

Define la **GLC G = (V, T, P, S)**:

- **V** (no terminales): `S`, `CMD_COMP`, `CMD`, `OBJ`, `DEST`
- **T** (terminales): los tipos de token que produce el lexer
- **S** (símbolo inicial): `S`

**Producciones:**

```
P1:  S        → CMD
P2:  S        → CMD_COMP
P3:  CMD_COMP → CMD CONNECTOR CMD
P4:  CMD      → VERBS OBJ
P5:  CMD      → VERBS OBJ DEST
P6:  OBJ      → DET TYPE
P7:  OBJ      → DET TYPE EXT
P8:  OBJ      → DET TYPE NAMING
P9:  OBJ      → DET TYPE NAMED_AS NAMING
P10: OBJ      → DET TYPE EXT NAMED_AS NAMING
P11: DEST     → PREP NAMING
P12: DEST     → NAMED_AS NAMING
P13: DEST     → NAMING
```

---

### 4. `parser.py` — Analizador Sintáctico (Top-Down con Backtracking)

Construye el **árbol de derivación** usando las producciones de la GLC.

**Estrategia:** Descenso recursivo con backtracking.

1. Empieza desde `S`
2. Para cada producción de `S`, intenta hacer match con los tokens
3. Si un símbolo es **terminal** → verifica que el token actual coincida
4. Si es **no terminal** → llama recursivamente a `_parse_variable`
5. Si una producción falla → prueba la siguiente (**backtracking**)
6. Si ninguna funciona → lanza `ParseError`

**Ejemplo de árbol para** `"crea una carpeta llamada proyectos"`:

```
S  [P1]
`-- CMD  [P4]
    |-- VERBS  'crea' (crear)
    `-- OBJ  [P9]
        |-- DET      'una'
        |-- TYPE     'carpeta'
        |-- NAMED_AS 'llamada'
        `-- NAMING   'proyectos'
```

---

### 5. `tree.py` — Árbol de Derivación

La clase `TreeNode` representa cada nodo del árbol:

- **Nodo interior**: tiene `label` (no terminal) + `children` + `production`
- **Nodo hoja**: tiene `label` (tipo de token) + `token`

Métodos relevantes:

- `display()` — imprime el árbol visualmente con formato de árbol
- `display_productions_used()` — muestra las producciones usadas en orden (derivación más a la izquierda)
- `yield_tokens()` — devuelve la lista de tokens hoja de izquierda a derecha

---

### 6. `semantic.py` — Análisis Semántico

Recorre el árbol y extrae un **diccionario de significado**:

```python
{
  'action':      'mkdir',     # comando OS
  'verb':        'crear',     # verbo normalizado
  'object_type': 'carpeta',   # tipo de objeto
  'name':        'proyectos', # nombre
  'extension':   None,        # extensión de archivo
  'destination': None,        # destino
}
```

**Mapeo de verbos a acciones OS:**

| Verbo      | Acción OS |
|------------|-----------|
| crear      | `mkdir`   |
| mover      | `mv`      |
| eliminar   | `rm`      |
| copiar     | `cp`      |
| renombrar  | `mv`      |
| listar     | `ls`      |

Para comandos compuestos (`CMD_COMP`) devuelve una **lista** de dos diccionarios. Además resuelve referencias como "ahi" apuntando al destino del comando anterior.

---

### 7. `ambiguity.py` — Detección y Resolución de Ambigüedad

Detecta dos tipos de ambigüedad **antes** del parser:

**Tipo 1 — Preposición "de":**

Frase: `"elimina los archivos de documentos"`

- Interpretación A: elimina archivos que están **en** la carpeta `documentos`
- Interpretación B: elimina archivos **de tipo/nombre** `documentos`

**Tipo 2 — Destino implícito:**

Frase: `"mueve el archivo pdf informe"`

- Interpretación A: mueve archivos `.pdf` a la carpeta `informe`
- Interpretación B: el objeto se llama `informe.pdf`

Cuando detecta ambigüedad, **le pregunta al usuario** cuál interpretación es la correcta antes de continuar.

---

### 8. `simulator.py` — Simulador de Comandos

Toma el diccionario semántico y genera el comando de terminal equivalente:

| Ejemplo semántico                      | Comando generado      |
|----------------------------------------|-----------------------|
| `mkdir` + nombre `proyectos`           | `mkdir proyectos`     |
| `mv` + ext `pdf` + dest `respaldo`     | `mv *.pdf respaldo/`  |
| `rm` + nombre `vieja` + tipo `carpeta` | `rm -r vieja`         |
| `cp` + ext `txt` + dest `respaldo`     | `cp *.txt respaldo/`  |
| `ls` + tipo `carpeta`                  | `ls -d */`            |

---

### 9. `main.py` — Punto de entrada

Orquesta todo con un menú interactivo:

- **Opción 1**: ingresas una frase manualmente
- **Opción 2**: ejecuta 8 casos demo predefinidos
- **Opción 3**: muestra la GLC (variables, terminales, producciones)
- **Opción 0**: salir

**Flujo en `run_case()`:**

1. Tokeniza con el lexer
2. Verifica ambigüedad → si hay, resuelve interactivamente
3. Si no hay ambigüedad, parsea → árbol sintáctico
4. Extrae semántica del árbol
5. Simula el comando OS

---

## Resumen de la teoría usada

| Concepto                                  | Dónde se aplica                                      |
|-------------------------------------------|------------------------------------------------------|
| **Autómata Finito Determinista (DFA)**    | `dfa.py` + `lexer.py` — clasificación de tokens     |
| **Gramática Regular**                     | Vocabulario del lexer (VERBS, DET, TYPE...)          |
| **Gramática Libre de Contexto (GLC)**     | `grammar.py` — estructura de los comandos            |
| **Parser Top-Down con Backtracking**      | `parser.py` — árbol de derivación                    |
| **Análisis Semántico**                    | `semantic.py` — extracción de significado            |
| **Detección de Ambigüedad**               | `ambiguity.py` — ambigüedad sintáctica               |
