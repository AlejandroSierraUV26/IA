import numpy as np
import pygame
import time
from pygame.locals import *
from collections import deque

# Tamaño de la ventana
WIDTH, HEIGHT = 500, 500

# Crear la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Laberintos")

# Cargar y escalar imágenes
pared = pygame.transform.scale(pygame.image.load('Images/pared1.png'), (50, 50))
suelo = pygame.transform.scale(pygame.image.load('Images/ground1.png'), (50, 50))
robot = pygame.transform.scale(pygame.image.load('Images/robot1.png'), (50, 50))
robot_left = pygame.transform.scale(pygame.image.load('Images/robot1_left.png'), (50, 50))
out1 = pygame.transform.scale(pygame.image.load('Images/out1.png'), (50, 50))
fin_bg = pygame.transform.scale(pygame.image.load('Images/bg_winner.png'), (WIDTH, HEIGHT))

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
queue = deque([((pos_x, pos_y), [(pos_x, pos_y)])])  # Cola para BFS
failed_paths = set()  # Guarda caminos completos bloqueados
decision_points = []  # Guarda puntos de decisión

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
    if direccion == 'derecha' or direccion == 'arriba' or direccion == 'abajo':
        screen.blit(robot, (pos_x * cell_width, pos_y * cell_height))
    elif direccion == 'izquierda':
        screen.blit(robot_left, (pos_x * cell_width, pos_y * cell_height))
    
    # Dibujar la salida
    screen.blit(out1, (salida_x * cell_width, salida_y * cell_height))
    
    # Fondo de finalización
    if fin:
        screen.blit(fin_bg, (0, 0))

"""-------------------------------------------------
Función para movimiento BFS evitando caminos previos
-------------------------------------------------"""
def bfs_move():
    global pos_x, pos_y, direccion, fin, queue, visited, decision_points
    
    if not queue:
        reset_game()  # Reinicia el juego si no hay movimientos válidos
        return
    
    (x, y), path = queue.popleft()
    
    if (x, y) == (salida_x, salida_y):
        fin = True
        return
    
    visited.add((x, y))
    
    directions = [((0, -1), 'arriba'), ((0, 1), 'abajo'), ((-1, 0), 'izquierda'), ((1, 0), 'derecha')]
    possible_moves = []
    
    for (dx, dy), dir in directions:
        nx, ny = x + dx, y + dy
        if (nx, ny) not in failed_paths and 0 <= nx < columnas and 0 <= ny < filas and mapa[ny, nx] == 0 and (nx, ny) not in visited:
            possible_moves.append(((nx, ny), dir))
    
    # Determinar si el nodo actual es un punto de decisión
    if len(possible_moves) > 1:
        decision_points.append((x, y))
    
    if possible_moves:
        (nx, ny), dir = possible_moves[0]
        queue.append(((nx, ny), path + [(nx, ny)]))
        pos_x, pos_y = nx, ny
        direccion = dir
    else:
        # Si está en un callejón sin salida, marca el camino como fallido
        failed_paths.update(path)

def reset_game():
    global pos_x, pos_y, queue, visited, decision_points
    
    # Reinicia el juego desde el punto de decisión más cercano
    pos_x, pos_y = decision_points.pop() if decision_points else (0, 0)
    visited.clear()
    queue = deque([((pos_x, pos_y), [(pos_x, pos_y)])])

"""-------------------------------------------------
Bucle principal del programa
-------------------------------------------------"""
pygame.init()  
running = True
fin = False

while running:
    time.sleep(0.4)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
    
    if not fin:
        bfs_move()
    
    if not fin and pos_x == salida_x and pos_y == salida_y:
        fin = True
    
    map_draw()
    pygame.display.flip()
    
pygame.quit()
