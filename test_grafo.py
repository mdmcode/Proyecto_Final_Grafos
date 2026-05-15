import unittest

from grafo import ARISTAS_CAMPUS_PREDEFINIDAS, NODOS_CAMPUS_PREDEFINIDOS, GrafoCampus


class TestGrafoCampus(unittest.TestCase):
    def setUp(self) -> None:
        self.grafo = GrafoCampus()

    def test_agregar_nodo_valida_entrada(self) -> None:
        with self.assertRaises(ValueError):
            self.grafo.agregar_nodo("")
        with self.assertRaises(ValueError):
            self.grafo.agregar_nodo(123)  # type: ignore[arg-type]

    def test_agregar_arista_valida_restricciones(self) -> None:
        with self.assertRaises(ValueError):
            self.grafo.agregar_arista("A", "A", 10)
        with self.assertRaises(ValueError):
            self.grafo.agregar_arista("A", "B", 0)
        with self.assertRaises(ValueError):
            self.grafo.agregar_arista("A", "B", -1)

    def test_agregar_arista_bidireccional_y_actualizable(self) -> None:
        self.grafo.agregar_arista("A", "B", 5)
        self.assertIn(("B", 5.0), self.grafo.adyacencia["A"])
        self.assertIn(("A", 5.0), self.grafo.adyacencia["B"])

        self.grafo.agregar_arista("A", "B", 8)
        self.assertEqual(self.grafo.adyacencia["A"], [("B", 8.0)])
        self.assertEqual(self.grafo.adyacencia["B"], [("A", 8.0)])

    def test_cargar_predefinido_carga_todos_los_datos(self) -> None:
        self.grafo.cargar_grafo_predefinido()
        self.assertEqual(set(self.grafo.adyacencia.keys()), set(NODOS_CAMPUS_PREDEFINIDOS))
        self.assertEqual(len(self.grafo.obtener_aristas()), len(ARISTAS_CAMPUS_PREDEFINIDAS))

    def test_matriz_adyacencia_es_simetrica(self) -> None:
        self.grafo.cargar_grafo_predefinido()
        _, matriz = self.grafo.obtener_matriz_adyacencia()
        n = len(matriz)
        for i in range(n):
            for j in range(n):
                self.assertEqual(matriz[i][j], matriz[j][i])

    def test_bfs_y_conexidad_en_grafo_simple(self) -> None:
        self.grafo.agregar_arista("A", "B", 1)
        self.grafo.agregar_arista("B", "C", 1)
        self.assertEqual(self.grafo.bfs("A"), ["A", "B", "C"])
        self.assertTrue(self.grafo.es_conexo())

    def test_es_conexo_vacio_por_convencion(self) -> None:
        self.assertTrue(self.grafo.es_conexo())

    def test_tiene_ciclos_detecta_correctamente(self) -> None:
        aciclico = GrafoCampus()
        aciclico.agregar_arista("A", "B", 1)
        aciclico.agregar_arista("B", "C", 1)
        self.assertFalse(aciclico.tiene_ciclos())

        ciclico = GrafoCampus()
        ciclico.agregar_arista("A", "B", 1)
        ciclico.agregar_arista("B", "C", 1)
        ciclico.agregar_arista("C", "A", 1)
        self.assertTrue(ciclico.tiene_ciclos())

    def test_dijkstra_predefinido_retornar_distancia_y_camino(self) -> None:
        self.grafo.cargar_grafo_predefinido()
        distancia, camino = self.grafo.dijkstra("Entrada_Principal", "Lab_Sistemas")
        self.assertEqual(distancia, 410.0)
        self.assertEqual(camino, ["Entrada_Principal", "Rectoría", "Biblioteca", "Lab_Sistemas"])

    def test_dijkstra_valida_nodos_existentes(self) -> None:
        with self.assertRaises(ValueError):
            self.grafo.dijkstra("A", "B")

    def test_dijkstra_sin_camino_retorna_infinito(self) -> None:
        self.grafo.agregar_arista("A", "B", 2)
        self.grafo.agregar_nodo("C")
        distancia, camino = self.grafo.dijkstra("A", "C")
        self.assertEqual(distancia, float("inf"))
        self.assertEqual(camino, [])

    def test_kruskal_predefinido_retorna_mst_valido(self) -> None:
        self.grafo.cargar_grafo_predefinido()
        aristas_mst, peso_total = self.grafo.kruskal_mst()
        self.assertEqual(len(aristas_mst), len(self.grafo.adyacencia) - 1)
        self.assertEqual(peso_total, 920.0)

    def test_kruskal_falla_si_el_grafo_no_es_conexo(self) -> None:
        self.grafo.agregar_arista("A", "B", 1)
        self.grafo.agregar_nodo("C")
        with self.assertRaises(ValueError):
            self.grafo.kruskal_mst()

    def test_grados_nodos_predefinido(self) -> None:
        self.grafo.cargar_grafo_predefinido()
        grados = self.grafo.grados_nodos()
        self.assertEqual(grados["Cafetería"], 4)
        self.assertEqual(grados["Entrada_Principal"], 2)


if __name__ == "__main__":
    unittest.main()
