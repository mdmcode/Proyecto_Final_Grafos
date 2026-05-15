# Sistema de Recomendación de Rutas en una Red de Campus Universitario

Aplicación de **Matemática Discreta** (Ingeniería Informática, UAO) que modela el campus como un **grafo ponderado no dirigido** \(G=(V,E,w)\), donde:

- \(V\): edificios del campus.
- \(E\): caminos entre edificios.
- \(w:E \to \mathbb{R}^+\): distancia en metros.

El sistema permite calcular rutas mínimas, verificar conectividad, detectar ciclos, obtener un árbol de expansión mínima y visualizar el grafo.

## Estructura de archivos

- `/home/runner/work/Proyecto_Final_-Grafos/Proyecto_Final_-Grafos/grafo.py`: clase `GrafoCampus` y algoritmos (Dijkstra, BFS, DFS, Kruskal, grados).
- `/home/runner/work/Proyecto_Final_-Grafos/Proyecto_Final_-Grafos/main.py`: interfaz interactiva de consola.
- `/home/runner/work/Proyecto_Final_-Grafos/Proyecto_Final_-Grafos/visualizacion.py`: visualización con `networkx` + `matplotlib`.
- `/home/runner/work/Proyecto_Final_-Grafos/Proyecto_Final_-Grafos/requirements.txt`: dependencias.

## Requisitos

- Python **3.10+**
- Dependencias:
  - `networkx`
  - `matplotlib`

## Instalación

1. Abrir terminal en la carpeta del proyecto.
2. (Opcional) crear y activar entorno virtual.
3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

## Menú disponible

a) Cargar grafo predefinido (10 nodos, 15 aristas)  
b) Agregar nodo  
c) Agregar arista con peso  
d) Mostrar matriz de adyacencia  
e) Mostrar lista de adyacencia  
f) Ejecutar Dijkstra  
g) Verificar conexidad (BFS)  
h) Detectar ciclos (DFS)  
i) Calcular Árbol de Expansión Mínima (Kruskal)  
j) Mostrar grado de cada nodo  
k) Visualizar grafo (pesos, nodos y resaltados)  
l) Salir

## Datos de prueba precargados

Nodos:

- Biblioteca
- Cafetería
- Lab_Sistemas
- Auditorio
- Rectoría
- Deportes
- Entrada_Principal
- Facultad_Ing
- Bienestar
- Parqueadero

Aristas (u, v, peso):

- (Entrada_Principal, Rectoría, 120)
- (Entrada_Principal, Parqueadero, 80)
- (Rectoría, Biblioteca, 200)
- (Rectoría, Auditorio, 150)
- (Biblioteca, Lab_Sistemas, 90)
- (Biblioteca, Cafetería, 110)
- (Lab_Sistemas, Facultad_Ing, 60)
- (Facultad_Ing, Cafetería, 140)
- (Facultad_Ing, Bienestar, 170)
- (Auditorio, Deportes, 130)
- (Deportes, Bienestar, 95)
- (Bienestar, Cafetería, 85)
- (Parqueadero, Deportes, 200)
- (Cafetería, Auditorio, 160)
- (Lab_Sistemas, Bienestar, 210)

## Ejemplo de uso esperado

1. Elegir `a` para cargar grafo predefinido.
2. Elegir `f` y escribir:
   - Origen: `Entrada_Principal`
   - Destino: `Lab_Sistemas`
3. Salida esperada (puede variar en formato):
   - Distancia mínima: `410 metros`
   - Camino: `Entrada_Principal -> Rectoría -> Biblioteca -> Lab_Sistemas`
4. Elegir `i` para obtener el MST y su peso total.
5. Elegir `k` para visualizar el grafo.

## Especificaciones técnicas

- **Representaciones:** lista de adyacencia y matriz de adyacencia.
- **Algoritmos implementados manualmente:**
  - Dijkstra: \(O((V+E)\log V)\) con `heapq`.
  - BFS (conectividad): \(O(V+E)\).
  - DFS (ciclos): \(O(V+E)\).
  - Kruskal (MST): \(O(E\log E)\).
- **Visualización:** `networkx` y `matplotlib`.
- **Manejo de errores:** validación de nodos, pesos y estado del grafo mediante excepciones y mensajes en consola.

## Contexto de ingeniería

Este sistema puede integrarse en una app móvil de orientación universitaria para recomendar rutas entre edificios a estudiantes nuevos, personal administrativo y visitantes.
