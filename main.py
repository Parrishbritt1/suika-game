import pygame
from fruits import Fruit
from grid import Grid
import random


FPS = 60
XBOUND = 640
YBOUND = 800

# HORIZONTAL LINE WHERE FRUITS STAY ABOVE
LINE_Y = 100
LEFT_LINE_COORD = (0, LINE_Y)
RIGHT_LINE_COORD = (XBOUND, LINE_Y)

possible_radii = [15, 25, 35]


def draw_background(screen):
    screen.fill((255,253,208)) # Cream color
    pygame.draw.line(screen, (211, 211, 211), LEFT_LINE_COORD, RIGHT_LINE_COORD, 4)


def main():
    pygame.init()
    window_screen = pygame.display.set_mode((XBOUND, YBOUND))
    pygame.event.set_grab(True) # Lock mouse into window
    clock = pygame.time.Clock()
    running = True

    # Create first fruit
    fruits = []
    current_fruit = Fruit(0, 0, random.choice(possible_radii))
    fruits.append(current_fruit)

    # Init grid for spatial partitioning
    grid = Grid(XBOUND, YBOUND - LINE_Y, 50)

    while running:
        clock.tick(FPS)
        draw_background(window_screen)

        # FRUIT DRAW LOGIC
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # print(grid.get_cell_indices(mouse_x, mouse_y-LINE_Y, 25))

        for fruit in fruits:
            if fruit.is_dropped:
                fruit.update(grid)
            else:
                # Ensure fruit doesn't go past screen boundaries
                if (mouse_x - fruit.radius) < 0: # LEFT BOUND
                    fruit.x, fruit.y = fruit.radius, (LINE_Y / 2)
                elif (mouse_x + fruit.radius) > XBOUND: # RIGHT BOUND
                    fruit.x, fruit.y = (XBOUND - fruit.radius), LINE_Y/2
                else:
                    fruit.x, fruit.y = mouse_x, (LINE_Y / 2)

            fruit.draw(window_screen)
            
        print(len(fruits))

        # KEY EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # ONLY WAY TO EXIT IS ESC
                    running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # Left click only
                    # Pick another fruit
                    current_fruit.is_dropped = True
                    current_fruit = Fruit(0, 0, random.choice(possible_radii))
                    fruits.append(current_fruit)

        pygame.display.flip()


if __name__ == "__main__":
    main()