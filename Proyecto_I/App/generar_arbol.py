import networkx as nx
import pygame
import sys


"""

Fecha : 2024-09-06
Autor : Alejandro Sierra 
Tema : Generar un árbol jerárquico con NetworkX y visualizarlo con Pygame

Version : 1.0

"""
# Crear un árbol con 10 nodos (2 hijos por nodo, 4 niveles de profundidad)
profundidad_arbol = 4
ancho_arbol = 2

G = nx.balanced_tree(ancho_arbol, profundidad_arbol)

# Inicializar pygame
pygame.init()
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Tree Visualization")

# Crear posiciones manualmente para un árbol jerárquico
def hierarchical_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    if root is None:
        root = next(iter(G.nodes()))  # Tomar el primer nodo como raíz si no se especifica
    pos = _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
    return pos

def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None):
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    
    children = list(G.neighbors(root))
    if parent is not None:  # Evitar volver al nodo padre
        children.remove(parent)
    
    if len(children) != 0:
        dx = width / len(children)  # Espaciado horizontal entre nodos
        nextx = xcenter - width / 2 - dx / 2
        for child in children:
            nextx += dx
            pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos, parent=root)
    
    return pos

# Obtener posiciones jerárquicas
pos = hierarchical_pos(G)

# Ajustar escala y offset para centrar el árbol en la pantalla
def calculate_scale_and_offset(pos, screen_width, screen_height, margin=50):
    # Encuentra los límites del árbol
    x_values = [p[0] for p in pos.values()]
    y_values = [p[1] for p in pos.values()]
    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)

    # Calcular escala
    tree_width = x_max - x_min
    tree_height = y_max - y_min
    scale_x = (screen_width - 2 * margin) / tree_width
    scale_y = (screen_height - 2 * margin) / tree_height
    scale = min(scale_x, scale_y)  # Usa la escala mínima para ajustar el árbol al tamaño de la pantalla

    # Calcular offset para centrar el árbol
    offset_x = (screen_width - (tree_width * scale)) / 2 - (x_min * scale)
    offset_y = (screen_height - (tree_height * scale)) / 2 - (y_max * scale)

    return scale, (offset_x, offset_y)

# Obtener la escala y el offset
scale, offset = calculate_scale_and_offset(pos, screen.get_width(), screen.get_height())

# Función para convertir las posiciones del layout a coordenadas de pygame
def convert_position(pos, scale, offset):
    return int(pos[0] * scale + offset[0]), int(offset[1] - pos[1] * scale)

# Dibujar el botón de detener
def draw_button(screen):
    font = pygame.font.SysFont(None, 30)
    pygame.draw.rect(screen, (255, 0, 0), (200, 450, 100, 40))  # Botón rojo
    text = font.render("Detener", True, (255, 255, 255))
    screen.blit(text, (210, 455))  # Posición del texto en el botón

# Verificar si el botón de detener ha sido presionado
def button_pressed(pos):
    x, y = pos
    if 200 <= x <= 300 and 450 <= y <= 490:  # Coordenadas del botón
        return True
    return False

# Dibujar el árbol nodo por nodo con un delay
def draw_tree_incremental(screen, G, pos, scale, offset):
    nodes = list(G.nodes())  # Lista de nodos en el árbol
    edges = list(G.edges())  # Lista de aristas en el árbol

    for i in range(len(nodes)):
        # Limpiar la pantalla
        screen.fill((255, 255, 255))



        # Dibujar aristas
        for edge in edges[:i]:  # Dibujar solo las aristas correspondientes a los nodos que ya están dibujados
            node1_pos = convert_position(pos[edge[0]], scale, offset)
            node2_pos = convert_position(pos[edge[1]], scale, offset)
            pygame.draw.line(screen, (0, 0, 0), node1_pos, node2_pos, 3)

        # Dibujar nodos
        for node in nodes[:i + 1]:  # Dibujar solo los nodos hasta el nodo actual
            node_pos = convert_position(pos[node], scale, offset)
            if node == nodes[i]:
                pygame.draw.circle(screen, (239, 35, 60), node_pos, 20)
            else:
                # Dibujar un lado azul y el otro verde
                if node % 2 == 0:
                    pygame.draw.circle(screen, (13, 27, 42), node_pos, 20)  # Círculos negro para los nodos
                else:
                    pygame.draw.circle(screen, (141, 153, 174), node_pos, 20)  # Círculos gris para los nodos
            font = pygame.font.SysFont(None, 24)
            text = font.render(str(node), True, (255, 255, 255))
            screen.blit(text, (node_pos[0] - 10, node_pos[1] - 10))  # Etiquetas de los nodos

        # Actualizar la pantalla
        pygame.display.flip()

        # Esperar un segundo antes de agregar el siguiente nodo
        pygame.time.delay(1000)

        # Comprobar si el botón fue presionado
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_pressed(event.pos):
                    return  # Detener el dibujo si se presiona el botón

# Dibujar el árbol nodo por nodo y luego mantener el árbol estático
def main_loop():
    draw_tree_incremental(screen, G, pos, scale, offset)  # Dibuja el árbol nodo por nodo

    # Mantener el árbol estático y manejar eventos
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_pressed(event.pos):
                    pygame.quit()
                    sys.exit()

main_loop()

# Salir de pygame
pygame.quit()
