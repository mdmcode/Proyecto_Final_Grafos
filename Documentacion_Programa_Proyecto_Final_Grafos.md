# Documentación técnica detallada — Proyecto Final de Grafos

**Proyecto:** Sistema de Recomendación de Rutas en Red de Campus Universitario  
**Estructura discreta implementada:** Grafo ponderado no dirigido \(G=(V,E,w)\)  
**Lenguaje:** Python  
**Fecha:** Mayo 2026  

---

## 1. Propósito y contexto

El objetivo del proyecto es **modelar un campus universitario como un grafo ponderado no dirigido** para resolver problemas reales de navegación: encontrar rutas mínimas entre edificios, verificar conectividad, detectar ciclos y construir un árbol de expansión mínima. El sistema ofrece una **interfaz de consola** y una **visualización gráfica** del grafo.

### ¿Cómo se aplica la teoría de grafos?

- **Vértices (V):** edificios del campus.
- **Aristas (E):** caminos entre edificios.
- **Peso de arista (w):** distancia en metros entre edificios.
- **Problemas resueltos con teoría de grafos:**
  - **Ruta mínima:** algoritmo de **Dijkstra**.
  - **Conectividad:** **BFS**.
  - **Ciclos:** **DFS**.
  - **Árbol de expansión mínima:** **Kruskal**.

---

## 2. Estructura del proyecto

- **`grafo.py`**: implementación del modelo y algoritmos de grafos.
- **`main.py`**: flujo principal e interfaz de consola.
- **`visualizacion.py`**: representación gráfica con NetworkX y Matplotlib.

---

## 3. Modelo matemático y representación

### 3.1 Definición formal

El grafo se define como \(G=(V,E,w)\), donde:

- \(V\) es el conjunto de edificios (nodos).
- \(E\subseteq V\times V\) son los caminos (aristas no dirigidas).
- \(w: E \to \mathbb{R}^+\) asigna el peso (distancia positiva en metros).

### 3.2 Representación computacional

Se utiliza **lista de adyacencia**:

- `adyacencia[v] = [(u, w(v,u)), ...]`
- Para grafo no dirigido: si \((u,v)\in E\), entonces aparecen **ambas direcciones** en la lista.

Código clave:

```python
class GrafoCampus:
    def __init__(self) -> None:
        self.adyacencia: Dict[Nodo, List[Tuple[Nodo, float]]] = {}
```

---

## 4. Funciones principales relacionadas con teoría de grafos

A continuación se muestran los fragmentos más relevantes del núcleo algorítmico, que conectan directamente con teoría de grafos.

### 4.1 Inserción de vértices y aristas (modelo \(V\) y \(E\))

```python
def agregar_nodo(self, nodo: Nodo) -> None:
    if not nodo or not isinstance(nodo, str):
        raise ValueError("El nombre del nodo debe ser un texto no vacío.")
    if nodo not in self.adyacencia:
        self.adyacencia[nodo] = []

def agregar_arista(self, nodo1: Nodo, nodo2: Nodo, peso: float) -> None:
    if nodo1 == nodo2:
        raise ValueError("No se permiten lazos (aristas de un nodo consigo mismo).")
    if peso <= 0:
        raise ValueError("El peso debe ser un número positivo.")

    self.agregar_nodo(nodo1)
    self.agregar_nodo(nodo2)
    self._agregar_o_reemplazar_vecino(nodo1, nodo2, float(peso))
    self._agregar_o_reemplazar_vecino(nodo2, nodo1, float(peso))
```

**Teoría aplicada:** construcción explícita de \(V\) y \(E\) con pesos positivos, respetando simetría del grafo no dirigido.

---

### 4.2 BFS — Conectividad de grafos

```python
def bfs(self, inicio: Nodo) -> List[Nodo]:
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
```

**Aplicación:** verificar si el grafo es conexo (todos los edificios alcanzables) usando BFS.

---

### 4.3 DFS — Detección de ciclos

```python
def tiene_ciclos(self) -> bool:
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
```

**Teoría aplicada:** detección de ciclos en grafos no dirigidos mediante aristas de retroceso en DFS.

---

### 4.4 Dijkstra — Camino mínimo ponderado

```python
def dijkstra(self, origen: Nodo, destino: Nodo) -> Tuple[float, List[Nodo]]:
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
```

**Teoría aplicada:** algoritmo de caminos mínimos con pesos no negativos, ideal para distancias físicas en campus.

---

### 4.5 Kruskal — Árbol de expansión mínima (MST)

```python
def kruskal_mst(self) -> Tuple[List[Arista], float]:
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
```

**Teoría aplicada:** construcción de MST usando la **propiedad de corte**. Útil para minimizar cableado o rutas base de mantenimiento.

---

## 5. Flujo del sistema (cómo se ejecuta)

1. **El usuario inicia** el programa (`main.py`).
2. **Carga un grafo predefinido** o crea nuevos nodos/aristas.
3. **Ejecuta algoritmos** desde el menú (Dijkstra, BFS, DFS, Kruskal).
4. **Obtiene resultados** en consola (rutas, conectividad, ciclos, MST).
5. **Opcionalmente visualiza** el grafo con resaltados de camino mínimo o MST.

---

## 6. Visualización (apoyo didáctico)

La visualización usa **NetworkX** solo para dibujo, **no para los algoritmos**. Los algoritmos fueron implementados manualmente, cumpliendo con el objetivo académico.

```python
if aristas_mst:
    nx.draw_networkx_edges(G, pos, edgelist=resaltadas_mst, width=4, edge_color="green")

if camino_resaltado:
    nx.draw_networkx_edges(G, pos, edgelist=edges_camino, width=4, edge_color="red")
```

---

## 7. Caso de uso práctico

- El sistema puede integrarse en una app de orientación universitaria.
- Dijkstra permite guiar a estudiantes con la ruta más corta entre edificios.
- Kruskal ofrece un **subconjunto mínimo de caminos** que conecta todo el campus con el menor costo total.

---

## 8. Conclusiones

Este proyecto traduce conceptos formales de teoría de grafos a un problema real: **movilidad dentro de un campus**. La implementación demuestra:

- Representación correcta de grafos ponderados no dirigidos.
- Uso de algoritmos clásicos (BFS, DFS, Dijkstra, Kruskal).
- Interpretación práctica de resultados (rutas, conectividad, ciclos y MST).

---

## 9. Créditos

Proyecto académico de Matemática Discreta / Teoría de Grafos.
