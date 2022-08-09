import pygame
from sys import exit
from copy import deepcopy
import settings as s
from board import Board
from numba import njit
import numpy as np


def main():
    global screen, clock
    pygame.init()
    screen = pygame.display.set_mode((s.WINDOWS_WIDTH, s.WINDOWS_HEIGHT))
    pygame.display.set_caption('Game of Life')
    clock = pygame.time.Clock()

    # Initializing board
    board = Board(initial_pattern='5')
    # draw_grid()
    for y in range(board.y_dim):
        for x in range(board.x_dim):
            draw_block(state=board.matrix[y][x], position=(x, y))
    pygame.display.update()

    pause = True

    while True:
        # Checking for close button press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print(f'entered pause: {pause}')
                    pause = False if pause else True

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            x = pos[0] // s.BLOCK_SIZE
            y = pos[1] // s.BLOCK_SIZE
            if board.matrix[y][x] == 0:
                board.matrix[y][x] = 1
            else:
                board.matrix[y][x] = 0
            draw_block(state=board.matrix[y][x], position=(x, y))

        # Apply Game of Life's rules
        if not pause:
            changed_positions, board.matrix = update_state(board.matrix, board.aux_matrix, board.x_dim, board.y_dim)
            for x, y in changed_positions:
                draw_block(state=board.matrix[y][x], position=(x, y))
            board.aux_matrix = deepcopy(board.matrix)
        pygame.display.update()
        print(clock.get_fps())
        clock.tick()


def draw_grid() -> None:
    for i in range(0, s.WINDOWS_WIDTH, s.BLOCK_SIZE):
        pygame.draw.line(screen, s.GREY, (0, i), (s.WINDOWS_WIDTH, i), s.GRID_WIDTH)
        pygame.draw.line(screen, s.GREY, (i, 0), (i, s.WINDOWS_HEIGHT), s.GRID_WIDTH)


# todo: write a function to determine the color of the cell based on its previous value
def draw_block(state: int, position: tuple) -> None:
    color = s.BLACK if state == 0 else s.GREEN
    pygame.draw.rect(screen, color, pygame.Rect(position[0] * s.BLOCK_SIZE,
                                                position[1] * s.BLOCK_SIZE,
                                                s.BLOCK_SIZE, s.BLOCK_SIZE))


@njit(fastmath=True)
def update_state(matrix, aux_matrix, x_dim, y_dim) -> tuple:
    changed_positions = []
    for y in range(len(aux_matrix)):
        for x in range(len(aux_matrix[0])):
            total = 0
            for y_neighbour in range(y - 1, y + 2):
                if y_neighbour in [y_dim, -1]:
                    continue
                for x_neighbour in range(x - 1, x + 2):
                    if x_neighbour in [x_dim, -1]:
                        continue
                    total += aux_matrix[y_neighbour][x_neighbour]
            total -= aux_matrix[y][x]
            if not aux_matrix[y][x]:
                if total == 3:
                    matrix[y][x] = 1
                    changed_positions.append((x, y))
            else:
                if total < 2:
                    matrix[y][x] = 0
                    changed_positions.append((x, y))
                elif total >= 4:
                    matrix[y][x] = 0
                    changed_positions.append((x, y))

    return np.array(changed_positions), matrix


if __name__ == '__main__':
    main()
