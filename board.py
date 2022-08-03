import settings as s
from copy import deepcopy
import random
from block import Block
import pygame


class Board:
    def __init__(self):
        self.x_dim = s.WINDOWS_WIDTH // s.BLOCK_SIZE
        self.y_dim = s.WINDOWS_HEIGHT // s.BLOCK_SIZE
        # Allow only whole numbers for x_dim and y_dim
        if (self.x_dim != s.WINDOWS_WIDTH / s.BLOCK_SIZE) or (self.y_dim != s.WINDOWS_HEIGHT / s.BLOCK_SIZE):
            raise ValueError("Invalid block quantity. Change windows and block size ratio.")
        self.matrix = self.initialize_matrix()
        self.aux_matrix = deepcopy(self.matrix)

    def initialize_matrix(self) -> list:
        return [[Block(state=random.randint(0, 1)) for _ in range(self.x_dim)] for _ in
                range(self.y_dim)]

    def get_alive_neighbours(self, x: int, y: int) -> int:
        total = 0
        for y_neighbour in range(y - 1, y + 2):
            for x_neighbour in range(x - 1, x + 2):
                try:
                    total += self.aux_matrix[y_neighbour][x_neighbour].state
                except IndexError as e:
                    continue
                # if ((x_neighbour, y_neighbour) == (x, y) or
                #         x_neighbour == self.x_dim - 1 or
                #         y_neighbour == self.y_dim - 1 or
                #         x_neighbour == 0 or
                #         y_neighbour == 0):
                #     continue
        total -= self.aux_matrix[y][x].state
        return total
