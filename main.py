import pygame
from sys import exit
import numpy

BLACK = (0, 0, 0)
GREY = (150, 150, 150)
WHITE = (255, 255, 255)

WINDOWS_HEIGHT = 400
WINDOWS_WIDTH = 800

BLOCK_SIZE = 10
GRID_WIDTH = 1


class Block:
    def __init__(self, color: tuple, state: int, position: tuple) -> None:
        self.color = color
        self.state = state
        self.position = position

    def draw_block(self) -> None:
        pygame.draw.rect(screen, self.color, pygame.Rect(self.position[0] * BLOCK_SIZE, self.position[1] * BLOCK_SIZE,
                                                         BLOCK_SIZE - GRID_WIDTH, BLOCK_SIZE - GRID_WIDTH))


def main():
    global screen, clock
    pygame.init()
    screen = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))
    pygame.display.set_caption('Game of Life')
    clock = pygame.time.Clock()
    draw_grid()

    while True:
        board = initialize_matrix()

        # Checking for close button press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # todo: implement draw_block method
        for x in board:
            for y in x:
                pygame.draw.rect(screen, WHITE, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE,
                                                            BLOCK_SIZE - GRID_WIDTH, BLOCK_SIZE - GRID_WIDTH))

        pygame.display.update()
        clock.tick(60)


def draw_grid():
    for i in range(0, WINDOWS_WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GREY, (0, i), (900, i), GRID_WIDTH)
        pygame.draw.line(screen, GREY, (i, 0), (i, 900), GRID_WIDTH)


def initialize_matrix():
    return numpy.zeros((WINDOWS_WIDTH // BLOCK_SIZE, WINDOWS_HEIGHT // BLOCK_SIZE))


if __name__ == '__main__':
    main()
