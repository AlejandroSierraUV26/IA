import numpy as np
import pydot 
import networkx as nx
import matplotlib.pyplot as plt
from graphviz import Graph
from collections import deque
from networkx.drawing.nx_pydot import graphviz_layout
import heapq


def construir_arbol(inicio, mapa):
    arbol = {}
    filas, columnas = mapa.shape
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, Abajo, Izquierda, Derecha
    frontera = [(inicio, [])]
    
    while frontera:
        nodo, camino = frontera.pop(0)
        arbol[nodo] = []
        
        for dx, dy in movimientos:
            x, y = nodo[0] + dx, nodo[1] + dy
            if x < 0 or x >= filas or y < 0 or y >= columnas or mapa[x, y] == 1:
                continue
            if (x, y) in arbol:
                continue
            frontera.append(((x, y), camino + [(x, y)]))
            arbol[nodo].append(((x, y), (dx, dy)))
        
    
    
    

    return arbol
def imprimir_arbol(arbol):
    for nodo in arbol:
        print(nodo, arbol[nodo])
def dibujar_arbol(arbol, camino, inicio, final):
    
    for nodo in arbol:
        T.add_node(str(nodo))
        for hijo, _ in arbol[nodo]:
            T.add_edge(str(nodo), str(hijo))

    pos = graphviz_layout(T, prog="dot")
    node_colors = []
    for node in T.nodes():
        node_eval = eval(node)
        if node_eval == inicio:
            node_colors.append('yellow')
        elif node_eval == final:
            node_colors.append('green')
        elif node_eval in camino:
            node_colors.append('red')
        else:
            node_colors.append('blue')
    nx.draw(T, pos, with_labels=True, node_size=2000, node_color=node_colors)
    plt.show()
def main():
    mapa = np.array([
        [0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 0, 0, 1, 0]
    ])
    arbol_generado = construir_arbol((0, 0), mapa)
    # Inicia en (0, 0) y termina en (13, 13)
    inicio =(0, 0)
    final = (4, 4)
    n = 15
    sin_salida = set()
    camino_recodido = [inicio]
    for i in range(10):
        algoritmo_aleatorio = np.random.choice([profundidad, amplitud, costo, limitada, iterativa])    
        print(algoritmo_aleatorio.__name__)
        camino, visitados, sin_salida = algoritmo_aleatorio(camino_recodido[-1], final, arbol_generado, n, sin_salida)
        visitados = visitados.union(set(camino_recodido))
        sin_salida = sin_salida.union(set(sin_salida))
        camino_recodido = leer_camino_recorrido()
        if len(camino_recodido) == 1:
            print("No hay camino")
            print("Quedo en el nodo", camino_recodido[-1])
            break                
        if camino[-1] == final:
            # Pintar el nodo final
            break
        
        

    
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
                    if hijo not in visitados and hijo not in sin_salida:
                        stack.append((hijo, camino + [hijo], profundidad + 1))
                        moved = True
            if not moved:
                sin_salida.add(nodo)
                    
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
                        if hijo not in visitados and hijo not in sin_salida:
                            stack.append((hijo, camino + [hijo], profundidad + 1))
                            moved = True
                if not moved:
                    sin_salida.add(nodo)
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
                    moved = True
                    
        if not moved:
            sin_salida.add(nodo)

                    
        i += 1
    return visitados,set(camino), sin_salida
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

T = nx.DiGraph()
main()
