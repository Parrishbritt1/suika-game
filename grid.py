import collections


class Grid:

    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cols = int(width / cell_size)
        self.rows = int(height / cell_size)
        # Each cell has a linked list to store objects
        self.cells = [[collections.deque() 
                       for _ in range(self.cols)] 
                        for _ in range(self.rows)]
        

    def add_obj_to_cell(self, obj):
        col, row = self.get_cell_index(obj.x, obj.y)
        self.cells[row][col].append(obj)


    def remove_obj_from_cell(self, obj):
        col, row = self.get_cell_index(obj.x, obj.y)
        self.cells[row][col].remove(obj)
        

    def get_cell_index(self, x, y):
        col = int(x / self.cell_size)
        row = int(y / self.cell_size)
        col = max(0, min(col, self.cols - 1))
        row = max(0, min(row, self.rows - 1))
        return col, row

