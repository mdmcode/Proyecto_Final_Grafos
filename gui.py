"""
Interfaz gráfica para el Sistema de Recomendación de Rutas en Campus Universitario.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkinter.scrolledtext import ScrolledText

from grafo import GrafoCampus
from visualizacion import visualizar_grafo


class AplicacionGrafoGUI:
    """Aplicación GUI para interactuar con el grafo del campus."""

    def __init__(self, raiz: tk.Tk) -> None:
        self.raiz = raiz
        self.raiz.title("Sistema de Rutas Campus - GUI")
        self.raiz.geometry("900x650")

        self.grafo = GrafoCampus()
        self._construir_interfaz()

    def _construir_interfaz(self) -> None:
        marco_botones = ttk.Frame(self.raiz, padding=10)
        marco_botones.pack(fill="x")

        botones = [
            ("Cargar grafo predefinido", self.cargar_predefinido),
            ("Agregar nodo", self.agregar_nodo),
            ("Agregar arista", self.agregar_arista),
            ("Mostrar matriz", self.mostrar_matriz),
            ("Mostrar lista", self.mostrar_lista),
            ("Ejecutar Dijkstra", self.ejecutar_dijkstra),
            ("Verificar conexidad", self.verificar_conexidad),
            ("Detectar ciclos", self.detectar_ciclos),
            ("Calcular MST", self.calcular_mst),
            ("Mostrar grados", self.mostrar_grados),
            ("Visualizar grafo", self.visualizar),
            ("Limpiar salida", self.limpiar_salida),
        ]

        for i, (texto, comando) in enumerate(botones):
            ttk.Button(marco_botones, text=texto, command=comando).grid(
                row=i // 3,
                column=i % 3,
                padx=5,
                pady=5,
                sticky="ew",
            )

        for col in range(3):
            marco_botones.columnconfigure(col, weight=1)

        self.salida = ScrolledText(self.raiz, wrap="word", font=("Consolas", 10))
        self.salida.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self._escribir("GUI iniciada. Use los botones para interactuar con el sistema.")

    def _escribir(self, texto: str) -> None:
        self.salida.insert("end", texto + "\n")
        self.salida.see("end")

    def limpiar_salida(self) -> None:
        self.salida.delete("1.0", "end")

    def cargar_predefinido(self) -> None:
        self.grafo.cargar_grafo_predefinido()
        self._escribir("Grafo predefinido cargado correctamente.")

    def agregar_nodo(self) -> None:
        nombre = simpledialog.askstring("Agregar nodo", "Nombre del nuevo edificio:")
        if nombre is None:
            return
        try:
            self.grafo.agregar_nodo(nombre.strip())
            self._escribir(f"Nodo '{nombre.strip()}' agregado correctamente.")
        except ValueError as error:
            messagebox.showerror("Error de validación", str(error))

    def agregar_arista(self) -> None:
        nodo1 = simpledialog.askstring("Agregar arista", "Nodo 1:")
        if nodo1 is None:
            return
        nodo2 = simpledialog.askstring("Agregar arista", "Nodo 2:")
        if nodo2 is None:
            return
        peso = simpledialog.askfloat("Agregar arista", "Distancia (metros):")
        if peso is None:
            return
        try:
            self.grafo.agregar_arista(nodo1.strip(), nodo2.strip(), float(peso))
            self._escribir(f"Arista {nodo1.strip()} -- {nodo2.strip()} ({peso:.0f}m) agregada.")
        except ValueError as error:
            messagebox.showerror("Error de validación", str(error))

    def mostrar_matriz(self) -> None:
        nodos, matriz = self.grafo.obtener_matriz_adyacencia()
        if not nodos:
            self._escribir("No hay nodos en el grafo.")
            return
        self._escribir("\nMatriz de adyacencia (pesos en metros):")
        self._escribir(" " * 20 + " ".join(f"{n[:12]:>12}" for n in nodos))
        for i, nodo in enumerate(nodos):
            fila = " ".join(f"{matriz[i][j]:>12.0f}" for j in range(len(nodos)))
            self._escribir(f"{nodo[:18]:>18} {fila}")

    def mostrar_lista(self) -> None:
        lista = self.grafo.obtener_lista_adyacencia()
        if not lista:
            self._escribir("No hay nodos en el grafo.")
            return
        self._escribir("\nLista de adyacencia:")
        for nodo in sorted(lista):
            vecinos = ", ".join(f"({v}, {w:.0f}m)" for v, w in lista[nodo])
            self._escribir(f"- {nodo}: {vecinos if vecinos else 'Sin conexiones'}")

    def ejecutar_dijkstra(self) -> None:
        origen = simpledialog.askstring("Dijkstra", "Nodo origen:")
        if origen is None:
            return
        destino = simpledialog.askstring("Dijkstra", "Nodo destino:")
        if destino is None:
            return
        try:
            distancia, camino = self.grafo.dijkstra(origen.strip(), destino.strip())
        except ValueError as error:
            messagebox.showerror("Error de validación", str(error))
            return

        if distancia == float("inf"):
            self._escribir("No existe ruta entre los nodos seleccionados.")
            return

        self._escribir(f"Distancia mínima: {distancia:.0f} metros")
        self._escribir("Camino: " + " -> ".join(camino))

        if messagebox.askyesno("Visualización", "¿Desea visualizar el camino en rojo?"):
            visualizar_grafo(
                self.grafo,
                camino_resaltado=camino,
                titulo=f"Camino más corto: {origen.strip()} -> {destino.strip()}",
            )

    def verificar_conexidad(self) -> None:
        if self.grafo.es_conexo():
            self._escribir("El grafo es conexo: todos los edificios son alcanzables.")
        else:
            self._escribir("El grafo NO es conexo: existen edificios aislados o componentes separadas.")

    def detectar_ciclos(self) -> None:
        if self.grafo.tiene_ciclos():
            self._escribir("Se detectaron ciclos en el grafo.")
        else:
            self._escribir("No se detectaron ciclos en el grafo.")

    def calcular_mst(self) -> None:
        try:
            aristas_mst, peso_total = self.grafo.kruskal_mst()
        except ValueError as error:
            messagebox.showerror("Error de validación", str(error))
            return

        self._escribir("Aristas del Árbol de Expansión Mínima:")
        for u, v, w in aristas_mst:
            self._escribir(f"- {u} -- {v}: {w:.0f}m")
        self._escribir(f"Peso total del MST: {peso_total:.0f}m")

        if messagebox.askyesno("Visualización", "¿Desea visualizar el MST en verde?"):
            visualizar_grafo(
                self.grafo,
                aristas_mst=aristas_mst,
                titulo="Árbol de Expansión Mínima (Kruskal)",
            )

    def mostrar_grados(self) -> None:
        grados = self.grafo.grados_nodos()
        if not grados:
            self._escribir("No hay nodos en el grafo.")
            return
        self._escribir("Grado de cada nodo:")
        for nodo in sorted(grados):
            self._escribir(f"- grado({nodo}) = {grados[nodo]}")

    def visualizar(self) -> None:
        try:
            visualizar_grafo(self.grafo)
        except ValueError as error:
            messagebox.showerror("Error de visualización", str(error))


def iniciar_gui() -> None:
    """Inicia la versión GUI de la aplicación."""
    raiz = tk.Tk()
    AplicacionGrafoGUI(raiz)
    raiz.mainloop()


__all__ = ["AplicacionGrafoGUI", "iniciar_gui"]
