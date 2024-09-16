"""
Debemos constuir el arbol a partir de los movimientos posibles,
La informacion esta almacenada en el archivo movimientos.txt

"""

import numpy as np
import networkx as nx
import ast 
import pygame as pg


def procesar_elemento(elemento):
    """Función recursiva para procesar tuplas y listas anidadas"""
    if isinstance(elemento, tuple) and len(elemento) == 2:
        return elemento  # Devolver la tupla
    elif isinstance(elemento, list):
        # Procesar cada elemento de la lista de manera recursiva
        return [procesar_elemento(e) for e in elemento]
    else:
        raise ValueError(f"Formato inválido encontrado: {elemento}")

def leer_movimientos():
    with open("movimientos.txt", "r") as archivo:
        contenido = archivo.read().splitlines()  # Leer cada línea sin el salto de línea
        movimientos = []
        
        for dato in contenido:
            if dato:  # Verificar si la línea no está vacía
                try:
                    # Intentar convertir la línea a una estructura Python (tupla o lista de tuplas)
                    elemento = ast.literal_eval(dato)
                    
                    # Procesar la estructura, permitiendo listas anidadas
                    procesado = procesar_elemento(elemento)
                    movimientos.append(procesado)
                
                except (ValueError, SyntaxError):
                    print(f"Error de conversión en: {dato}")
        
    return movimientos




def construir_arbol():
    movimientos = leer_movimientos()
    G = nx.Graph()

    # Agregar el nodo raíz
    raiz = (0, 0)
    G.add_node(raiz)

    def agregar_nodos(nodo_actual, mov):
        """Función recursiva para agregar nodos al grafo"""
        if isinstance(mov, tuple):  # Si es una tupla individual
            G.add_node(mov)
            G.add_edge(nodo_actual, mov)
        elif isinstance(mov, list):  # Si es una lista (puede contener tuplas o sublistas)
            for submov in mov:
                if isinstance(submov, tuple):  # Procesar cada tupla en la lista
                    G.add_node(submov)
                    G.add_edge(nodo_actual, submov)
                    nodo_actual = submov  # Actualizamos el nodo actual para los siguientes hijos
                elif isinstance(submov, list):  # Procesar sublistas recursivamente
                    for item in submov:
                        if isinstance(item, tuple):
                            G.add_node(item)
                            G.add_edge(nodo_actual, item)
                        elif isinstance(item, list):
                            agregar_nodos(nodo_actual, item)

    # Comenzar a procesar cada movimiento
    for mov in movimientos:
        if isinstance(mov, tuple):
            G.add_node(mov)
            G.add_edge(raiz, mov)
        elif isinstance(mov, list):
            agregar_nodos(raiz, mov)

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

    
    
dibujar_arbol()

 

    
