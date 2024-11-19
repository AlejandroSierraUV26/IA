import numpy as np
import pydot 
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time 
import matplotlib.animation as animation
import time 
from graphviz import Graph
from collections import deque
from networkx.drawing.nx_pydot import graphviz_layout
import heapq


def construir_arbol(inicio, mapa):
    arbol = {}
    filas, columnas = mapa.shape
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, Abajo, Izquierda, Derecha
    frontera = [(inicio, [])]
    
    visitados = set()
    while frontera:
        nodo, camino = frontera.pop(0)
        arbol[nodo] = []
        visitados.add(nodo)
        
        for dx, dy in movimientos:
            x, y = nodo[0] + dx, nodo[1] + dy
            if x < 0 or x >= filas or y < 0 or y >= columnas or mapa[x, y] == 1:
                continue
            if (x, y) in visitados:
                continue
            frontera.append(((x, y), camino + [(x, y)]))
            arbol[nodo].append(((x, y), (dx, dy)))
        
    return arbol

def imprimir_arbol(arbol):
    for nodo in arbol:
        print(nodo, arbol[nodo])
def dibujar_arbol(arbol, camino, inicio, final):
    T = nx.DiGraph()  # Crea el grafo dirigido

    # Construir el grafo
    for nodo in arbol:
        T.add_node(str(nodo))
        for hijo, _ in arbol[nodo]:
            T.add_edge(str(nodo), str(hijo))

    pos = graphviz_layout(T, prog="dot")
    
    # Activar modo interactivo
    plt.ion()
    fig, ax = plt.subplots()
    camino = list(camino)
    camino.sort()
    # Inicializar los colores de los nodos
    node_colors_dict = {node: 'blue' for node in T.nodes()}
    node_colors_dict[str(inicio)] = 'yellow'
    node_colors_dict[str(final)] = 'green'
    # Dibujar el árbol inicial
    for nodo_actual in camino:
        # Actualizar el color del nodo actual
        node_colors_dict[str(nodo_actual)] = 'red'

        # Construir la lista de colores para el grafo
        node_colors = [node_colors_dict[node] for node in T.nodes()]

        # Dibujar el grafo
        ax.clear()  # Limpiar el gráfico anterior
        nx.draw(T, pos, with_labels=True, node_size=500, node_color=node_colors, ax=ax, arrowsize=20, font_size=10, font_color='white', font_weight='bold', edge_color='black', width=2, edgecolors='black', linewidths=1.5, alpha=0.7, connectionstyle='arc3, rad = 0.1', style='dashed', edge_cmap=plt.cm.Blues, edge_vmin=0, edge_vmax=1)
        plt.pause(1)  # Pausa para visualizar el cambio

    # Desactivar modo interactivo
    plt.ioff()
    plt.show()
def main():
    mapa, inicio, final = leer_mapa("lab_matrix.txt")

    arbol_generado = construir_arbol(inicio, mapa)
    print("Arbol generado")
    print(arbol_generado)
    print()
    n = leer_n()
    sin_salida = set()
    camino_recodido = [inicio]
    for i in range(30):
        algoritmo_aleatorio = np.random.choice([limitada,  iterativa,profundidad, amplitud, costo, avara])  
        print(algoritmo_aleatorio.__name__)
        camino, visitados, sin_salida = algoritmo_aleatorio(camino_recodido[-1], final, arbol_generado, n, sin_salida)
        visitados = list(dict.fromkeys(camino_recodido + list(visitados)))
        sin_salida = sin_salida.union(set(sin_salida))
        camino_recodido = leer_camino_recorrido()
        if len(camino_recodido) == 1:
            print("No hay camino")
            print("Quedo en el nodo", camino_recodido[-1])
            break             
        if camino[-1] == final:
            # Pintar el nodo final
            break
        
        
    print(visitados)
    
    dibujar_arbol(arbol_generado, visitados, inicio, final)
    

    with open("camino.txt", "w") as f:
        f.write("")
         


def profundidad(inicio, final, arbol, n, sin_salida, camino_previo=None ):
    # Sombrear el camino de inicio a final, que toma profundidad a partir del arbol
    # Prioridad : Derecha, Abajo, Izquierda, Arriba
    visitados = set(camino_previo) if camino_previo else set()
    stack = [(inicio, camino_previo + [inicio] if camino_previo else [inicio])]
    i = 0
    while stack:
        if i == n:
            break
        nodo, camino = stack.pop()
        if nodo in sin_salida:
            continue
        if nodo == final:
            
            return camino, visitados, sin_salida
        if nodo not in visitados:
            visitados.add(nodo)
            guardar_camino(nodo)
            moved = False
            for hijo, _ in arbol.get(nodo, []):
                if hijo not in visitados and hijo not in sin_salida:
                    stack.append((hijo, camino + [hijo]))
                    moved = True
            if not moved:
                sin_salida.add(nodo)
                if camino:
                    camino.pop()
        i += 1
    return camino, visitados, sin_salida
def amplitud(inicio, final, arbol, altura_max, sin_salida):
    # Sombrear el camino de inicio a final, que toma amplitud apartir del arbol
    # Prioridad : Derecha, Abajo, Izquierda, Arriba
        visitados = set()
        queue = deque([(inicio, [inicio])])
        i = 0
        while queue:
            if i == altura_max:
                break
            
            nodo, camino = queue.popleft()
            if nodo == final:
                
                return camino, visitados, sin_salida
            if nodo in sin_salida:
                continue
            if nodo not in visitados:
                visitados.add(nodo)
                guardar_camino(nodo)
                
                moved = False
                for hijo, _ in arbol.get(nodo, []):
                    if hijo not in visitados and hijo not in sin_salida:
                        queue.append((hijo, camino + [hijo]))
                        moved = True
                        
                if not moved:
                    sin_salida.add(nodo)
            i += 1
        return camino, visitados, sin_salida
def costo(inicio, final, arbol, n, sin_salida):
    # Sombrear el camino de inicio a final, que toma costo apartir del arbol
    # Prioridad : Derecha, Abajo, Izquierda, Arriba
    visitados = set()
    queue = [(0, inicio, [inicio])]  # (costo, nodo, camino)
    i = 0
    while queue:
        if i == n:
            break
        queue.sort()  # Ordenar la cola por costo
        costo, nodo, camino = queue.pop(0)
        if nodo == final:
            
            return camino, visitados, sin_salida
        if nodo not in visitados:
            visitados.add(nodo)
            guardar_camino(nodo)
            moved = False
            for hijo, _ in arbol.get(nodo, []):
                if hijo not in visitados:
                    queue.append((costo + 1, hijo, camino + [hijo]))
                    moved = True
                    
        i += 1
    return camino, visitados, sin_salida
def limitada(inicio, final, arbol, alt_max, sin_salida):
    # Sombrear el camino de inicio a final, que toma limitada apartir del arbol
    # Prioridad : Derecha, Abajo, Izquierda, Arriba
    visitados = set()
    stack = [(inicio, [inicio], 0)]
    
    while stack:
        nodo, camino, profundidad = stack.pop()
        if nodo == final:
            
            return camino, visitados, sin_salida
        if nodo in sin_salida:
            continue
        if nodo not in visitados:
            visitados.add(nodo)
            guardar_camino(nodo)
            moved = False
            if profundidad < alt_max:
                for hijo, _ in arbol.get(nodo, []):
                    if hijo not in visitados:
                        stack.append((hijo, camino + [hijo], profundidad + 1))
                        moved = True
                    
    return camino, visitados, sin_salida
def iterativa(inicio, final, arbol, alt_max, sin_salida):
    visitados = set()
    for i in range(alt_max):
        stack = [(inicio, [inicio], 0)]
        
        while stack:
            nodo, camino, profundidad = stack.pop()
            if nodo == final:
                
                return camino, visitados, sin_salida
            if nodo in sin_salida:
                continue
            if nodo not in visitados:
                visitados.add(nodo)
                guardar_camino(nodo)
                moved = False
                if profundidad < alt_max:
                    for hijo, _ in arbol.get(nodo, []):
                        if hijo not in visitados :
                            stack.append((hijo, camino + [hijo], profundidad + 1))
                            moved = True

    return camino, visitados, sin_salida          
def avara(inicio, final, arbol, n, sin_salida):
    # Sombrear el camino de inicio a final, que toma avara apartir del arbol
    # Prioridad : Derecha, Abajo, Izquierda, Arriba
    # Definir la heurística de la distancia de Manhattan
    dm = lambda x, y: abs(x - final[0]) + abs(y - final[1])
    visitados = set()
    queue = [(dm(inicio[0], inicio[1]), inicio, [inicio])]
    i = 0
    while queue:
        if i == n:
            break
        _, nodo, camino = heapq.heappop(queue)

        """Pop the smallest item off the heap, maintaining the heap invariant."""
        if nodo == final:
            
            return camino, visitados, sin_salida
        if nodo in sin_salida:
            continue
        if nodo not in visitados:
            visitados.add(nodo)
            guardar_camino(nodo)
            moved = False
            for hijo, _ in arbol.get(nodo, []):
                if hijo not in visitados and hijo not in sin_salida:
                    heapq.heappush(queue, (dm(hijo[0], hijo[1]), hijo, camino + [hijo]))
                    """Push item onto heap, maintaining the heap invariant."""
                    moved = True
                    
        if not moved:
            sin_salida.add(nodo)

                    
        i += 1
    return list(visitados),set(camino), sin_salida
def guardar_camino(nodo):
    with open("camino.txt", "a") as f:
        f.write(f"{nodo}\n")

def leer_camino_recorrido():
    with open("camino.txt", "r") as f:
        f = f.read().splitlines()
        elem = []
        for linea in f:
            elem.append(eval(linea))
        
        
            
    return elem
def leer_mapa(ruta):
    with open(ruta, "r") as f:
        mapa = []
        f = f.read().splitlines()
        for elem in f: 
            elem = elem.split()
            elem = list(map(int, elem))
            mapa.append(elem)
        inicio = ()
        final = ()
        for i in range(len(mapa)):
            for j in range(len(mapa[i])):
                if mapa[i][j] == 2:
                    inicio = (i, j)
                if mapa[i][j] == 3:
                    final = (i, j)
                    
                
    return np.array(mapa), inicio, final
def leer_n():
    with open("valor.txt", "r") as f:
        n = f.read()
    return int(n)

T = nx.DiGraph()
main()



