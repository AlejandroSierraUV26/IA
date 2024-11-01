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

    # Dibuja las líneas de los caminos tomados
    if len(backtrack_stack) > 1:
        for i in range(len(backtrack_stack) - 1):
            start_pos = (backtrack_stack[i][0] * cell_width + cell_width // 2,
                         backtrack_stack[i][1] * cell_height + cell_height // 2)
            end_pos = (backtrack_stack[i + 1][0] * cell_width + cell_width // 2,
                       backtrack_stack[i + 1][1] * cell_height + cell_height // 2)
            pygame.draw.line(screen, (0, 255, 0), start_pos, end_pos, 3)  # Color verde y grosor de 3px

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
# Lista para almacenar el camino paso a paso desde la posición actual al nodo de menor costo
path = []

def find_path(x, y, end_x, end_y):
    """Encuentra el camino al nodo de menor costo y lo guarda en la lista 'path'."""
    global path
    
    # Cola de prioridad para nodos por visitar, usando (costo acumulado, posición actual, camino hasta aquí)
    pq = [(0, x, y, [])]
    visited = set()

    while pq:
        cost, cx, cy, current_path = heapq.heappop(pq)
        print(current_path)
        
        if (cx, cy) == (end_x, end_y):  # Se alcanza el nodo objetivo
            path = current_path + [(cx, cy)]
            return
        
        if (cx, cy) in visited:
            continue

        visited.add((cx, cy))
        
        # Agrega posiciones vecinas válidas a la cola
        for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Izquierda, Derecha, Arriba, Abajo
            nx, ny = cx + dx, cy + dy
            if (0 <= nx < columnas and 0 <= ny < filas and 
                mapa[ny, nx] == 0 and (nx, ny) not in visited):
                heapq.heappush(pq, (cost + 1, nx, ny, current_path + [(cx, cy)]))

def ucs_move():
    global pos_x, pos_y, direccion, fin, path
    
    if fin:
        return
    
    if not path:  # Si no hay un camino guardado, busca uno nuevo
        find_path(pos_x, pos_y, salida_x, salida_y)
    
    if path:
        # Tomar el siguiente paso en el camino y actualizar posición
        next_pos = path.pop(0)
        pos_x, pos_y = next_pos
        # Actualizar dirección basada en el movimiento
        dx, dy = next_pos[0] - pos_x, next_pos[1] - pos_y
        if dx == 1:
            direccion = 'derecha'
        elif dx == -1:
            direccion = 'izquierda'
        elif dy == 1:
            direccion = 'abajo'
        elif dy == -1:
            direccion = 'arriba'

    # Verificar si se llegó a la meta
    if (pos_x, pos_y) == (salida_x, salida_y):
        fin = True
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
