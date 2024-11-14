import numpy as np
from graphviz import Graph
from collections import deque
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
def dibujar_arbol(arbol, camino):
    g = Graph('G', filename='arbol', format='svg')
    for nodo in arbol:
        if nodo in camino:
            g.node(str(nodo), color='red', style='filled')
        else:
            g.node(str(nodo))
        for hijo, direccion in arbol[nodo]:
            if direccion == (-1, 0):
                direccion = 'Arriba'
            elif direccion == (1, 0):
                direccion = 'Abajo'
            elif direccion == (0, -1):
                direccion = 'Izquierda'
            elif direccion == (0, 1):
                direccion = 'Derecha'
            
            g.edge(str(nodo), str(hijo), label=str(direccion))
    g.view()
def main():
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
    arbol_generado = construir_arbol((0, 0), mapa)
    # Inicia en (0, 0) y termina en (13, 13)
    
    camino_recodido = leer_camino_recorrido()
    camino, visitados = amplitud((0, 0), (13, 13), arbol_generado, 2)
    visitados = visitados.union(set(camino_recodido))
    
    
    camino_recodido = leer_camino_recorrido()
    camino, visitados = profundidad(camino_recodido[-1], (13, 13), arbol_generado, 2)
    visitados = visitados.union(set(camino_recodido))
    
    
    camino_recodido = leer_camino_recorrido()
    camino, visitados = costo(camino_recodido[-1], (13, 13), arbol_generado, 2)
    visitados = visitados.union(set(camino_recodido))
    
    
    camino_recodido = leer_camino_recorrido()
    camino, visitados = limitada(camino_recodido[-1], (13, 13), arbol_generado, 2)
    visitados = visitados.union(set(camino_recodido))
    
    camino_recodido = leer_camino_recorrido()
    camino, visitados = iterativa(camino_recodido[-1], (13, 13), arbol_generado, 2)
    camino_recodido = visitados.union(set(camino_recodido))
    
    camino_recodido = leer_camino_recorrido()
    camino, visitados = avara(camino_recodido[-1], (13, 13), arbol_generado, 20)
    visitados = visitados.union(set(camino_recodido))
    

    dibujar_arbol(arbol_generado, visitados)
    

    with open("camino.txt", "w") as f:
        f.write("")
         


def profundidad(inicio, final, arbol, n, camino_previo=None ):
    # Sombrear el camino de inicio a final, que toma profundidad a partir del arbol
    # Prioridad : Derecha, Abajo, Izquierda, Arriba
    visitados = set(camino_previo) if camino_previo else set()
    stack = [(inicio, camino_previo + [inicio] if camino_previo else [inicio])]
    i = 0
    while stack:
        if i == n:
            break
        nodo, camino = stack.pop()
        if nodo == final:
            return camino, visitados
        if nodo not in visitados:
            visitados.add(nodo)
            guardar_camino(nodo)
            moved = False
            for hijo, _ in arbol.get(nodo, []):
                if hijo not in visitados:
                    stack.append((hijo, camino + [hijo]))
                    moved = True
            if not moved and camino:
                camino.pop()
        i += 1
    return camino, visitados
def amplitud(inicio, final, arbol, altura_max):
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
                return camino, visitados
            if nodo not in visitados:
                visitados.add(nodo)
                guardar_camino(nodo)
                for hijo, _ in arbol.get(nodo, []):
                    if hijo not in visitados:
                        queue.append((hijo, camino + [hijo]))
            i += 1
        return camino, visitados
def costo(inicio, final, arbol, n):
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
            return camino, visitados
        if nodo not in visitados:
            visitados.add(nodo)
            guardar_camino(nodo)
            for hijo, _ in arbol.get(nodo, []):
                if hijo not in visitados:
                    queue.append((costo + 1, hijo, camino + [hijo]))
        i += 1
    return camino, visitados
def limitada(inicio, final, arbol, alt_max):
    # Sombrear el camino de inicio a final, que toma limitada apartir del arbol
    # Prioridad : Derecha, Abajo, Izquierda, Arriba
    visitados = set()
    stack = [(inicio, [inicio], 0)]
    
    while stack:
        nodo, camino, profundidad = stack.pop()
        if nodo == final:
            return camino, visitados
        if nodo not in visitados:
            visitados.add(nodo)
            guardar_camino(nodo)
            if profundidad < alt_max:
                for hijo, _ in arbol.get(nodo, []):
                    if hijo not in visitados:
                        stack.append((hijo, camino + [hijo], profundidad + 1))
    return camino, visitados
def iterativa(inicio, final, arbol, alt_max):
    # Sombrear el camino de inicio a final, que toma iterativa apartir del arbol
    # Prioridad : Derecha, Abajo, Izquierda, Arriba
    for alt_max in range(1, alt_max + 1):
        camino, visitados = limitada(inicio, final, arbol, alt_max)
        if camino and camino[-1] == final:
            print(alt_max)
            return camino, visitados
    return camino, visitados
def avara(inicio, final, arbol, n):
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
            return camino, visitados
        if nodo not in visitados:
            visitados.add(nodo)
            guardar_camino(nodo)
            for hijo, _ in arbol.get(nodo, []):
                if hijo not in visitados:
                    heapq.heappush(queue, (dm(hijo[0], hijo[1]), hijo, camino + [hijo]))
        i += 1
    return set(camino), visitados
def guardar_camino(nodo):
    with open("camino.txt", "a") as f:
        f.write(f"{nodo}\n")

def leer_camino_recorrido():
    with open("camino.txt", "r") as f:
        if not f.read():
            return []
        f = f.read().splitlines()
        elem = []
        for linea in f:
            elem.append(eval(linea))
        
        
            
    return elem
            
main()
