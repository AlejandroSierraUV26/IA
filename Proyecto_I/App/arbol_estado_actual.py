"""
Debemos constuir el arbol a partir de los movimientos posibles,
La informacion esta almacenada en el archivo movimientos.txt

"""
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import ast 
import pygame as pg

def leer_arbol():
    with open("arbol.txt", "r") as archivo:
        contenido = archivo.read()
        contenido = contenido.split("-")
        inicio = contenido[0]
        nodos = contenido[1].split("\n")
        aristas = contenido[2].split("\n")
        inicio = ast.literal_eval(inicio)
        nodos = [ast.literal_eval(nodo) for nodo in nodos if nodo]
        aristas = [ast.literal_eval(arista) for arista in aristas if arista]    
    return inicio, nodos, aristas

def construir_arbol():
    movimientos = leer_arbol()
    G = nx.Graph()

    # Agregar el nodo raíz
    G.add_node(movimientos[0])
    
    for nodo in movimientos[1]:
        G.add_node(nodo)
    
    for arista in movimientos[2]:
        G.add_edge(arista[0], arista[1])
    
    plt.figure()
    nx.draw(G, with_labels=True)
    plt.show()
    return G


def posicionar_nodos_jerarquicamente(G, nivel_y=100, separacion_x=100):
    niveles = {}
    for nodo in G.nodes():
        niveles[nodo] = nx.shortest_path_length(G, (0, 0), nodo)
    
    nodos_por_nivel = {}
    for nodo, nivel in niveles.items():
        if nivel not in nodos_por_nivel:
            nodos_por_nivel[nivel] = []
        nodos_por_nivel[nivel].append(nodo)
    
    posiciones = {}
    for nivel, nodos in nodos_por_nivel.items():
        x_inicial = (len(nodos) - 1) * -separacion_x / 2  
        for i, nodo in enumerate(nodos):
            posiciones[nodo] = (x_inicial + i * separacion_x, nivel * nivel_y)
    
    return posiciones


def dibujar_arbol():
    pg.init()
    
    ancho_pantalla, alto_pantalla = 800, 600
    pantalla = pg.display.set_mode((ancho_pantalla, alto_pantalla))
    pg.display.set_caption("Árbol de movimientos balanceado")
    reloj = pg.time.Clock()
    
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    ROJO = (255, 0, 0)
    
    G = construir_arbol()
    
    posiciones = posicionar_nodos_jerarquicamente(G, nivel_y=100, separacion_x=100)
    
    for nodo, (x, y) in posiciones.items():
        posiciones[nodo] = (x + ancho_pantalla // 2, y + 50)  # Centrar y ajustar
    
    ejecutando = True
    while ejecutando:
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                ejecutando = False
        
        pantalla.fill(BLANCO)
        
        for nodo in G.nodes():
            x, y = posiciones[nodo]
            pg.draw.circle(pantalla, ROJO, (int(x), int(y)), 20)
        
        for (nodo1, nodo2) in G.edges():
            x1, y1 = posiciones[nodo1]
            x2, y2 = posiciones[nodo2]
            pg.draw.line(pantalla, NEGRO, (int(x1), int(y1)), (int(x2), int(y2)), 2)
        
        pg.display.flip()
        reloj.tick(60)
    
    pg.quit()

    
    
print(construir_arbol())

 

    
