import networkx as nx
import matplotlib.pyplot as plt
import time

def leer_datos():
    with open('datos.txt') as f:
        f = f.read().splitlines()
        return [eval(line) for line in f if line]

def dibujar_arbol():
    caminos_posibles = leer_datos()
    nodos_puestos = set()
    G = nx.Graph()
    
    # Mapeo de posiciones para un layout manual en niveles
    posiciones = {}
    
    for camino in caminos_posibles:
        for i, nodo in enumerate(camino):
            if nodo not in nodos_puestos:
                nodos_puestos.add(nodo)
                G.add_node(nodo)

                # Posición jerárquica: usamos la coordenada y para el nivel y x para la distribución horizontal
                posiciones[nodo] = (nodo[1], -nodo[0])

                # Dibujo en cada paso
                plt.clf()
                nx.draw(G, pos=posiciones, with_labels=True, node_size=500, node_color="skyblue", font_size=10)
                plt.draw()
                plt.pause(0.5)

        for i in range(len(camino) - 1):
            G.add_edge(camino[i], camino[i + 1])
    
    # Dibuja el árbol final
    plt.clf()
    nx.draw(G, pos=posiciones, with_labels=True, node_size=500, node_color="skyblue", font_size=10)
    plt.show()

dibujar_arbol()