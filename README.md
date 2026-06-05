# Analizador PLN

Analiza y comandos en lenguaje natural en espanol y simula comandos de sistema de archivos.

Ejemplo de entrada:

```text
crea una carpeta llamada proyectos
```

## Requisitos

- Python 3
- No requiere instalar librerias externas.

## Como ejecutar

Desde la carpeta del proyecto, ejecuta:

```bash
python main.py
```

O tambien:

```bash
py main.py
```

Al iniciar, el sistema muestra un menu:

- `1` para ingresar una frase manualmente.
- `2` para ejecutar casos demo.
- `3` para ver informacion de la gramatica.
- `0` para salir.

## Componentes

- `main.py`: punto de entrada del programa y menu interactivo.
- `lexer.py`: tokeniza la frase y clasifica cada palabra.
- `dfa.py`: implementa el automata finito usado por el analizador lexico.
- `grammar.py`: define la gramatica libre de contexto.
- `parser.py`: construye el arbol sintactico usando la gramatica.
- `tree.py`: representa y muestra el arbol de derivacion.
- `semantic.py`: extrae el significado del arbol sintactico.
- `ambiguity.py`: detecta y resuelve frases ambiguas.
- `simulator.py`: genera el comando simulado del sistema de archivos.

## Flujo general

```text
frase -> lexer -> parser -> semantica -> simulador
```
