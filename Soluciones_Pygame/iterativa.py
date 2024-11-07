import numpy as np
import pygame
import time
from pygame.locals import *
from collections import deque

# Tamaño de la ventana
WIDTH, HEIGHT = 500, 500

pared = pygame.image.load('Images/pared1.png')
suelo = pygame.image.load('Images/ground1.png')
robot = pygame.image.load('Images/robot1.png')
robot_left = pygame.image.load('Images/robot1_left.png')
out1 = pygame.image.load('Images/out1.png')
fin_bg = pygame.image.load('Images/bg_winner.png')

# Crear la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Laberintos")

# Cargar y escalar imágenes
pared = pygame.transform.scale(pygame.image.load('Images/pared1.png'), (50, 50))
suelo = pygame.transform.scale(pygame.image.load('Images/ground1.png'), (50, 50))
robot = pygame.transform.scale(pygame.image.load('Images/robot1.png'), (50, 50))
robot_left = pygame.transform.scale(pygame.image.load('Images/robot1_left.png'), (50, 50))
out1 = pygame.transform.scale(pygame.image.load('Images/out1.png'), (50, 50))
fin_bg = pygame.transform.scale(fin_bg, (WIDTH, HEIGHT))

# Parámetros del laberinto
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


# Posiciones
pos_x, pos_y = 0, 0
direccion = 'derecha'
salida_x, salida_y = 11,5

# Variables de control
visited = set()
stack = deque([((pos_x, pos_y), [(pos_x, pos_y)], 0)])  # Pila para DFS con límite de profundidad
failed_paths = set()  # Guarda caminos completos bloqueados
decision_points = []  # Guarda puntos de decisión

# Límite de profundidad
profundidad_maxima = 1


"""-------------------------------------------------
Función que dibuja todos los elementos en el mapa
-------------------------------------------------"""
def map_draw():
    pared_mask = np.where(mapa == 1, 1, 0)
    suelo_mask = np.where(mapa == 0, 1, 0)
    cell_width = WIDTH // columnas
    cell_height = HEIGHT // filas
    
    for fil, col in np.argwhere(pared_mask == 1):
        screen.blit(pared, (col * cell_width, fil * cell_height))
    
    for fil, col in np.argwhere(suelo_mask == 1):
        screen.blit(suelo, (col * cell_width, fil * cell_height))
    
    # Dibuja al robot
    if direccion in ['derecha', 'arriba', 'abajo']:
        screen.blit(robot, (pos_x * cell_width, pos_y * cell_height))
    elif direccion == 'izquierda':
        screen.blit(robot_left, (pos_x * cell_width, pos_y * cell_height))
    
    # Dibujar la salida
    screen.blit(out1, (salida_x * cell_width, salida_y * cell_height))
    
    # Fondo de finalización
    if fin:
        screen.blit(fin_bg, (0, 0))

"""-------------------------------------------------
Función para movimiento DFS con límite de profundidad
-------------------------------------------------"""
def dfs_limited_depth_move():
    global direccion, fin, pos_x, pos_y
    # Reinicia el juego si no hay movimientos válidos
    if not stack:
        reset_game()  # Reinicia el juego si no hay movimientos válidos
        return
    
    (x, y), path, depth = stack.pop()
    
    if (x, y) == (salida_x, salida_y):
        fin = True
        return
    
    # Se marca como visitado antes de avanzar en la profundidad
    visited.add((x, y))
    if depth >= profundidad_maxima:
        failed_paths.update(path)
        return
    
    directions = [((0, -1), 'arriba'), ((0, 1), 'abajo'), ((-1, 0), 'izquierda'), ((1, 0), 'derecha')]
    possible_moves = []
    
    for (dx, dy), dir in directions:
        nx, ny = x + dx, y + dy
        # Se verifica que no haya retroceso a una posición visitada en la rama actual
        if (nx, ny) not in failed_paths and (nx, ny) not in visited and 0 <= nx < columnas and 0 <= ny < filas and mapa[ny, nx] == 0:
            possible_moves.append(((nx, ny), dir))
    
    if len(possible_moves) > 1:
        decision_points.append((x, y, depth))
    
    if possible_moves:
        next_pos_x, next_pos_y = possible_moves[0][0]
        direccion = possible_moves[0][1]
        # Se agrega el nuevo nodo al stack y lo marca como visitado
        stack.append(((next_pos_x, next_pos_y), path + [(next_pos_x, next_pos_y)], depth + 1))
        visited.add((next_pos_x, next_pos_y))
        pos_x, pos_y = next_pos_x, next_pos_y
    else:
        failed_paths.update(path)
        
def increment_level():
    global profundidad_maxima
    profundidad_maxima += 1
    print()
    print("Aumento")
    
def reset_game():
    global pos_x, pos_y, stack, visited, decision_points, profundidad_maxima, possible_moves
    
    
    if decision_points:
        pos_x, pos_y, depth = decision_points.pop()
    else:
        pos_x, pos_y, depth = (0, 0, 0)
        failed_paths.clear()  # Limpia caminos fallidos para 
        increment_level()  # Aumenta la profundidad máxima
        
    visited.clear()
    stack = deque([((pos_x, pos_y), [(pos_x, pos_y)], depth)])
    
    

"""-------------------------------------------------
Bucle principal del programa
-------------------------------------------------"""
pygame.init()  
running = True
fin = False
move_count = 0  # Contador para controlar el número de movimientos

while running:
    time.sleep(0.3)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
    
    if not fin:
        dfs_limited_depth_move()
    
    if pos_x == salida_x and pos_y == salida_y:
        fin = True
    
    map_draw()
    pygame.display.flip()

pygame.quit()