import sys
from itertools import combinations
from typing import Dict, List, Set, Tuple


def _leer_linea_stripped() -> str:
    """Lee una línea de stdin y la devuelve sin espacios finales; cadena vacía si EOF."""
    linea = sys.stdin.readline()
    return linea.strip() if linea else ""


class Minimizador:
    """Encapsula la lógica de marcado para encontrar pares equivalentes en un DFA."""

    def __init__(self, num_estados: int, alfabeto: List[str], estados_finales: Set[int], transiciones: Dict[int, Dict[str, int]]):
        self.n = num_estados
        self.alfabeto = alfabeto
        self.finales = estados_finales
        self.trans = transiciones

    def _marcado_inicial(self) -> Set[Tuple[int, int]]:
        marcado = set()
        for a, b in combinations(range(self.n), 2):
            if (a in self.finales) ^ (b in self.finales):
                marcado.add((a, b))
        return marcado

    def _iterar_marcado(self, marcado: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        cambiado = True
        while cambiado:
            cambiado = False
            for a, b in combinations(range(self.n), 2):
                if (a, b) in marcado:
                    continue
                for s in self.alfabeto:
                    na = self.trans[a][s]
                    nb = self.trans[b][s]
                    par_norm = (na, nb) if na <= nb else (nb, na)
                    if par_norm in marcado:
                        marcado.add((a, b))
                        cambiado = True
                        break
        return marcado

    def pares_equivalentes(self) -> List[str]:
        marcado = self._marcado_inicial()
        marcado = self._iterar_marcado(marcado)
        equivalentes = []
        for a, b in combinations(range(self.n), 2):
            if (a, b) not in marcado:
                equivalentes.append(f"({a}, {b})")
        return equivalentes


def procesar_caso() -> bool:
    """Procesa un único caso desde stdin; devuelve False en EOF o error."""
    try:
        num_estados_line = _leer_linea_stripped()
        if not num_estados_line:
            return False
        num_estados = int(num_estados_line)

        alfabeto = _leer_linea_stripped().split()
        finales_line = _leer_linea_stripped()
        estados_finales = set(map(int, finales_line.split())) if finales_line else set()

        transiciones: Dict[int, Dict[str, int]] = {}
        for i in range(num_estados):
            fila = _leer_linea_stripped().split()
            transiciones[i] = {alfabeto[j]: int(fila[j]) for j in range(len(alfabeto))}

    except (IOError, ValueError):
        return False

    m = Minimizador(num_estados, alfabeto, estados_finales, transiciones)
    resultado = m.pares_equivalentes()
    print(" ".join(resultado))
    return True


def principal() -> None:
    try:
        casos_line = _leer_linea_stripped()
        if not casos_line:
            return
        casos = int(casos_line)
        for _ in range(casos):
            if not procesar_caso():
                break
    except (IOError, ValueError):
        return


if __name__ == "__main__":
    principal()