import pygame
from sys import exit
import random
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
