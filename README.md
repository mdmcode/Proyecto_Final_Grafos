# Manual de usuario - Sistema de Recomendación de Rutas en Campus Universitario

Este proyecto modela una red de edificios y caminos dentro de un campus universitario mediante un **grafo ponderado no dirigido**. Desde una aplicación de consola, el usuario puede cargar un mapa base del campus, agregar nodos y aristas, consultar representaciones del grafo, calcular rutas mínimas y visualizar resultados.

## 1. Objetivo del sistema

El sistema permite:

- representar edificios como nodos;
- representar caminos como aristas con peso en metros;
- calcular la ruta más corta entre dos ubicaciones;
- verificar si toda la red está conectada;
- detectar ciclos;
- obtener un árbol de expansión mínima;
- visualizar el grafo completo y resaltar resultados.

## 2. Archivos principales

- `/home/runner/work/Proyecto_Final_-Grafos/Proyecto_Final_-Grafos/main.py`: interfaz de consola y flujo principal.
- `/home/runner/work/Proyecto_Final_-Grafos/Proyecto_Final_-Grafos/grafo.py`: estructura del grafo y algoritmos.
- `/home/runner/work/Proyecto_Final_-Grafos/Proyecto_Final_-Grafos/visualizacion.py`: dibujo del grafo con `networkx` y `matplotlib`.
- `/home/runner/work/Proyecto_Final_-Grafos/Proyecto_Final_-Grafos/requirements.txt`: dependencias necesarias.

## 3. Requisitos

Antes de ejecutar el sistema, asegúrese de tener:

- Python 3.10 o superior.
- Acceso a una terminal o consola.
- Las dependencias instaladas desde `requirements.txt`.

Dependencias incluidas:

- `networkx`
- `matplotlib`

## 4. Instalación

1. Abra una terminal dentro de la carpeta del proyecto.
2. Opcionalmente, cree y active un entorno virtual.
3. Instale las dependencias con:

```bash
pip install -r requirements.txt
```

## 5. Ejecución

Para iniciar la aplicación, ejecute:

```bash
python main.py
```

Al iniciar, el sistema mostrará un menú interactivo y solicitará una opción entre `a` y `l`.

## 6. Menú principal

El programa ofrece las siguientes opciones:

- `a) Cargar grafo predefinido`
- `b) Agregar nodo (edificio)`
- `c) Agregar arista (camino) con peso`
- `d) Mostrar matriz de adyacencia`
- `e) Mostrar lista de adyacencia`
- `f) Ejecutar Dijkstra`
- `g) Verificar si el grafo es conexo (BFS)`
- `h) Detectar ciclos (DFS)`
- `i) Calcular Árbol de Expansión Mínima (Kruskal)`
- `j) Mostrar grado de cada nodo`
- `k) Visualizar grafo`
- `l) Salir`

## 7. Guía de uso

### 7.1 Cargar el grafo predefinido

Seleccione la opción `a` para cargar automáticamente una red de ejemplo del campus. Esta opción es recomendable antes de probar los algoritmos, ya que crea una red con nodos y caminos listos para consultar.

### 7.2 Agregar un edificio

Seleccione `b`.

El sistema solicitará:

- `Nombre del nuevo edificio`

Si el nombre es válido, el nodo se agregará al grafo.

### 7.3 Agregar un camino entre edificios

Seleccione `c`.

El sistema solicitará:

- `Nodo 1`
- `Nodo 2`
- `Distancia (metros)`

Use esta opción para crear o actualizar conexiones entre edificios.

### 7.4 Mostrar la matriz de adyacencia

Seleccione `d`.

El sistema imprimirá una tabla donde cada fila y columna representa un edificio, y cada valor indica la distancia entre nodos conectados. Un valor `0` indica ausencia de conexión directa.

### 7.5 Mostrar la lista de adyacencia

Seleccione `e`.

Se mostrará cada nodo junto con sus vecinos y el peso de la arista correspondiente.

### 7.6 Calcular la ruta mínima

Seleccione `f`.

El sistema solicitará:

- `Nodo origen`
- `Nodo destino`

Luego mostrará:

- la distancia mínima total en metros;
- el camino encontrado, en orden desde el origen hasta el destino.

Después, preguntará si desea visualizar el camino en color rojo.

### 7.7 Verificar conexidad

Seleccione `g`.

El sistema indicará si todos los edificios del grafo pueden alcanzarse entre sí.

### 7.8 Detectar ciclos

Seleccione `h`.

El sistema informará si existen recorridos cerrados dentro del grafo.

### 7.9 Calcular el árbol de expansión mínima

Seleccione `i`.

El sistema mostrará:

- las aristas seleccionadas para el árbol;
- el peso total del árbol de expansión mínima.

Después, preguntará si desea visualizar el MST en color verde.

### 7.10 Mostrar el grado de cada nodo

Seleccione `j`.

Se imprimirá el número de conexiones de cada edificio.

### 7.11 Visualizar el grafo

Seleccione `k`.

Se abrirá una ventana con la representación gráfica del campus. En la visualización:

- los nodos representan edificios;
- las aristas representan caminos;
- las etiquetas sobre las aristas indican la distancia;
- el camino mínimo puede resaltarse en rojo;
- el árbol de expansión mínima puede resaltarse en verde.

### 7.12 Salir del programa

Seleccione `l` para cerrar la aplicación.

## 8. Datos precargados del campus

Al usar la opción `a`, el sistema carga los siguientes nodos:

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

También carga estas conexiones iniciales:

- Entrada_Principal -- Rectoría (120)
- Entrada_Principal -- Parqueadero (80)
- Rectoría -- Biblioteca (200)
- Rectoría -- Auditorio (150)
- Biblioteca -- Lab_Sistemas (90)
- Biblioteca -- Cafetería (110)
- Lab_Sistemas -- Facultad_Ing (60)
- Facultad_Ing -- Cafetería (140)
- Facultad_Ing -- Bienestar (170)
- Auditorio -- Deportes (130)
- Deportes -- Bienestar (95)
- Bienestar -- Cafetería (85)
- Parqueadero -- Deportes (200)
- Cafetería -- Auditorio (160)
- Lab_Sistemas -- Bienestar (210)

## 9. Ejemplo de uso rápido

1. Ejecute `python main.py`.
2. Ingrese `a` para cargar el grafo predefinido.
3. Ingrese `f` para calcular una ruta mínima.
4. Escriba como origen `Entrada_Principal`.
5. Escriba como destino `Lab_Sistemas`.
6. Revise la distancia y el camino resultante.
7. Si desea, responda `s` para visualizar el recorrido resaltado.

## 10. Recomendaciones de uso

- Cargue primero el grafo predefinido si desea probar el sistema rápidamente.
- Escriba los nombres de nodos exactamente como fueron creados.
- Ingrese distancias positivas al agregar aristas.
- Si desea resultados visuales, asegúrese de tener un entorno con soporte gráfico para `matplotlib`.

## 11. Posibles errores y su significado

El sistema puede mostrar mensajes como los siguientes:

- **"El nodo 'X' no existe en el grafo."**: el nombre ingresado no está registrado.
- **"El peso debe ser un número positivo."**: se intentó crear una arista con valor inválido.
- **"No se permiten lazos"**: se intentó conectar un nodo consigo mismo.
- **"No hay nodos para visualizar."**: se intentó abrir la visualización sin datos cargados.
- **"El grafo no es conexo"**: no es posible construir un MST que abarque todos los nodos.

## 12. Tecnologías utilizadas

- Python
- `networkx`
- `matplotlib`

## 13. Resumen

Este sistema sirve como apoyo académico para aplicar conceptos de matemática discreta y teoría de grafos en un caso práctico: la recomendación de rutas dentro de un campus universitario.
