"""
Proyecto: Sistema de Recomendación de Rutas en Red de Campus Universitario
Estructura discreta implementada: Grafo ponderado no dirigido G=(V,E,w)
Autor:
Fecha: Mayo 2026
Institución: UAO
"""

from __future__ import annotations

import heapq
from collections import deque
from typing import Dict, Iterable, List, Optional, Set, Tuple


Nodo = str
Arista = Tuple[Nodo, Nodo, float]


NODOS_CAMPUS_PREDEFINIDOS: List[Nodo] = [
    "Biblioteca",
    "Cafetería",
    "Lab_Sistemas",
    "Auditorio",
    "Rectoría",
    "Deportes",
    "Entrada_Principal",
    "Facultad_Ing",
    "Bienestar",
    "Parqueadero",
]

ARISTAS_CAMPUS_PREDEFINIDAS: List[Tuple[Nodo, Nodo, float]] = [
    ("Entrada_Principal", "Rectoría", 120),
    ("Entrada_Principal", "Parqueadero", 80),
    ("Rectoría", "Biblioteca", 200),
    ("Rectoría", "Auditorio", 150),
    ("Biblioteca", "Lab_Sistemas", 90),
    ("Biblioteca", "Cafetería", 110),
    ("Lab_Sistemas", "Facultad_Ing", 60),
    ("Facultad_Ing", "Cafetería", 140),
    ("Facultad_Ing", "Bienestar", 170),
    ("Auditorio", "Deportes", 130),
    ("Deportes", "Bienestar", 95),
    ("Bienestar", "Cafetería", 85),
    ("Parqueadero", "Deportes", 200),
    ("Cafetería", "Auditorio", 160),
    ("Lab_Sistemas", "Bienestar", 210),
]


class GrafoCampus:
    """Modela un grafo ponderado no dirigido G=(V,E,w) para rutas de campus.

    La representación principal es una lista de adyacencia:
    adj: V -> [(u, w(v,u))].
    Por simetría de grafos no dirigidos, (u,v)∈E implica (v,u)∈E con mismo peso.
    """

    def __init__(self) -> None:
        """Inicializa un grafo vacío con V=∅ y E=∅. Complejidad: O(1)."""
        self.adyacencia: Dict[Nodo, List[Tuple[Nodo, float]]] = {}

    def agregar_nodo(self, nodo: Nodo) -> None:
        """Agrega un vértice a V.

        Parámetros:
            nodo: etiqueta del vértice.

        Complejidad: O(1) promedio con diccionario hash.
        """
        if not nodo or not isinstance(nodo, str):
            raise ValueError("El nombre del nodo debe ser un texto no vacío.")
        if nodo not in self.adyacencia:
            self.adyacencia[nodo] = []

    def agregar_arista(self, nodo1: Nodo, nodo2: Nodo, peso: float) -> None:
        """Agrega o actualiza una arista no dirigida (nodo1,nodo2) con peso positivo.

        Formalmente, actualiza E := E ∪ {(nodo1,nodo2)} y w(nodo1,nodo2)=peso,
        respetando simetría: w(nodo1,nodo2)=w(nodo2,nodo1).

        Complejidad: O(grado(nodo1)+grado(nodo2)) por búsqueda/reemplazo local.
        """
        if nodo1 == nodo2:
            raise ValueError("No se permiten lazos (aristas de un nodo consigo mismo).")
        if peso <= 0:
            raise ValueError("El peso debe ser un número positivo.")

        self.agregar_nodo(nodo1)
        self.agregar_nodo(nodo2)

        self._agregar_o_reemplazar_vecino(nodo1, nodo2, float(peso))
        self._agregar_o_reemplazar_vecino(nodo2, nodo1, float(peso))

    def _agregar_o_reemplazar_vecino(self, origen: Nodo, destino: Nodo, peso: float) -> None:
        for i, (vecino, _) in enumerate(self.adyacencia[origen]):
            if vecino == destino:
                self.adyacencia[origen][i] = (destino, peso)
                return
        self.adyacencia[origen].append((destino, peso))

    def cargar_grafo_predefinido(self) -> None:
        """Carga un grafo de campus con |V|=10 y |E|=15.

        Caso de uso real: este sistema puede integrarse en una app móvil de
        orientación universitaria para guiar estudiantes nuevos entre edificios.

        Complejidad: O(|V|+|E|).
        """
        self.adyacencia.clear()
        for nodo in NODOS_CAMPUS_PREDEFINIDOS:
            self.agregar_nodo(nodo)
        for nodo1, nodo2, peso in ARISTAS_CAMPUS_PREDEFINIDAS:
            self.agregar_arista(nodo1, nodo2, peso)

    def obtener_lista_adyacencia(self) -> Dict[Nodo, List[Tuple[Nodo, float]]]:
        """Retorna una copia de la lista de adyacencia de G.

        Complejidad: O(|V|+|E|).
        """
        return {nodo: sorted(vecinos)[:] for nodo, vecinos in self.adyacencia.items()}

    def obtener_matriz_adyacencia(self) -> Tuple[List[Nodo], List[List[float]]]:
        """Construye la matriz de adyacencia A de un grafo ponderado no dirigido.

        A[i][j]=w(v_i,v_j) si (v_i,v_j)∈E; en otro caso 0.
        En grafos no dirigidos A es simétrica: A[i][j]=A[j][i].

        Retorna:
            (nodos_ordenados, matriz)

        Complejidad: O(|V|^2 + |E|).
        """
        nodos = sorted(self.adyacencia.keys())
        indice = {nodo: i for i, nodo in enumerate(nodos)}
        n = len(nodos)
        matriz = [[0.0 for _ in range(n)] for _ in range(n)]

        for origen, vecinos in self.adyacencia.items():
            i = indice[origen]
            for destino, peso in vecinos:
                j = indice[destino]
                matriz[i][j] = peso

        return nodos, matriz

    def grados_nodos(self) -> Dict[Nodo, int]:
        """Calcula grado(v) para cada vértice v∈V.

        En un grafo no dirigido simple, grado(v)=|N(v)|.
        Complejidad: O(|V|).
        """
        return {nodo: len(vecinos) for nodo, vecinos in self.adyacencia.items()}

    def bfs(self, inicio: Nodo) -> List[Nodo]:
        """Realiza BFS (Búsqueda en Anchura) desde un nodo inicial.

        Explora por capas y obtiene el conjunto de alcanzabilidad R(inicio).
        Complejidad: O(|V|+|E|).
        """
        self._validar_nodo_existente(inicio)

        visitados: Set[Nodo] = {inicio}
        cola: deque[Nodo] = deque([inicio])
        recorrido: List[Nodo] = []

        while cola:
            actual = cola.popleft()
            recorrido.append(actual)
            for vecino, _ in self.adyacencia[actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(vecino)

        return recorrido

    def es_conexo(self) -> bool:
        """Verifica conexidad de G usando BFS.

        Propiedad: G es conexo ↔ existe v∈V tal que BFS(v) alcanza todos los vértices.
        Si V=∅ se considera conexo por convención vacía.

        Complejidad: O(|V|+|E|).
        """
        if not self.adyacencia:
            return True
        inicio = next(iter(self.adyacencia))
        return len(self.bfs(inicio)) == len(self.adyacencia)

    def tiene_ciclos(self) -> bool:
        """Detecta ciclos en un grafo no dirigido mediante DFS.

        En DFS, existe ciclo si aparece una arista de retroceso hacia un vértice
        visitado distinto del padre en el árbol DFS.

        Complejidad: O(|V|+|E|).
        """
        visitados: Set[Nodo] = set()

        def dfs(actual: Nodo, padre: Optional[Nodo]) -> bool:
            visitados.add(actual)
            for vecino, _ in self.adyacencia[actual]:
                if vecino not in visitados:
                    if dfs(vecino, actual):
                        return True
                elif vecino != padre:
                    return True
            return False

        for nodo in self.adyacencia:
            if nodo not in visitados and dfs(nodo, None):
                return True
        return False

    def dijkstra(self, origen: Nodo, destino: Nodo) -> Tuple[float, List[Nodo]]:
        """Implementa Dijkstra para camino mínimo en G=(V,E,w), con w(e)≥0.

        Justificación formal (teorema de optimalidad): al extraer de la cola de
        prioridad el vértice u con distancia tentativa mínima, d[u] es óptima y no
        puede mejorarse por pesos no negativos. Repitiendo, se obtiene la distancia
        mínima desde origen hasta todos los vértices alcanzables.

        Parámetros:
            origen: vértice de inicio.
            destino: vértice final.

        Retorna:
            (distancia_mínima, camino)

        Lanza:
            ValueError si los nodos no existen.

        Complejidad: O((|V|+|E|) log |V|) con min-heap.
        """
        self._validar_nodo_existente(origen)
        self._validar_nodo_existente(destino)

        distancias: Dict[Nodo, float] = {nodo: float("inf") for nodo in self.adyacencia}
        predecesor: Dict[Nodo, Optional[Nodo]] = {nodo: None for nodo in self.adyacencia}
        distancias[origen] = 0.0

        heap: List[Tuple[float, Nodo]] = [(0.0, origen)]

        while heap:
            dist_actual, actual = heapq.heappop(heap)
            if dist_actual > distancias[actual]:
                continue
            if actual == destino:
                break

            for vecino, peso in self.adyacencia[actual]:
                nueva_dist = dist_actual + peso
                if nueva_dist < distancias[vecino]:
                    distancias[vecino] = nueva_dist
                    predecesor[vecino] = actual
                    heapq.heappush(heap, (nueva_dist, vecino))

        if distancias[destino] == float("inf"):
            return float("inf"), []

        camino = self._reconstruir_camino(predecesor, destino)
        return distancias[destino], camino

    def kruskal_mst(self) -> Tuple[List[Arista], float]:
        """Calcula el Árbol de Expansión Mínima usando Kruskal.

        Kruskal ordena aristas por peso no decreciente y agrega una arista e∈E
        sólo si conecta dos componentes distintas (estructura de conjuntos disjuntos).
        Correctitud por propiedad de corte de MST.

        Retorna:
            (aristas_mst, peso_total)

        Lanza:
            ValueError si el grafo no es conexo y no existe un árbol que abarque V.

        Complejidad: O(|E| log |E|).
        """
        if not self.adyacencia:
            return [], 0.0
        if not self.es_conexo():
            raise ValueError("El grafo no es conexo; no existe un árbol de expansión mínima único para todos los nodos.")

        parent: Dict[Nodo, Nodo] = {nodo: nodo for nodo in self.adyacencia}
        rank: Dict[Nodo, int] = {nodo: 0 for nodo in self.adyacencia}

        def find(x: Nodo) -> Nodo:
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x: Nodo, y: Nodo) -> bool:
            rx, ry = find(x), find(y)
            if rx == ry:
                return False
            if rank[rx] < rank[ry]:
                parent[rx] = ry
            elif rank[rx] > rank[ry]:
                parent[ry] = rx
            else:
                parent[ry] = rx
                rank[rx] += 1
            return True

        aristas_ordenadas = sorted(self.obtener_aristas(), key=lambda e: e[2])
        mst: List[Arista] = []
        peso_total = 0.0

        for u, v, w in aristas_ordenadas:
            if union(u, v):
                mst.append((u, v, w))
                peso_total += w
                if len(mst) == len(self.adyacencia) - 1:
                    break

        return mst, peso_total

    def obtener_aristas(self) -> List[Arista]:
        """Retorna la lista de aristas únicas E en formato (u,v,w).

        Complejidad: O(|V|+|E|).
        """
        vistas: Set[frozenset[Nodo]] = set()
        aristas: List[Arista] = []

        for u, vecinos in self.adyacencia.items():
            for v, w in vecinos:
                clave = frozenset((u, v))
                if clave not in vistas:
                    vistas.add(clave)
                    aristas.append((u, v, w))

        return aristas

    def _validar_nodo_existente(self, nodo: Nodo) -> None:
        if nodo not in self.adyacencia:
            raise ValueError(f"El nodo '{nodo}' no existe en el grafo.")

    @staticmethod
    def _reconstruir_camino(predecesor: Dict[Nodo, Optional[Nodo]], destino: Nodo) -> List[Nodo]:
        camino: List[Nodo] = []
        actual: Optional[Nodo] = destino
        while actual is not None:
            camino.append(actual)
            actual = predecesor[actual]
        camino.reverse()
        return camino


__all__ = [
    "GrafoCampus",
    "NODOS_CAMPUS_PREDEFINIDOS",
    "ARISTAS_CAMPUS_PREDEFINIDAS",
]
