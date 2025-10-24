# Tareas Lenguajes Formales

## Juan Esteban Jimenez 

Este repositorio contiene dos scripts de utilidad relacionados con autómatas y gramáticas en teoría de lenguajes formales:

- `Minimizador.py` — Encuentra pares de estados equivalentes en un DFA (refactorizado en clase `Minimizador`).
- `EliminadorRecursion.py` — Elimina recursión por la izquierda inmediata y general en gramáticas, preservando formato de entrada/salida.

A continuación se describe la funcionalidad, formato de entrada/salida, ejemplos de uso y notas prácticas.

## Archivos y propósito

### `Minimizador.py`
- Objetivo: Dado un DFA descrito por su número de estados, alfabeto, estados finales y tabla de transición, calcula los pares de estados equivalentes (no distinguibles) usando el algoritmo de llenado de tabla.
- Estructura principal: Clase `Minimizador` que encapsula:
  - `_marcado_inicial()` — marca pares donde uno es final y otro no.
  - `_iterar_marcado()` — propaga el marcado según las transiciones.
  - `pares_equivalentes()` — devuelve la lista de pares equivalentes en formato `("(i, j)")`.
- Funciones auxiliares para I/O: `_leer_linea_stripped()`, `procesar_caso()` y `principal()`.

Formato de entrada (por stdin):
1. Línea 1: número de casos (C)
Por cada caso:
- Línea 1: número de estados (n)
- Línea 2: símbolos del alfabeto separados por espacios (por ejemplo: `a b`)
- Línea 3: índices de estados finales separados por espacios (ej. `2 3`) — puede estar vacía si no hay finales
- Siguientes n líneas: cada línea es la fila de la tabla de transición: |alfabeto| enteros separados por espacios (destinos por símbolo)

Salida (por stdout):
- Para cada caso se imprime una línea con los pares equivalentes separados por espacios, cada par con el formato `(i, j)`. Si no hay pares equivalentes la línea estará vacía.



### `EliminadorRecursion.py`
- Objetivo: Eliminar recursión por la izquierda en gramáticas (inmediata y la general según el algoritmo clásico).
- Estructura principal: Clase `GrammarProcessor` con métodos estáticos/cls:
  - `read_input()` — parsea entrada en el formato del script original.
  - `eliminate_left_recursion()` — algoritmo general (sustitución + eliminación inmediata).
  - `eliminate_immediate_left_recursion()` — transforma A -> Aα | β en A y A' según convención.
  - `format_output()` — prepara la representación en texto para imprimir.
- Modo de uso: conserva los mismos modos del script original:
  - Pasar la gramática como argumento en la línea de comandos (llama a `run_with_grammar`) — útil para pruebas rápidas.
  - Modo interactivo: si no se pasan argumentos pide la gramática por stdin.

Formato de entrada esperado por `GrammarProcessor.read_input()` (stdin):
1. Línea 1: número de gramáticas (G)
Por cada gramática:
- Línea 1: número de no terminales k
- Siguientes k líneas: producciones en la forma `A -> Aa | b` donde el separador `|` se usa entre alternativas.

Formato de salida:
- Lista de producciones transformadas, una por línea, con el mismo estilo `A -> prod1 prod2 ...`.
- Si hay múltiples gramáticas, se separan por una línea en blanco doble.

Ejemplo (ejecutando con argumento desde PowerShell):
```powershell
python "c:\EliminadorRecursion.py" "A -> Aa | b"
```
Salida mostrada (ejemplo):
```
A -> bB
B -> aB e
```
(El script usa `e` para denotar la cadena vacía/épsilon en la salida de este implementador.)

## Notas importantes
- Los scripts mantienen compatibilidad con su comportamiento original: no cambié la semántica, solo la organización del código y la legibilidad.
- Ambos scripts leen desde `stdin` cuando se ejecutan sin argumentos y también permiten modos de prueba (argumento o funciones helper internas).
- `EliminadorRecursion.py` usa listas de símbolos por producción (`['A','a']`), pero al formatear la salida concatena esos símbolos para mostrar `Aa`.

## Cómo probar localmente
1. Abrir PowerShell (en Windows) y ejecutar ejemplos como los mostrados en las secciones anteriores.
2. Para pruebas automatizadas rápidas puedes redirigir cadenas con `io.StringIO` desde Python (los scripts ya incluyen helpers de prueba en su código).

## Siguientes mejoras sugeridas
- Añadir un conjunto de tests con `pytest` que cubran varios DFAs y gramáticas con y sin recursión izquierda, comprobando la salida esperada.
- Reemplazar la representación del épsilon `e` por `ε` si se desea mayor claridad (solo visual).
- Añadir validación de entrada más robusta (mensajes de error claros cuando la entrada no tenga el formato esperado).

---

