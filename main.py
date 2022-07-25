import pygame
from sys import exit
import random
from copy import deepcopy

BLACK = (0, 0, 0)
GREY = (150, 150, 150)
WHITE = (255, 255, 255)

WINDOWS_HEIGHT = 500
WINDOWS_WIDTH = 1000

BLOCK_SIZE = 10
GRID_WIDTH = 1


class Block:
    def __init__(self, state: int) -> None:
        self.state = state
        self._color = BLACK

    def draw_block(self, position: tuple) -> None:
        self._change_color()
        pygame.draw.rect(screen, self._color, pygame.Rect(position[0] * BLOCK_SIZE + GRID_WIDTH,
                                                          position[1] * BLOCK_SIZE + GRID_WIDTH,
                                                          BLOCK_SIZE - GRID_WIDTH, BLOCK_SIZE - GRID_WIDTH))

    def _change_color(self):
        self._color = BLACK if self.state == 0 else WHITE


class Board:
    def __init__(self):
        self.x_dim = WINDOWS_WIDTH // BLOCK_SIZE
        self.y_dim = WINDOWS_HEIGHT // BLOCK_SIZE
        # Allow only whole numbers for x_dim and y_dim
        if (self.x_dim != WINDOWS_WIDTH / BLOCK_SIZE) or (self.y_dim != WINDOWS_HEIGHT / BLOCK_SIZE):
            raise ValueError("Invalid block quantity. Change windows and block size ratio.")
        self.matrix = self.initialize_matrix()
        self.aux_matrix = deepcopy(self.matrix)

    def initialize_matrix(self) -> list:
        return [[Block(state=random.randint(0, 1)) for _ in range(self.x_dim)] for _ in
                range(self.y_dim)]

    @staticmethod
    def draw_grid() -> None:
        for i in range(0, WINDOWS_WIDTH, BLOCK_SIZE):
            pygame.draw.line(screen, GREY, (0, i), (WINDOWS_WIDTH, i), GRID_WIDTH)
            pygame.draw.line(screen, GREY, (i, 0), (i, WINDOWS_HEIGHT), GRID_WIDTH)

    def get_alive_neighbours(self, x: int, y: int) -> int:
        total = 0
        for y_neighbour in range(y - 1, y + 2):
            for x_neighbour in range(x - 1, x + 2):
                try:
                    total += self.matrix[y_neighbour][x_neighbour].state
                except IndexError as e:
                    continue
                # if ((x_neighbour, y_neighbour) == (x, y) or
                #         x_neighbour == self.x_dim - 1 or
                #         y_neighbour == self.y_dim - 1 or
                #         x_neighbour == 0 or
                #         y_neighbour == 0):
                #     continue
        total -= self.matrix[y][x].state
        return total


def main():
    global screen, clock
    pygame.init()
    screen = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))
    pygame.display.set_caption('Game of Life')
    clock = pygame.time.Clock()

    # Initializing board
    board = Board()
    board.draw_grid()

    pause_flag = False

    while True:
        # Checking for close button press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x = pos[0] // BLOCK_SIZE
                y = pos[1] // BLOCK_SIZE
                if board.matrix[y][x].state == 0:
                    board.matrix[y][x].state = 1
                else:
                    board.matrix[y][x].state = 0
                board.matrix[y][x].draw_block(position=(x, y))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print(f'entered pause: {pause_flag}')
                    pause_flag = False if pause_flag else True

        # Apply Game of Life's rules
        if not pause_flag:
            for y, line in enumerate(board.aux_matrix):
                for x, item in enumerate(line):
                    alive_neighbours = board.get_alive_neighbours(x, y)
                    if item.state == 0:
                        if alive_neighbours == 3:
                            board.matrix[y][x].state = 1
                    else:
                        if alive_neighbours < 2:
                            board.matrix[y][x].state = 0
                        elif alive_neighbours >= 4:
                            board.matrix[y][x].state = 0
                    item.draw_block(position=(x, y))

        board.aux_matrix = deepcopy(board.matrix)
        pygame.display.update()
        clock.tick(60)


# todo: create an update display funtion, i dont need  to only update at the end of the loop

if __name__ == '__main__':
    main()
