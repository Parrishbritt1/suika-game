import pygame
import math
from grid import Grid


GRAVITY = 0.2
BOUNCE_STOP = 0.5

RED = (255, 0, 0)
GREEN = (0, 255, 0)

XBOUND = 640
YBOUND = 800

class Fruit:
    def __init__(self, x, y, radius, color=RED):
        self.x, self.y = x, y
        self.radius = radius
        self.color = color
        self.mass = 1
        self.retention = 0.5
        self.x_speed = 0
        self.y_speed = 0
        self.is_dropped = False
        self.current_overlapping_cells = set()

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def apply_gravity(self):
        self.y_speed += GRAVITY

    def update(self, grid:Grid):
        self.apply_gravity()
        self.update_position()
        # Update overlapping cells
        new_overlapping_cells = grid.get_cell_indices(self.x, self.y, self.radius)
        cells_to_remove_this_from = set.difference(self.current_overlapping_cells, new_overlapping_cells)
        cells_to_add_this_to = set.difference(new_overlapping_cells, self.current_overlapping_cells)
        for cell in cells_to_remove_this_from:
            grid.remove_obj_from_cell(self, cell)
        for cell in cells_to_add_this_to:
            grid.add_obj_to_cell(self, cell)
        self.current_overlapping_cells = new_overlapping_cells
        self.check_collision(grid)
        self.check_wall_collision()
    
    def update_position(self):
        self.x += self.x_speed
        self.y += self.y_speed

    def check_collision(self, grid):
        for cell in self.current_overlapping_cells:
            row, col = cell
            for other_fruit in grid.cells[row][col]:
                if other_fruit != self:
                    distance = math.sqrt((self.x - other_fruit.x)**2 + (self.y - other_fruit.y)**2)
                    if distance < self.radius + other_fruit.radius:
                        normal_x = (other_fruit.x - self.x) / distance
                        normal_y = (other_fruit.y - self.y) / distance

                        relative_velocity_x = other_fruit.x_speed - self.x_speed
                        relative_velocity_y = other_fruit.y_speed - self.y_speed
                        dot_product = (relative_velocity_x * normal_x) + (relative_velocity_y * normal_y)

                        if dot_product < 0:
                            overlap = self.radius + other_fruit.radius - distance
                            separation_x = overlap * normal_x
                            separation_y = overlap * normal_y

                            # Separate the circles entirely along the collision normal
                            self.x -= separation_x * .5
                            self.y -= separation_y * .5
                            other_fruit.x += separation_x * .5
                            other_fruit.y += separation_y * .5

                            # Rest of the collision resolution remains unchanged
                            impulse_magnitude = min(0.8 * (-dot_product / (self.mass + other_fruit.mass)), 1.0)
                            impulse_x = impulse_magnitude * normal_x
                            impulse_y = impulse_magnitude * normal_y

                            self.x_speed -= impulse_x * other_fruit.mass
                            self.y_speed -= impulse_y * other_fruit.mass
                            other_fruit.x_speed += impulse_x * self.mass
                            other_fruit.y_speed += impulse_y * self.mass

    def check_wall_collision(self):
        if self.x + self.radius >= XBOUND:
            self.x = XBOUND - self.radius
            self.x_speed = -abs(self.x_speed) * self.retention
        elif self.x - self.radius <= 0:
            self.x = self.radius
            self.x_speed = abs(self.x_speed) * self.retention

        if self.y + self.radius >= YBOUND:
            self.y = YBOUND - self.radius
            self.y_speed = -abs(self.y_speed) * self.retention
        elif self.y - self.radius <= 0:
            self.y = self.radius
            self.y_speed = abs(self.y_speed) * self.retention
