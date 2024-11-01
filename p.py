import numpy as np
import graphviz
from collections import deque

# Definir el laberinto y posiciones de entrada/salida
columnas, filas = 15, 15
mapa = np.array([
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
])
pos_x, pos_y = 0, 0
salida_x, salida_y = 11, 5

# Configuración del gráfico de Graphviz
grafo = graphviz.Digraph('G', filename='laberinto_dfs', format='svg')

grafo.attr(size='15,15')

# Función de DFS con visualización de árbol de búsqueda
def dfs(x, y, camino):
    # Si está fuera de los límites o es una pared, regresamos
    if x < 0 or x >= filas or y < 0 or y >= columnas or mapa[x][y] == 1:
        return False

    # Si encontramos la salida, registramos el camino
    if (x, y) == (salida_x, salida_y):
        grafo.node(str((x, y)), shape='doublecircle', color='green', label=f"Salida: ({x}, {y})")
        grafo.edge(camino[-1], str((x, y)))
        return True

    # Marcar la celda como visitada
    mapa[x][y] = 1
    grafo.node(str((x, y)), label=f"({x}, {y})")
    if camino:
        grafo.edge(camino[-1], str((x, y)))

    # Guardar el camino actual y explorar en direcciones: derecha, abajo, izquierda, arriba
    camino.append(str((x, y)))
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        if dfs(x + dx, y + dy, camino):
            return True  # Si se encuentra la salida, no se necesita seguir buscando

    # Si no encuentra la salida, deshacer el camino y continuar con otro
    camino.pop()
    return False

# Funcion de Amplitud con visualización de árbol de búsqueda

def amplitud(x, y, camino):
    # La característica de amplitud es que debe ir extendiendo los nodos hijos hasta que todos los nodos hijos estén completos, para después pasar con los nodos hijos de los hijos
    queue = deque([(x, y, [])])
    visitados = set()

    while queue:
        x, y, camino = queue.popleft()

        # Si está fuera de los límites o es una pared, continuamos con el siguiente nodo
        if x < 0 or x >= filas or y < 0 or y >= columnas or mapa[x][y] == 1:
            continue

        # Si encontramos la salida, registramos el camino
        if (x, y) == (salida_x, salida_y):
            grafo.node(str((x, y)), shape='doublecircle', color='green', label=f"Salida: ({x}, {y})")
            if camino:
                grafo.edge(camino[-1], str((x, y)))
            return True

        # Marcar la celda como visitada
        mapa[x][y] = 1
        grafo.node(str((x, y)), label=f"({x}, {y})")
        if camino:
            grafo.edge(camino[-1], str((x, y)))

        # Guardar el camino actual y explorar en direcciones: derecha, abajo, izquierda, arriba
        nuevo_camino = camino + [str((x, y))]
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in visitados:
                visitados.add((nx, ny))
                queue.append((nx, ny, nuevo_camino))

    return False
def costos(x, y, camino, costo=0):
    # El algoritmo por costos, va tomando un acumulado del costo necesario para ir desde el inicio hasta la meta, y va tomando el camino con menor costo hasta llegar a la meta.
    
    # La idea es que se expanda el árbol hasta encontrar la meta con menor costo
    
    # Cada movimiento tiene un costo de 1
    queue = deque([(x, y, [], 0)])
    visitados = set()
    
    while queue:
        x, y, camino, costo = queue.popleft()
        
        # Si está fuera de los límites o es una pared, continuamos con el siguiente nodo
        if x < 0 or x >= filas or y < 0 or y >= columnas or mapa[x][y] == 1:
            continue
        
        # Si encontramos la salida, registramos el camino
        if (x, y) == (salida_x, salida_y):
            grafo.node(str((x, y)), shape='doublecircle', color='green', label=f"Salida: ({x}, {y})\nCosto total: {costo}")
            if camino:
                grafo.edge(camino[-1], str((x, y)), label=f"Costo: {costo}")
            return True
        
        # Marcar la celda como visitada
        mapa[x][y] = 1
        grafo.node(str((x, y)), label=f"({x}, {y})\nCosto: {1}")
        if camino:
            grafo.edge(camino[-1], str((x, y)), label=f"Costo: {costo}")
        
        # Guardar el camino actual y explorar en direcciones: derecha, abajo, izquierda, arriba
        nuevo_camino = camino + [str((x, y))]
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in visitados:
                visitados.add((nx, ny))
                queue.append((nx, ny, nuevo_camino, costo + 1))
        
    return False


    

    
# Ejecutar DFS desde la posición inicial
# amplitud(pos_x, pos_y, [])
# dfs(pos_x, pos_y, [])
costos(pos_x, pos_y, [])


# Generar el gráfico y mostrar
grafo.view()
