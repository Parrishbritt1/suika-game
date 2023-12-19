import collections
import math


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
        

    def add_obj_to_cell(self, obj, cell):
        row, col = cell
        self.cells[row][col].append(obj)
        return row, col

    def remove_obj_from_cell(self, obj, cell):
        row, col = cell
        self.cells[row][col].remove(obj)
        return row, col
    

    def get_cell_index(self, x, y):
        row = int(y / self.cell_size)
        row = max(0, min(row, self.rows - 1))
        col = int(x / self.cell_size)
        col = max(0, min(col, self.cols - 1))
        return row, col
        

    def get_cell_indices(self, x, y, radius):
        '''
        Gets the cell index where (x, y) is located on the grid
        '''
        output = set()

        # Center of circle
        row, col = self.get_cell_index(x, y)
        output.add((row, col))

        # Top of circle
        row, col = self.get_cell_index(x, (y - radius))
        output.add((row, col))

        # Bottom of circle
        row, col = self.get_cell_index(x, (y + radius))
        output.add((row, col))

        # Right of circle
        row, col = self.get_cell_index((x + radius), y)
        output.add((row, col))

        # Left of circle
        row, col = self.get_cell_index((x - radius), y)
        output.add((row, col))

        # Diagonals of circle (45 degrees)
        top_right_x = x + radius * math.cos(math.pi / 4)
        top_right_y = y + radius * math.sin(math.pi / 4)
        row, col = self.get_cell_index(top_right_x, top_right_y)
        output.add((row, col))

        top_left_x = x + radius * math.cos((3 * math.pi) / 4)
        top_left_y = y + radius * math.sin((3 * math.pi) / 4)
        row, col = self.get_cell_index(top_left_x, top_left_y)
        output.add((row, col))

        bottom_left_x = x + radius * math.cos((5 * math.pi) / 4)
        bottom_left_y = y + radius * math.sin((5 * math.pi) / 4)
        row, col = self.get_cell_index(bottom_left_x, bottom_left_y)
        output.add((row, col))

        bottom_right_x = x + radius * math.cos((7 * math.pi) / 4)
        bottom_right_y = y + radius * math.sin((7 * math.pi) / 4)
        row, col = self.get_cell_index(bottom_right_x, bottom_right_y)
        output.add((row, col))

        return output
