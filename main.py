import pygame
from sys import exit

BLACK = (0, 0, 0)
GREY = (150, 150, 150)
WHITE = (255, 255, 255)

WINDOWS_HEIGHT = 400
WINDOWS_WIDTH = 800

BLOCK_SIZE = 10
GRID_WIDTH = 1


class Block:
    def __init__(self, color: tuple, state: int) -> None:
        self.color = color
        self.state = state

    def draw_block(self, position: tuple) -> None:
        pygame.draw.rect(screen, self.color, pygame.Rect(position[0] * BLOCK_SIZE + GRID_WIDTH,
                                                         position[1] * BLOCK_SIZE + GRID_WIDTH,
                                                         BLOCK_SIZE - GRID_WIDTH, BLOCK_SIZE - GRID_WIDTH))


class Board:
    def __init__(self):
        self.x_dim = WINDOWS_WIDTH // BLOCK_SIZE
        self.y_dim = WINDOWS_HEIGHT // BLOCK_SIZE
        # Allow only whole numbers for x_dim and y_dim
        if (self.x_dim != WINDOWS_WIDTH / BLOCK_SIZE) or (self.y_dim != WINDOWS_HEIGHT / BLOCK_SIZE):
            raise ValueError("Invalid block quantity. Change windows and block size ratio.")
        self.matrix = self.initialize_matrix()
        self.aux_matrix = self.matrix

    def initialize_matrix(self) -> list:
        return [[Block(color=BLACK, state=0) for x in range(self.x_dim)] for y in range(self.y_dim)]

    @staticmethod
    def draw_grid() -> None:
        for i in range(0, WINDOWS_WIDTH, BLOCK_SIZE):
            pygame.draw.line(screen, GREY, (0, i), (900, i), GRID_WIDTH)
            pygame.draw.line(screen, GREY, (i, 0), (i, 900), GRID_WIDTH)

    def get_alive_neighbours(self, x: int, y: int) -> int:
        total = 0
        for y_neighbour in range(y - 1, y + 2):
            for x_neighbour in range(x - 1, x + 2):
                try:
                    total += self.matrix[y_neighbour][x_neighbour].state
                except IndexError as e:
                    continue
                # if ((x_neighbour, y_neighbour) == (x, y) or
                #         x_neighbour == self.x_dim - 2 or
                #         y_neighbour == self.y_dim - 2 or
                #         x_neighbour == 0 or
                #         y_neighbour == 0):
                #    continue
                #total += self.matrix[y_neighbour][x_neighbour].state
        return total


def main():
    global screen, clock
    pygame.init()
    screen = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))
    pygame.display.set_caption('Game of Life')
    clock = pygame.time.Clock()

    # Initializing board
    board = Board()
    board.initialize_matrix()
    board.draw_grid()

    while True:
        # Checking for close button press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     pos = pygame.mouse.get_pos()
            #     x = pos[0] // BLOCK_SIZE
            #     y = pos[1] // BLOCK_SIZE
            #     if board.matrix[y][x].state == 0:
            #         board.matrix[y][x].state = 1
            #         board.matrix[y][x].color = WHITE
            #     else:
            #         board.matrix[y][x].state = 0
            #         board.matrix[y][x].color = BLACK

        # Apply Game of Life's rules
        for y, line in enumerate(board.aux_matrix):
            for x, item in enumerate(line):
                alive_neighbours = board.get_alive_neighbours(x, y)
                if item.state == 0:
                    if alive_neighbours == 0:
                        board.matrix[y][x].state = 1
                        board.matrix[y][x].color = WHITE
                else:
                    if alive_neighbours < 2:
                        board.matrix[y][x].state = 0
                        board.matrix[y][x].color = BLACK
                    elif 2 <= alive_neighbours <= 3:
                        continue
                    else:
                        board.matrix[y][x].state = 0
                        board.matrix[y][x].color = BLACK
                item.draw_block(position=(x, y))

        board.aux_matrix = board.matrix
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
