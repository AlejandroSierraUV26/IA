import pygame
import random
import math
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def generate_random_start_end():
    global start_pos, end_pos
    while True:
        start_pos = (random.randint(0, rows-1), random.randint(0, cols-1))
        end_pos = (random.randint(0, rows-1), random.randint(0, cols-1))
        
        # Asegurarse de que el inicio y fin estén lo suficientemente alejados
        if manhattan_distance(start_pos, end_pos) >= 6:
            break
        
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

def generate_maze():
    stack = [(start_pos[0], start_pos[1])]
    grid[start_pos[0]][start_pos[1]] = 0  # Iniciar el camino desde el inicio

    while stack:
        current_row, current_col = stack[-1]
        
        # Obtener vecinos válidos
        neighbors = get_valid_neighbors(current_row, current_col)

        if neighbors:
            next_row, next_col = neighbors[0]
            grid[(current_row + next_row) // 2][(current_col + next_col) // 2] = 0  # Romper pared
            grid[next_row][next_col] = 0  # Hacer la celda vecina parte del camino
            stack.append((next_row, next_col))
        else:
            stack.pop()  # Retroceder si no hay vecinos válidos

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


# ======================================================================
pygame.init()
width, height = 700, 700

screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Construcción del laberinto")

BACKGROUND = (6, 214, 160)
WHITE = (255, 255, 255)  # Libre
BLACK = (7, 59, 76)        # Obstáculo
GREEN = (0, 119, 182)      # Inicio
RED = (255, 195, 0)        # Fin

font = pygame.font.Font(None, 74)  

background_color = (0, 128, 255)  # Azul claro
text_color = (255, 255, 255)  # Blanco

title_text = font.render('Modifique el Lab', True, text_color)

rows, cols = 10, 10  # Cuadrícula de 10x10
cell_size = 35


offset_x = (700 - cols * cell_size) // 2
offset_y = (700 - rows * cell_size) // 2
# sirve para centrar la cuadrícula verticalmente


grid = [[1 for _ in range(cols)] for _ in range(rows)]  # Inicializar como obstáculos


mode = 0  # 0: libre, 1: obstáculo, 2: inicio, 3: fin
start_pos = (0, 0)
end_pos = (rows-1, cols-1)

generate_random_start_end()
generate_maze()
grid[start_pos[0]][start_pos[1]] = 2  # Establecer inicio
grid[end_pos[0]][end_pos[1]] = 3      # Establecer fin

running = True
while running:   
    screen.fill(BACKGROUND) 
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 50))
    
    draw_grid()  
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            row, col = (y - offset_y) // cell_size, (x - offset_x) // cell_size
            
            if 0 <= row < rows and 0 <= col < cols: 
                if mode == 2:  
                    if start_pos:
                        grid[start_pos[0]][start_pos[1]] = 0 
                    start_pos = (row, col)
                    grid[row][col] = 2
                
                elif mode == 3:  
                    if end_pos:
                        grid[end_pos[0]][end_pos[1]] = 0  
                    end_pos = (row, col)
                    grid[row][col] = 3

                else:  
                    if grid[row][col] == 0:
                        grid[row][col] = 1  
                    elif grid[row][col] == 1:
                        grid[row][col] = 0 

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
print("Una vez terminado se le genera el laberinto, el cual se puede guardar en un archivo de texto")

# ======================================================================

with open("lab_matrix.txt", "w") as f:
    for row in grid:
        f.write(" ".join(map(str, row)) + "\n")
print("El laberinto se ha guardado en un archivo de texto llamado 'lab_matrix'")