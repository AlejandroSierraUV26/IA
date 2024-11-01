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

# Lista para almacenar el recorrido
recorrido = []



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
    global pos_x, pos_y, direccion, fin, queue, visited, decision_points, recorrido
    
    if not queue:
        reset_game("amplitud")  # Reinicia el juego si no hay movimientos válidos
        return
    
    (x, y), path = queue.popleft()  # Desencolar la posición actual y su camino

    # Verificar si se ha alcanzado la meta
    if (x, y) == (salida_x, salida_y):
        fin = True
        return

    visited.add((x, y))  # Marcar la posición actual como visitada
    recorrido.append((x, y))  # Agregar a la lista de recorrido

    directions = [((0, -1), 'arriba'), ((0, 1), 'abajo'), ((-1, 0), 'izquierda'), ((1, 0), 'derecha')]
    possible_moves = []  # Lista para los movimientos posibles

    for (dx, dy), dir in directions:
        nx, ny = x + dx, y + dy  # Nuevas coordenadas
        # Comprobar si el movimiento es válido
        if (nx, ny) not in failed_paths and 0 <= nx < columnas and 0 <= ny < filas and mapa[ny, nx] == 0 and (nx, ny) not in visited:
            possible_moves.append(((nx, ny), dir))  # Agregar movimiento válido

    # Determinar si el nodo actual es un punto de decisión
    if len(possible_moves) > 1:
        decision_points.append((x, y))

    if possible_moves:
        (nx, ny), dir = possible_moves[0]  # Tomar el primer movimiento válido
        queue.append(((nx, ny), path + [(nx, ny)]))  # Agregar a la cola
        pos_x, pos_y = nx, ny  # Actualizar posición
        direccion = dir  # Actualizar dirección
    else:
        # Si está en un callejón sin salida, marca el camino como fallido
        failed_paths.update(path)  # Marcar el camino actual como fallido
def costo():
    global pos_x, pos_y, direccion, fin, visited, priority_queue, decision_points, costs, recorrido
    
    if not priority_queue or fin:
        return
    
    # Tomar la posición con el menor costo acumulado
    current_cost, (x, y), path = heapq.heappop(priority_queue)

    # Verificar si se ha llegado a la meta
    if (x, y) == (salida_x, salida_y):
        fin = True
        print("Meta alcanzada con costo:", current_cost)
        return
    
    # Si ya se visitó, continua (esto evita procesar el mismo nodo varias veces)
    if (x, y) in visited:
        return

    # Añadir posición actual a visitados
    visited.add((x, y))
    recorrido.append((x, y))
    
    # Definir movimientos posibles
    directions = [((0, -1), 'arriba'), ((0, 1), 'abajo'), ((-1, 0), 'izquierda'), ((1, 0), 'derecha')]

    for (dx, dy), dir in directions:
        nx, ny = x + dx, y + dy  # Nuevas coordenadas
        new_cost = current_cost + 1  # Incrementar el costo al moverse a una nueva celda

        # Verificar límites, caminos válidos y que no haya ciclos
        if 0 <= nx < columnas and 0 <= ny < filas and mapa[ny, nx] == 0:
            # Verifica si hemos encontrado un costo menor para la posición
            if (nx, ny) not in costs or new_cost < costs[(nx, ny)]:
                costs[(nx, ny)] = new_cost  # Actualiza el costo
                heapq.heappush(priority_queue, (new_cost, (nx, ny), path + [(nx, ny)]))  # Agregar a la cola
                print("Añadiendo a cola:", (nx, ny), "con costo:", new_cost)
    
    # Si hay movimientos válidos, actualizar la posición y dirección
    if priority_queue:
        # Obtener el siguiente movimiento más barato
        next_cost, (nx, ny), path = priority_queue[0]
        pos_x, pos_y = nx, ny  # Actualiza la posición
        direccion = dir  # Actualiza la dirección
        print("Moviendo a:", (nx, ny), "con costo:", next_cost)
                
# def iterativa():
#     # Realiza el movimiento DFS
#     pass
def profundidad():
    global pos_x, pos_y, direccion, fin, visited, queue, decision_points, recorrido
    
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
    recorrido.append((x, y))
    
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
def profundidad_limitada():
    global pos_x, pos_y, direccion, fin, visited, stack, decision_points, recorrido
    
    if not stack or fin:
        reset_game("profundidad_limitada")
        return
    
    (x, y), path, depth = stack.pop()
    
    # Verificar si se ha llegado a la meta
    if (x, y) == (salida_x, salida_y):
        fin = True
        return
    
    # Marcar la posición actual como visitada
    visited.add((x, y))
    recorrido.append((x, y))
    
    # Si alcanzamos la profundidad máxima, marcamos el camino como fallido
    if depth >= profundidad_maxima:
        failed_paths.update(path)  # Marca el camino como fallido
        return
    
    directions = [((0, -1), 'arriba'), ((0, 1), 'abajo'), ((-1, 0), 'izquierda'), ((1, 0), 'derecha')]
    possible_moves = []
    
    for (dx, dy), dir in directions:
        nx, ny = x + dx, y + dy
        if (nx, ny) not in failed_paths and 0 <= nx < columnas and 0 <= ny < filas and mapa[ny, nx] == 0 and (nx, ny) not in visited:
            possible_moves.append(((nx, ny), dir))
    
    # Determinar si el nodo actual es un punto de decisión
    if len(possible_moves) > 1:
        decision_points.append((x, y, depth))
    
    if possible_moves:
        # Seleccionar la primera opción para avanzar
        next_pos_x, next_pos_y = possible_moves[0][0]
        direccion = possible_moves[0][1]
        
        # Agregar el nuevo movimiento a la pila
        stack.append(((next_pos_x, next_pos_y), path + [(next_pos_x, next_pos_y)], depth + 1))
    else:
        # Si no hay movimientos, marca el camino como fallido
        failed_paths.update(path)

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
    if algortimo == 'profundidad_limitada':
        pos_x, pos_y = 0, 0  # Reinicia a la posición inicial
        visited.clear()
        stack = [((pos_x, pos_y), [(pos_x, pos_y)], 0)]  # Reinicia la pila con la posición inicial
        
    

"""-------------------------------------------------
Bucle principal del programa
-------------------------------------------------"""
pygame.init()  
running = True
fin = False  # Variable de fin del juego

n = 5  # Número de veces que quieres ejecutar el algoritmo
profundidad_maxima = n 
movimientos_realizados = 0  # Contador de movimientos
costo_t = 0
while running:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
            
    # Limpia la pantalla
    screen.fill((0, 0, 0))

    map_draw()  # Dibuja el mapa
    pygame.display.flip()
    time.sleep(0.8)  # Tiempo de espera para observar los movimientos
    if movimientos_realizados == 0:
        algoritmo_seleccionado = random.choice([costo])
        if algoritmo_seleccionado != costo:
            costo_t += 1 
            costs[pos_x, pos_y] = costo_t
            
        
    
    if movimientos_realizados < n:
        # Ejecuta el algoritmo seleccionado una vez
        algoritmo_seleccionado()  # Ejecuta el algoritmo una vez
        movimientos_realizados += 1  # Aumenta el contador de movimientos
        
    if movimientos_realizados >= n:
        movimientos_realizados = 0
        # Aquí puedes agregar la lógica para cambiar de algoritmo o reiniciar, si lo deseas.

pygame.quit()
print("Recorrido del ratón:", recorrido)