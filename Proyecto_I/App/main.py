# main.py

from board import Board
from mouse import Mouse
from cheese import Cheese
from search_algorithms import UninformedSearch, GreedySearch
from visualizer import Visualizer

def main():
    # Configuración inicial
    board = Board(rows=5, columns=5)  # Dimensiones de ejemplo
    mouse = Mouse(start_position=(0, 0))
    cheese = Cheese(position=(4, 4))
    
    # Inicializar visualización
    visualizer = Visualizer(board, mouse, cheese)
    
    # Configurar y ejecutar algoritmos de búsqueda
    algorithms = [UninformedSearch(board, mouse, cheese, strategy=i) for i in range(5)]
    greedy_search = GreedySearch(board, mouse, cheese)
    
    # Ejecución de los algoritmos
    for algorithm in algorithms:
        algorithm.run()
        visualizer.update(algorithm)
    
    # Visualización del proceso
    visualizer.display()

if __name__ == "__main__":
    main()
