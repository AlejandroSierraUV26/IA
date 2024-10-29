# search_algorithms.py

class SearchAlgorithm:
    def __init__(self, board, mouse, cheese):
        self.board = board
        self.mouse = mouse
        self.cheese = cheese
    
    def run(self):
        raise NotImplementedError("Este método debe ser implementado en las subclases")

class UninformedSearch(SearchAlgorithm):
    def __init__(self, board, mouse, cheese, strategy):
        super().__init__(board, mouse, cheese)
        self.strategy = strategy
    
    def run(self):
        # Implementación específica de cada búsqueda no informada
        pass

class GreedySearch(SearchAlgorithm):
    def run(self):
        # Implementación de la búsqueda Avara
        pass
