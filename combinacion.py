import numpy as np
from graphviz import Graph
from collections import deque


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
    # imprimir_arbol(arbol_generado)
    
    # print(profundidad((0, 0), (5, 5), arbol_generado))
    
    # print(amplitud((0, 0), (5, 5), arbol_generado))
    # print(costo((0, 0), (5, 5), arbol_generado))
    # print(limitada((0, 0), (5, 5), arbol_generado, 10))
    # print(iterativa((0, 0), (5, 5), arbol_generado)) # Revisar
    # print(avara((0, 0), (5, 5), arbol_generado))
    camino, visitados = profundidad((0, 0), (13, 13), arbol_generado)
    camino, visitados = amplitud((0, 0), (13, 13), arbol_generado)
    camino, visitados = costo((0, 0), (13, 13), arbol_generado)
    camino, visitados = limitada((0, 0), (13, 13), arbol_generado, 15)
    camino, visitados = iterativa((0, 0), (13, 13), arbol_generado)
    camino, visitados = avara((0, 0), (13, 13), arbol_generado)
    dibujar_arbol(arbol_generado, camino)
    
    



def profundidad(inicio, final, arbol):
    # Sombrear el camino de inicio a final, que toma profundidad apartir del arbol
    # Prioridad : Derecha, Abajo, Izquierda, Arriba
    visitados = set()
    stack = [(inicio, [inicio])]
    
    while stack:
        nodo, camino = stack.pop()
        if nodo == final:
            return camino, visitados
        if nodo not in visitados:
            visitados.add(nodo)
            print(nodo)
            moved = False
            for hijo, _ in arbol.get(nodo, []):
                if hijo not in visitados:
                    stack.append((hijo, camino + [hijo]))
                    moved = True
            if not moved and camino:
                camino.pop()
    
    return camino, visitados
def amplitud(inicio, final, arbol):
    # Sombrear el camino de inicio a final, que toma amplitud apartir del arbol
    # Prioridad : Derecha, Abajo, Izquierda, Arriba
        visitados = set()
        queue = deque([(inicio, [inicio])])
        
        while queue:
            nodo, camino = queue.popleft()
            if nodo == final:
                return camino, visitados
            if nodo not in visitados:
                visitados.add(nodo)
                for hijo, _ in arbol.get(nodo, []):
                    if hijo not in visitados:
                        queue.append((hijo, camino + [hijo]))
        return camino, visitados
def costo(inicio, final, arbol):
    # Sombrear el camino de inicio a final, que toma costo apartir del arbol
    # Prioridad : Derecha, Abajo, Izquierda, Arriba
    visitados = set()
    queue = [(0, inicio, [inicio])]  # (costo, nodo, camino)
    
    while queue:
        queue.sort()  # Ordenar la cola por costo
        costo, nodo, camino = queue.pop(0)
        if nodo == final:
            return camino, visitados
        if nodo not in visitados:
            visitados.add(nodo)
            for hijo, _ in arbol.get(nodo, []):
                if hijo not in visitados:
                    queue.append((costo + 1, hijo, camino + [hijo]))
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
            if profundidad < alt_max:
                for hijo, _ in arbol.get(nodo, []):
                    if hijo not in visitados:
                        stack.append((hijo, camino + [hijo], profundidad + 1))
    return camino, visitados
def iterativa(inicio, final, arbol):
    # Sombrear el camino de inicio a final, que toma iterativa apartir del arbol
    # Prioridad : Derecha, Abajo, Izquierda, Arriba
    for alt_max in range(1, 100):
        camino, visitados = limitada(inicio, final, arbol, alt_max)
        if camino and camino[-1] == final:
            print(alt_max)
            return camino, visitados
    return camino, visitados
def avara(inicio, final, arbol):
    # Sombrear el camino de inicio a final, que toma avara apartir del arbol
    # Prioridad : Derecha, Abajo, Izquierda, Arriba
    # Definicir la heurística de la distancia de Manhattan
    dm = lambda x, y: abs(x - final[0]) + abs(y - final[1])
    visitados = set()
    queue = deque([(inicio, [inicio], 0)])
    
    while queue:
        nodo, camino, costo = queue.popleft()
        if nodo == final:
            return camino, visitados
        if nodo not in visitados:
            visitados.add(nodo)
            for hijo, _ in arbol.get(nodo, []):
                if hijo not in visitados:
                    queue.append((hijo, camino + [hijo], costo + dm(hijo[0], hijo[1])))
    return camino, visitados


    
main()

