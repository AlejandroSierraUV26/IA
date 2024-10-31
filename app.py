import numpy as np
import pygame
import random
import time
from pygame.locals import *
from collections import deque
import heapq

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
salida_x, salida_y = 11, 5

# ! Variables de control
visited = set() # amplitud, 

queue = deque([((pos_x, pos_y), [(pos_x, pos_y)])])  # Cola para BFS # Amplitud

failed_paths = set()  # Guarda caminos completos bloqueados

decision_points = []  # Guarda puntos de decisión

costs = {(pos_x, pos_y): 0}  # Costo

priority_queue = [(0, (pos_x, pos_y), [(pos_x, pos_y)])]  # Cola de prioridad para el algoritmo de costo




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
# Amplitud
# Costo
# Iterativa
# Profundidad
# Profundidad limitada

def amplitud():
    global pos_x, pos_y, direccion, fin, queue, visited, decision_points
    
    if not queue:
        reset_game("amplitud")  # Reinicia el juego si no hay movimientos válidos
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
def costo():
    global pos_x, pos_y, direccion, fin, visited, priority_queue, decision_points, costs
    
    if not priority_queue or fin:
        return
    
    # Tomar la posición con el menor costo acumulado
    current_cost, (x, y), path = heapq.heappop(priority_queue)
    
    # Verificar si ya se ha llegado a la meta
    if (x, y) == (salida_x, salida_y):
        fin = True
        return
    
    # Si ya se visitó, continúa (esto evita procesar el mismo nodo varias veces)
    if (x, y) in visited:
        return

    # Añadir posición actual a visitados
    visited.add((x, y))
    
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
            heapq.heappush(priority_queue, (new_cost, (nx, ny), path + [(nx, ny)]))
            has_valid_moves = True  # Hay al menos un movimiento válido desde aquí

    # Actualizar posición y dirección si hay movimiento válido
    if has_valid_moves:
        pos_x, pos_y = x, y
        direccion = dir
    else:
        # Retrocede si no hay movimientos válidos desde esta posición
        if path:
            pos_x, pos_y = path[-1]  # Regresa a la última posición disponible

    
    
# def iterativa():
#     # Realiza el movimiento DFS
#     pass
def profundidad():
    global pos_x, pos_y, direccion, fin, visited, queue, decision_points
    
    if not queue or fin:
        reset_game("profundidad")
        return
    
    (x, y), path = queue.pop()
    
    # Verificar si ya se ha llegado a la meta
    if (x, y) == (salida_x, salida_y):
        fin = True
        return
    
    # Registrar la posición como visitada
    visited.add((x, y))
    
    # Probar movimientos en profundidad con backtracking
    directions = [((0, -1), 'arriba'), ((0, 1), 'abajo'), ((-1, 0), 'izquierda'), ((1, 0), 'derecha')]
    moved = False
    possible_moves = []
    for (dx, dy), dir in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < columnas and 0 <= ny < filas and mapa[ny, nx] == 0 and (nx, ny) not in visited:
            queue.append(((nx, ny), path + [(nx, ny)]))
            possible_moves.append(((nx, ny), dir))
            moved = True
            break
    
    # Si no se puede mover a ninguna dirección, retrocede
    if not moved:
        if queue:  # Verifica que aún haya nodos en la cola
            (pos_x, pos_y), _ = queue[-1]  # Retrocede a la posición anterior
    
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
# def profundidad_limitada():
#     # Realiza el movimiento DFS con límite de profundidad
#     pass

def reset_game(algortimo):
    global pos_x, pos_y, visited, queue, decision_points
    if algortimo == 'amplitud':
        
        pos_x, pos_y = decision_points.pop() if decision_points else (0, 0)
        visited.clear()
        queue = deque([((pos_x, pos_y), [(pos_x, pos_y)])])
    if algortimo == 'profundidad':
        pos_x, pos_y = decision_points.pop() if decision_points else (0, 0)
        visited.clear()
        queue = deque([((pos_x, pos_y), [(pos_x, pos_y)])])
        
    

"""-------------------------------------------------
Bucle principal del programa
-------------------------------------------------"""
pygame.init()  
running = True
fin = False  # Variable de fin del juego

n = 5  # Número de veces que quieres ejecutar el algoritmo
movimientos_realizados = 0  # Contador de movimientos


while running:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
            
    # Limpia la pantalla
    screen.fill((0, 0, 0))

    map_draw()  # Dibuja el mapa
    pygame.display.flip()
    time.sleep(0.5)  # Tiempo de espera para observar los movimientos
    algoritmo_seleccionado = random.choice([amplitud, profundidad, costo])
    for i in range(3):
        if not fin and movimientos_realizados < n:
            # Ejecuta el algoritmo seleccionado una vez
            print(algoritmo_seleccionado.__name__)
            algoritmo_seleccionado()  # Ejecuta el algoritmo una vez
            movimientos_realizados += 1  # Aumenta el contador de movimientos
            print(f"Movimientos realizados: {movimientos_realizados}/{n}")
            
        if movimientos_realizados >= n:
            print("Se han alcanzado el número máximo de movimientos.")
            movimientos_realizados = 0
            # Aquí puedes agregar la lógica para cambiar de algoritmo o reiniciar, si lo deseas.
    print()

pygame.quit()
