"""
Proyecto: Sistema de Recomendación de Rutas en Red de Campus Universitario
Estructura discreta implementada: Grafo ponderado no dirigido G=(V,E,w)
Autor:
Fecha: Mayo 2026
Institución: UAO
"""

from __future__ import annotations

from typing import Iterable, Optional, Set, Tuple

import matplotlib.pyplot as plt
import networkx as nx

from grafo import GrafoCampus


EdgeSimple = Tuple[str, str]


def visualizar_grafo(
    grafo: GrafoCampus,
    camino_resaltado: Optional[Iterable[str]] = None,
    aristas_mst: Optional[Iterable[Tuple[str, str, float]]] = None,
    titulo: str = "Red de Campus Universitario",
    mostrar: bool = True,
    ruta_guardado: Optional[str] = None,
) -> None:
    """Dibuja el grafo de campus con resaltado opcional de camino mínimo y MST.

    Usa `networkx` y `matplotlib` sólo para visualización; los algoritmos de grafos
    se implementan de forma manual en `grafo.py`.

    Parámetros:
        grafo: instancia de `GrafoCampus`.
        camino_resaltado: secuencia de nodos del camino mínimo (Dijkstra), color rojo.
        aristas_mst: aristas del árbol de expansión mínima (Kruskal), color verde.
        titulo: texto del título de la figura.
        mostrar: si es True abre ventana con `plt.show()`.
        ruta_guardado: si se indica, guarda la figura en la ruta dada.
    """
    G = nx.Graph()

    for nodo in grafo.adyacencia.keys():
        G.add_node(nodo)
    for u, v, w in grafo.obtener_aristas():
        G.add_edge(u, v, weight=w)

    if not G.nodes:
        raise ValueError("No hay nodos para visualizar.")

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(12, 8))

    nx.draw_networkx_nodes(G, pos, node_color="#A7D3F4", node_size=1800, edgecolors="black")
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold")

    base_edges = list(G.edges())
    nx.draw_networkx_edges(G, pos, edgelist=base_edges, width=2, edge_color="gray")

    etiquetas = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas, font_size=8)

    if aristas_mst:
        mst_edges: Set[EdgeSimple] = {
            tuple(sorted((u, v))) for u, v, _ in aristas_mst
        }
        resaltadas_mst = [edge for edge in base_edges if tuple(sorted(edge)) in mst_edges]
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=resaltadas_mst,
            width=4,
            edge_color="green",
        )

    if camino_resaltado:
        camino = list(camino_resaltado)
        if len(camino) >= 2:
            edges_camino = [(camino[i], camino[i + 1]) for i in range(len(camino) - 1)]
            nx.draw_networkx_edges(
                G,
                pos,
                edgelist=edges_camino,
                width=4,
                edge_color="red",
            )

    plt.title(titulo)
    plt.axis("off")
    plt.tight_layout()

    if ruta_guardado:
        plt.savefig(ruta_guardado, dpi=150, bbox_inches="tight")
    if mostrar:
        plt.show()
    else:
        plt.close()
