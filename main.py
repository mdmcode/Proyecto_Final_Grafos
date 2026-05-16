"""
Proyecto: Sistema de Recomendación de Rutas en Red de Campus Universitario
Estructura discreta implementada: Grafo ponderado no dirigido G=(V,E,w)
Autor:
Fecha: Mayo 2026
Institución: UAO
"""

from __future__ import annotations

import argparse
from typing import Callable

from grafo import GrafoCampus
from gui import iniciar_gui
from visualizacion import visualizar_grafo


def imprimir_menu() -> None:
    """Muestra el menú principal del sistema de recomendación de rutas."""
    print("\n=== MENÚ PRINCIPAL: SISTEMA DE RUTAS CAMPUS ===")
    print("a) Cargar grafo predefinido")
    print("b) Agregar nodo (edificio)")
    print("c) Agregar arista (camino) con peso")
    print("d) Mostrar matriz de adyacencia")
    print("e) Mostrar lista de adyacencia")
    print("f) Ejecutar Dijkstra")
    print("g) Verificar si el grafo es conexo (BFS)")
    print("h) Detectar ciclos (DFS)")
    print("i) Calcular Árbol de Expansión Mínima (Kruskal)")
    print("j) Mostrar grado de cada nodo")
    print("k) Visualizar grafo")
    print("l) Salir")


def mostrar_matriz(grafo: GrafoCampus) -> None:
    """Imprime la matriz de adyacencia en formato tabular."""
    nodos, matriz = grafo.obtener_matriz_adyacencia()
    if not nodos:
        print("No hay nodos en el grafo.")
        return

    print("\nMatriz de adyacencia (pesos en metros):")
    print(" " * 20 + " ".join(f"{n[:12]:>12}" for n in nodos))
    for i, nodo in enumerate(nodos):
        fila = " ".join(f"{matriz[i][j]:>12.0f}" for j in range(len(nodos)))
        print(f"{nodo[:18]:>18} {fila}")


def mostrar_lista(grafo: GrafoCampus) -> None:
    """Imprime la lista de adyacencia del grafo."""
    lista = grafo.obtener_lista_adyacencia()
    if not lista:
        print("No hay nodos en el grafo.")
        return

    print("\nLista de adyacencia:")
    for nodo in sorted(lista):
        vecinos = ", ".join(f"({v}, {w:.0f}m)" for v, w in lista[nodo])
        print(f"- {nodo}: {vecinos if vecinos else 'Sin conexiones'}")


def ejecutar_dijkstra(grafo: GrafoCampus) -> None:
    """Solicita origen/destino y ejecuta Dijkstra con manejo de errores."""
    origen = input("Nodo origen: ").strip()
    destino = input("Nodo destino: ").strip()
    distancia, camino = grafo.dijkstra(origen, destino)

    if distancia == float("inf"):
        print("No existe ruta entre los nodos seleccionados.")
        return

    print(f"Distancia mínima: {distancia:.0f} metros")
    print("Camino: " + " -> ".join(camino))

    visualizar = input("¿Desea visualizar el camino en rojo? (s/n): ").strip().lower()
    if visualizar == "s":
        visualizar_grafo(
            grafo,
            camino_resaltado=camino,
            titulo=f"Camino más corto: {origen} -> {destino}",
        )


def verificar_conexidad(grafo: GrafoCampus) -> None:
    """Ejecuta BFS para validar conectividad global de la red."""
    if grafo.es_conexo():
        print("El grafo es conexo: todos los edificios son alcanzables.")
    else:
        print("El grafo NO es conexo: existen edificios aislados o componentes separadas.")


def detectar_ciclos(grafo: GrafoCampus) -> None:
    """Ejecuta DFS para detectar ciclos en la red."""
    if grafo.tiene_ciclos():
        print("Se detectaron ciclos en el grafo.")
    else:
        print("No se detectaron ciclos en el grafo.")


def calcular_mst(grafo: GrafoCampus) -> None:
    """Calcula MST con Kruskal y permite visualización en verde."""
    aristas_mst, peso_total = grafo.kruskal_mst()
    print("Aristas del Árbol de Expansión Mínima:")
    for u, v, w in aristas_mst:
        print(f"- {u} -- {v}: {w:.0f}m")
    print(f"Peso total del MST: {peso_total:.0f}m")

    visualizar = input("¿Desea visualizar el MST en verde? (s/n): ").strip().lower()
    if visualizar == "s":
        visualizar_grafo(
            grafo,
            aristas_mst=aristas_mst,
            titulo="Árbol de Expansión Mínima (Kruskal)",
        )


def mostrar_grados(grafo: GrafoCampus) -> None:
    """Imprime el grado de cada vértice del grafo."""
    grados = grafo.grados_nodos()
    if not grados:
        print("No hay nodos en el grafo.")
        return

    print("Grado de cada nodo:")
    for nodo in sorted(grados):
        print(f"- grado({nodo}) = {grados[nodo]}")


def agregar_nodo_interactivo(grafo: GrafoCampus) -> None:
    """Agrega un nodo leyendo el nombre desde consola."""
    nombre = input("Nombre del nuevo edificio: ").strip()
    grafo.agregar_nodo(nombre)
    print(f"Nodo '{nombre}' agregado correctamente.")


def agregar_arista_interactiva(grafo: GrafoCampus) -> None:
    """Agrega una arista ponderada leyendo nodos y distancia desde consola."""
    nodo1 = input("Nodo 1: ").strip()
    nodo2 = input("Nodo 2: ").strip()
    peso_str = input("Distancia (metros): ").strip()
    peso = float(peso_str)
    grafo.agregar_arista(nodo1, nodo2, peso)
    print(f"Arista {nodo1} -- {nodo2} ({peso:.0f}m) agregada correctamente.")


def iniciar_aplicacion() -> None:
    """Inicia el menú interactivo del sistema y procesa entradas de usuario."""
    grafo = GrafoCampus()

    acciones: dict[str, Callable[[], None]] = {
        "a": lambda: (grafo.cargar_grafo_predefinido(), print("Grafo predefinido cargado.")),
        "b": lambda: agregar_nodo_interactivo(grafo),
        "c": lambda: agregar_arista_interactiva(grafo),
        "d": lambda: mostrar_matriz(grafo),
        "e": lambda: mostrar_lista(grafo),
        "f": lambda: ejecutar_dijkstra(grafo),
        "g": lambda: verificar_conexidad(grafo),
        "h": lambda: detectar_ciclos(grafo),
        "i": lambda: calcular_mst(grafo),
        "j": lambda: mostrar_grados(grafo),
        "k": lambda: visualizar_grafo(grafo),
    }

    while True:
        imprimir_menu()
        opcion = input("Seleccione una opción (a-l): ").strip().lower()

        if opcion == "l":
            print("Saliendo del sistema. ¡Éxitos en tu proyecto de Matemática Discreta!")
            break

        accion = acciones.get(opcion)
        if accion is None:
            print("Opción inválida. Intente nuevamente.")
            continue

        try:
            accion()
        except ValueError as error:
            print(f"Error de validación: {error}")
        except Exception as error:  # noqa: BLE001
            print(f"Error inesperado: {error}")


def parsear_argumentos() -> argparse.Namespace:
    """Parsea argumentos de ejecución."""
    parser = argparse.ArgumentParser(
        description="Sistema de recomendación de rutas en campus universitario.",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Inicia la versión gráfica (Tkinter).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    argumentos = parsear_argumentos()
    if argumentos.gui:
        iniciar_gui()
    else:
        iniciar_aplicacion()
