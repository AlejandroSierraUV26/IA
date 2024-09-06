import pygame
import random
import math

# Inicializar pygame
pygame.init()
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Construcción del laberinto")

# Colores para los diferentes tipos de celdas
WHITE = (255, 255, 255)  # Libre
BLACK = (0, 0, 0)        # Obstáculo
GREEN = (0, 255, 0)      # Inicio
RED = (255, 0, 0)        # Fin

# Tamaño de la cuadrícula y celdas
rows, cols = 10, 10  # Cuadrícula de 10x10
cell_size = 35

# Calcular el desplazamiento para centrar la cuadrícula en la pantalla
offset_x = (700 - cols * cell_size) // 2
offset_y = (700 - rows * cell_size) // 2

# Estado de la cuadrícula (0: libre, 1: obstáculo, 2: inicio, 3: fin)
grid = [[1 for _ in range(cols)] for _ in range(rows)]  # Inicializar como obstáculos

# Variables para manejar las selecciones
mode = 0  # 0: libre, 1: obstáculo, 2: inicio, 3: fin
start_pos = (0, 0)
end_pos = (rows-1, cols-1)

# Función para calcular la distancia de Manhattan
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Generar posiciones aleatorias para inicio y fin
def generate_random_start_end():
    global start_pos, end_pos
    while True:
        start_pos = (random.randint(0, rows-1), random.randint(0, cols-1))
        end_pos = (random.randint(0, rows-1), random.randint(0, cols-1))
        
        # Asegurarse de que el inicio y fin estén lo suficientemente alejados
        if manhattan_distance(start_pos, end_pos) >= 6:
            break

# Función para obtener vecinos válidos (celdas que aún no han sido visitadas)
def get_valid_neighbors(row, col):
    neighbors = []
    # Arriba
    if row > 1 and grid[row - 2][col] == 1:
        neighbors.append((row - 2, col))
    # Abajo
    if row < rows - 2 and grid[row + 2][col] == 1:
        neighbors.append((row + 2, col))
    # Izquierda
    if col > 1 and grid[row][col - 2] == 1:
        neighbors.append((row, col - 2))
    # Derecha
    if col < cols - 2 and grid[row][col + 2] == 1:
        neighbors.append((row, col + 2))
    
    random.shuffle(neighbors)  # Mezclar para hacer la elección aleatoria
    return neighbors

# Algoritmo DFS modificado para generar el laberinto con retroceso y exploración inteligente
def generate_maze():
    stack = [(start_pos[0], start_pos[1])]
    grid[start_pos[0]][start_pos[1]] = 0  # Iniciar el camino desde el inicio

    while stack:
        current_row, current_col = stack[-1]
        
        # Obtener vecinos válidos
        neighbors = get_valid_neighbors(current_row, current_col)

        if neighbors:
            # Elegir vecino "inteligentemente" y romper la pared entre el actual y el vecino
            next_row, next_col = neighbors[0]
            grid[(current_row + next_row) // 2][(current_col + next_col) // 2] = 0  # Romper pared
            grid[next_row][next_col] = 0  # Hacer la celda vecina parte del camino
            stack.append((next_row, next_col))
        else:
            stack.pop()  # Retroceder si no hay vecinos válidos

# Función para dibujar la cuadrícula
def draw_grid():
    for row in range(rows):
        for col in range(cols):
            color = WHITE
            if grid[row][col] == 1:
                color = BLACK
            elif grid[row][col] == 2:
                color = GREEN
            elif grid[row][col] == 3:
                color = RED

            pygame.draw.rect(screen, color, (col * cell_size + offset_x, row * cell_size + offset_y, cell_size, cell_size))
            pygame.draw.rect(screen, (200, 200, 200), (col * cell_size + offset_x, row * cell_size + offset_y, cell_size, cell_size), 1)

# Generar el laberinto inicial con inicio y fin aleatorio
generate_random_start_end()
generate_maze()
grid[start_pos[0]][start_pos[1]] = 2  # Establecer inicio
grid[end_pos[0]][end_pos[1]] = 3      # Establecer fin

# Bucle principal
running = True
while running:
    screen.fill((255, 255, 255))
    draw_grid()  # Redibujar la cuadrícula en cada ciclo
    pygame.display.flip()  # Actualizar la pantalla después de cada cambio

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Manejar el clic del ratón
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            row, col = (y - offset_y) // cell_size, (x - offset_x) // cell_size
            
            if 0 <= row < rows and 0 <= col < cols:  # Asegurarse de que el clic esté dentro de la cuadrícula
                if mode == 2:  # Establecer el inicio
                    if start_pos:
                        grid[start_pos[0]][start_pos[1]] = 0  # Limpiar el anterior
                    start_pos = (row, col)
                    grid[row][col] = 2
                
                elif mode == 3:  # Establecer el fin
                    if end_pos:
                        grid[end_pos[0]][end_pos[1]] = 0  # Limpiar el anterior
                    end_pos = (row, col)
                    grid[row][col] = 3

                else:  # Cambiar entre libre y obstáculo
                    if grid[row][col] == 0:
                        grid[row][col] = 1  # Cambia a obstáculo por defecto si el modo es 1
                    elif grid[row][col] == 1:
                        grid[row][col] = 0  # Si es obstáculo, lo vuelve a libre

        # Manejar teclas para cambiar modo
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                mode = 0  # Modo libre
            elif event.key == pygame.K_2:
                mode = 1  # Modo obstáculo
            elif event.key == pygame.K_3:
                mode = 2  # Modo inicio
            elif event.key == pygame.K_4:
                mode = 3  # Modo fin

pygame.quit()
