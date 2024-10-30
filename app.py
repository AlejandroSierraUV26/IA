import numpy as np
import pygame
import time
from pygame.locals import *
import heapq  # Para manejar la cola de prioridad

# Tamaño de la ventana
WIDTH, HEIGHT = 500, 500

# Crear la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Definir título a la ventana
pygame.display.set_caption("Juego de Laberintos")

# Cargar las imágenes
pared = pygame.image.load('Images/pared1.png')
suelo = pygame.image.load('Images/ground1.png')
robot = pygame.image.load('Images/robot1.png')
robot_left = pygame.image.load('Images/robot1_left.png')
out1 = pygame.image.load('Images/out1.png')
fin_bg = pygame.image.load('Images/bg_winner.png')

# Escala de las imágenes
pared = pygame.transform.scale(pared, (50, 50))
suelo = pygame.transform.scale(suelo, (50, 50))
robot = pygame.transform.scale(robot, (50, 50))
robot_left = pygame.transform.scale(robot_left, (50, 50))
out1 = pygame.transform.scale(out1, (50, 50))
fin_bg = pygame.transform.scale(fin_bg, (WIDTH, HEIGHT))

# Cantidad de columnas y filas
columnas, filas = 10, 10

# Matriz del laberinto
mapa = np.array([[0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
                 [1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                 [1, 0, 1, 1, 1, 1, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 1, 1, 1, 0, 1],
                 [1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
                 [1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
                 [1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]])

# Posición inicial del robot
pos_x, pos_y = 0, 0

# Dirección inicial del robot
direccion = 'derecha'

# Posición de salida del laberinto
salida_x, salida_y = 9, 9

# Variables para UCS
priority_queue = []
heapq.heappush(priority_queue, (0, pos_x, pos_y))  # Inicial con costo 0
costs = {(pos_x, pos_y): 0}  # Costos mínimos

# Conjunto para registrar las posiciones visitadas
visited = set()

# Historial de posiciones para permitir retrocesos
backtrack_stack = []

"""-------------------------------------------------
Función que dibuja todos los elementos en el mapa
-------------------------------------------------"""
def map_draw():
    # Usar np.where para crear máscaras
    pared_mask = np.where(mapa == 1, 1, 0)
    suelo_mask = np.where(mapa == 0, 1, 0)
    
    # Tamaño de una celda en la ventana
    cell_width = WIDTH // columnas
    cell_height = HEIGHT // filas
    
    # Dibujar imágenes de "robot" y "pared" usando las máscaras
    for fil, col in np.argwhere(pared_mask == 1):
        screen.blit(pared, (col * cell_width, fil * cell_height))
    
    for fil, col in np.argwhere(suelo_mask == 1):
        screen.blit(suelo, (col * cell_width, fil * cell_height))
    
    # Dibuja al robot en función de su dirección
    if direccion == 'derecha' or direccion == 'arriba' or direccion == 'abajo':
        screen.blit(robot, (pos_x * cell_width, pos_y * cell_height))
    elif direccion == 'izquierda':
        screen.blit(robot_left, (pos_x * cell_width, pos_y * cell_height))
    
    # Dibujar la salida en la posición 9,9 del mapa
    screen.blit(out1, (salida_x * cell_width, salida_y * cell_height))
    
    if fin:
        # Cuando el robot llega a la salida, dibuja la imagen de fondo "fin_bg"
        screen.blit(fin_bg, (0, 0))

"""-------------------------------------------------
Función para movimiento UCS con Backtracking
-------------------------------------------------"""
def ucs_move():
    global pos_x, pos_y, direccion, fin
    
    if not priority_queue or fin:
        return
    
    # Tomar la posición con el menor costo acumulado
    current_cost, x, y = heapq.heappop(priority_queue)
    
    # Verificar si ya se ha llegado a la meta
    if (x, y) == (salida_x, salida_y):
        fin = True
        return
    
    # Si ya se visitó, continúa (esto evita procesar el mismo nodo varias veces)
    if (x, y) in visited:
        return

    # Añadir posición actual a visitados y al historial de backtracking
    visited.add((x, y))
    backtrack_stack.append((x, y))
    
    # Definir movimientos posibles
    directions = [((0, -1), 'arriba'), ((0, 1), 'abajo'), ((-1, 0), 'izquierda'), ((1, 0), 'derecha')]
    has_valid_moves = False  # Marca si hay movimientos posibles desde la posición actual

    for (dx, dy), dir in directions:
        nx, ny = x + dx, y + dy
        new_cost = current_cost + 1
        
        # Verificar límites, caminos válidos, y que no haya ciclos
        if 0 <= nx < columnas and 0 <= ny < filas and mapa[ny, nx] == 0 and (nx, ny) not in visited:
            # Solo agrega a la cola si es un movimiento válido
            costs[(nx, ny)] = new_cost
            heapq.heappush(priority_queue, (new_cost, nx, ny))
            has_valid_moves = True  # Hay al menos un movimiento válido desde aquí

    # Actualizar posición y dirección si hay movimiento válido
    if has_valid_moves:
        pos_x, pos_y = x, y
        direccion = dir
    else:
        # Retrocede si no hay movimientos válidos desde esta posición
        if backtrack_stack:
            backtrack_stack.pop()  # Elimina la última posición
            if backtrack_stack:  # Verifica que aún haya historial
                pos_x, pos_y = backtrack_stack[-1]  # Regresa a la última posición disponible

"""-------------------------------------------------
Bucle principal del programa
-------------------------------------------------"""
pygame.init()
running = True
fin = False

while running:
    time.sleep(1)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
    
    # Llamar a la función de movimiento UCS continuamente si no se ha llegado a la meta
    if not fin:
        ucs_move()
    
    # Verifica si el robot ha llegado a la posición de salida
    if not fin and pos_x == salida_x and pos_y == salida_y:
        fin = True
    
    # Función de dibujo
    map_draw()

    # Actualizar la ventana
    pygame.display.flip()
    
# Cerrar Pygame
pygame.quit()
