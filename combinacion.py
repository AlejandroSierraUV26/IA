import numpy as np
import graphviz

class Nodo:
    def __init__(self, x, y, padre=None):
        self.x = x
        self.y = y
        self.padre = padre
        self.hijos = []
        self.visitado = False
    def __str__(self):
        return f'({self.x}, {self.y})'
    def __repr__(self):
        return f'({self.x}, {self.y})'
    def __eq__(self, otro):
        return self.x == otro.x and self.y == otro.y
    def __hash__(self):
        return hash((self.x, self.y))
    def __lt__(self, otro):
        return self.x < otro.x and self.y < otro.y
    def __le__(self, otro):
        return self.x <= otro.x and self.y <= otro.y
    def __gt__(self, otro):
        return self.x > otro.x and self.y > otro.y
    
grafo = graphviz.Digraph('G', filename='laberinto_dfs', format='svg')
grafo.attr(size='15,15')
def profundidad(x, y, caminos):
    lista_nodos = []
    
    # Arriba, derecha, abajo, izquierda
    vecinos = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
    
    for vecino in vecinos:
        if vecino[0] >= 0 and vecino[0] < columnas and vecino[1] >= 0 and vecino[1] < filas:
            if mapa[vecino[1], vecino[0]] == 0 and (vecino[0], vecino[1]) not in caminos:
                lista_nodos.append(Nodo(vecino[0], vecino[1]))        
    return lista_nodos
def amplitud(x, y, caminos):
    # La caracteristica de la busqueda en amplitud es que se recorre por niveles
    # es decir, se recorren todos los nodos de un nivel antes de pasar al siguiente
    # En este caso, se recorren todos los nodos vecinos de un nodo antes de pasar al siguiente
    # Se puede implementar una cola para almacenar los nodos
    
    # Debe devolver la lista de nodos que se pueden visitar
    lista_nodos = []
    
    # Arriba, derecha, abajo, izquierda
    vecinos = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
    
    for vecino in vecinos:
        if vecino[0] >= 0 and vecino[0] < columnas and vecino[1] >= 0 and vecino[1] < filas:
            if mapa[vecino[1], vecino[0]] == 0 and (vecino[0], vecino[1]) not in caminos:
                lista_nodos.append(Nodo(vecino[0], vecino[1]))
    return lista_nodos
def costo_uniforme(x, y, caminos):
    pass
def limitada(x, y, caminos, limite):
    pass
def iterativa(x, y, caminos):
    pass
def avara(x, y, caminos):
    pass


columnas, filas = 15, 15
mapa = np.array([
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1],
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
pos_x, pos_y = 1, 1
salida_x, salida_y = 11, 5
nodos_visitados = []
camino = []
i = 0
n = 20
pos = Nodo(pos_x, pos_y)
inicial_node = pos


while i < n:
    pos = profundidad(pos_x, pos_y, nodos_visitados)
    if len(pos) == 0:
        
        for cam in camino:
            if len(cam) > 1:
                pos_x = cam[1].x
                pos_y = cam[1].y
                pos_x0 = cam[0].x
                pos_y0 = cam[0].y
                cam.pop(0)
            
                grafo.edge(str((pos_x0, pos_y0)), str((pos_x, pos_y)))
                
                pos = profundidad(pos_x, pos_y, nodos_visitados)
                # Remover el primer nodo 
            
                
    camino.append(pos)
    nodos_visitados.append((pos_x, pos_y))
    izq = pos[0]
    pos_x = izq.x
    pos_y = izq.y
    
    grafo.node(str((pos_x, pos_y)), label=f"({pos_x}, {pos_y})")
    if i == 0:
        grafo.edge(str(inicial_node), str((pos_x, pos_y)))
    if i > 0:
        grafo.edge(str(nodos_visitados[-1]), str((pos_x, pos_y)))
        if len(pos) > 1:
            for i in range(1, len(pos)):
                grafo.edge(str((pos_x, pos_y)), str(pos[i]))
    
    if pos_x == salida_x and pos_y == salida_y:
        grafo.node(str((pos_x, pos_y)), shape='doublecircle', color='green', label=f"Salida: ({pos_x}, {pos_y})")
        break
    
    
    
    i += 1
print(camino)
grafo.view()

    
# print()

# print("Alternativa 2")
# pos_x = pos.x
# pos_y = pos.y

# for i in range(38):
#     pos = profundidad(pos_x, pos_y, nodos_visitados)
#     camino.append(pos)
#     nodos_visitados.append((pos_x, pos_y))
#     print(pos)
#     izq = pos[0]
#     pos_x = izq.x
#     pos_y = izq.y
#     if pos_x == salida_x and pos_y == salida_y:
#         print("Salida encontrada")
#         break





     