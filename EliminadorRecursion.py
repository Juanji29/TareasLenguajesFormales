import sys
import io
from typing import Dict, List, Set, Tuple


class GrammarProcessor:
    """Clase que encapsula operaciones para eliminar recursi\u00f3n por la izquierda.
    Mantiene la compatibilidad de I/O con el script original.
    """

    @staticmethod
    def read_input() -> List[Tuple[Dict[str, List[List[str]]], List[str]]]:
        """Lee la entrada estándar y devuelve una lista de gramáticas.
        Cada gramática es (dict: no_terminal -> [producciones], orden_no_terminales).
        """
        count = int(input())
        grammars = []

        for _ in range(count):
            k = int(input())
            grammar: Dict[str, List[List[str]]] = {}
            order: List[str] = []

            for _ in range(k):
                line = input().strip()
                left, right = line.split(' -> ')
                parts = right.split()

                productions: List[List[str]] = []
                for token in parts:
                    if token == '|':
                        continue
                    productions.append(list(token))

                grammar[left] = productions
                order.append(left)

            grammars.append((grammar, order))

        return grammars

    @staticmethod
    def has_immediate_left_recursion(prods: List[List[str]], nonterminal: str) -> bool:
        """True si alguna producci\u00f3n comienza con el mismo no terminal."""
        return any(p and p[0] == nonterminal for p in prods)

    @staticmethod
    def generate_new_nonterminal(used: Set[str]) -> str:
        """Genera una nueva letra may\u00fascula no usada; cae en 'X' si se agotan."""
        for ch in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            if ch not in used:
                return ch
        return 'X'

    @classmethod
    def eliminate_immediate_left_recursion(cls, grammar: Dict[str, List[List[str]]], A: str, used: Set[str]) -> None:
        """Elimina la recursi\u00f3n inmediata por la izquierda del no terminal A en el diccionario grammar."""
        prods = grammar.get(A, [])
        recursive = []
        non_recursive = []

        for p in prods:
            if p and p[0] == A:
                recursive.append(p[1:])
            else:
                non_recursive.append(p)

        if not recursive:
            return

        A_prime = cls.generate_new_nonterminal(used)
        used.add(A_prime)

        new_A_prods: List[List[str]] = [nr + [A_prime] for nr in non_recursive]
        grammar[A] = new_A_prods

        new_Aprime_prods: List[List[str]] = [r + [A_prime] for r in recursive]
        new_Aprime_prods.append(['e'])
        grammar[A_prime] = new_Aprime_prods

    @staticmethod
    def substitute_productions(grammar: Dict[str, List[List[str]]], Ai: str, Aj: str) -> None:
        """Sustituye en Ai las producciones que empiezan con Aj por las producciones de Aj."""
        prods_i = grammar.get(Ai, [])
        prods_j = grammar.get(Aj, [])
        new_prods: List[List[str]] = []

        for p in prods_i:
            if p and p[0] == Aj:
                gamma = p[1:]
                for pj in prods_j:
                    new_prods.append(pj + gamma)
            else:
                new_prods.append(p)

        grammar[Ai] = new_prods

    @classmethod
    def eliminate_left_recursion(cls, grammar: Dict[str, List[List[str]]], order: List[str]) -> Dict[str, List[List[str]]]:
        """Algoritmo general para eliminar recursi\u00f3n por la izquierda.
        Mantiene y actualiza grammar en sitio y devuelve el diccionario modificado.
        """
        n = len(order)
        used = set(order)

        for i in range(n):
            Ai = order[i]
            for j in range(i):
                Aj = order[j]
                cls.substitute_productions(grammar, Ai, Aj)

            if cls.has_immediate_left_recursion(grammar.get(Ai, []), Ai):
                cls.eliminate_immediate_left_recursion(grammar, Ai, used)

        return grammar

    @staticmethod
    def format_output(grammar: Dict[str, List[List[str]]], order: List[str]) -> str:
        """Formatea la gram\u00e1tica resultante en las l\u00edneas esperadas."""
        lines: List[str] = []

        # Mantener el orden original de no terminales y agregar nuevos al final
        all_nt = [nt for nt in order if nt in grammar]
        for nt in grammar:
            if nt not in all_nt:
                all_nt.append(nt)

        for nt in all_nt:
            if nt not in grammar:
                continue
            prods = grammar[nt]
            prods_str = [''.join(p) for p in prods]
            lines.append(f"{nt} -> {' '.join(prods_str)}")

        return '\n'.join(lines)


# --- Funciones de control y modos de uso (compatibles con el original) ---

def ejecutar_algoritmo_from_stdin():
    grammars = GrammarProcessor.read_input()
    outputs = []

    for grammar, order in grammars:
        result = GrammarProcessor.eliminate_left_recursion(grammar, order)
        outputs.append(GrammarProcessor.format_output(result, order))

    print('\n\n'.join(outputs))


def run_with_grammar(grammar_line: str) -> None:
    """Corre el algoritmo con una gram\u00e1tica dada (mismo comportamiento que antes)."""
    test_input = f"""1
1
{grammar_line}"""
    original_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(test_input)
        print('=' * 60)
        print('INPUT:')
        print(grammar_line)
        print('=' * 60)
        print('OUTPUT:')
        ejecutar_algoritmo_from_stdin()
        print('=' * 60)
    finally:
        sys.stdin = original_stdin


def modo_interactivo() -> None:
    print('=' * 60)
    print('LEFT RECURSION ELIMINATION - Interactive Mode')
    print('=' * 60)
    print('\nEjemplos de input v\u00e1lido:')
    print('  A -> Aa | b')
    print('  S -> Sa | Sb | c')
    print('  E -> E+T | T')
    print()

    while True:
        grammar = input('Ingresa la gram\u00e1tica: ').strip()
        if grammar:
            run_with_grammar(grammar)
            print()
            continuar = input('¿Quieres procesar otra gram\u00e1tica? (s/n): ').strip().lower()
            if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                print('\n¡Hasta luego!')
                break
            print()
        else:
            print('No ingresaste nada.')
            continuar = input('¿Quieres intentar de nuevo? (s/n): ').strip().lower()
            if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                print('\n¡Hasta luego!')
                break
            print()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        grammar = sys.argv[1]
        run_with_grammar(grammar)
    else:
        modo_interactivo()
