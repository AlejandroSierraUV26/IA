# board.py

class Board:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = [[None for _ in range(columns)] for _ in range(rows)]
    
    def add_mouse(self, mouse):
        self.grid[mouse.position[0]][mouse.position[1]] = 'M'
    
    def add_cheese(self, cheese):
        self.grid[cheese.position[0]][cheese.position[1]] = 'C'
