import pygame
from sys import exit
from copy import deepcopy
import settings as s
from board import Board
from block import Block


def main():
    global screen, clock
    pygame.init()
    screen = pygame.display.set_mode((s.WINDOWS_WIDTH, s.WINDOWS_HEIGHT))
    pygame.display.set_caption('Game of Life')
    clock = pygame.time.Clock()

    # Initializing board
    board = Board()
    draw_grid()

    pause_flag = False

    while True:
        # Checking for close button press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print(f'entered pause: {pause_flag}')
                    pause_flag = False if pause_flag else True

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            x = pos[0] // s.BLOCK_SIZE
            y = pos[1] // s.BLOCK_SIZE
            if board.matrix[y][x].state == 0:
                board.matrix[y][x].state = 1
            else:
                board.matrix[y][x].state = 0
            draw_block(block=board.matrix[y][x], position=(x, y))

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
                    draw_block(block=board.matrix[y][x], position=(x, y))

        board.aux_matrix = deepcopy(board.matrix)
        pygame.display.update()
        clock.tick(20)


def draw_grid() -> None:
    for i in range(0, s.WINDOWS_WIDTH, s.BLOCK_SIZE):
        pygame.draw.line(screen, s.GREY, (0, i), (s.WINDOWS_WIDTH, i), s.GRID_WIDTH)
        pygame.draw.line(screen, s.GREY, (i, 0), (i, s.WINDOWS_HEIGHT), s.GRID_WIDTH)


def draw_block(block: Block, position: tuple) -> None:
    pygame.draw.rect(screen, block.color, pygame.Rect(position[0] * s.BLOCK_SIZE + s.GRID_WIDTH,
                                                      position[1] * s.BLOCK_SIZE + s.GRID_WIDTH,
                                                      s.BLOCK_SIZE - s.GRID_WIDTH, s.BLOCK_SIZE - s.GRID_WIDTH))


if __name__ == '__main__':
    main()
