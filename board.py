import settings as s
from copy import deepcopy
import random
from block import Block


class Board:
    def __init__(self, initial_pattern='x'):
        self.x_dim = s.WINDOWS_WIDTH // s.BLOCK_SIZE
        self.y_dim = s.WINDOWS_HEIGHT // s.BLOCK_SIZE
        # Allow only whole numbers for x_dim and y_dim
        if (self.x_dim != s.WINDOWS_WIDTH / s.BLOCK_SIZE) or (self.y_dim != s.WINDOWS_HEIGHT / s.BLOCK_SIZE):
            raise ValueError("Invalid block quantity. Change windows and block size ratio.")
        self.matrix = self.initialize_matrix(initial_pattern)
        self.aux_matrix = deepcopy(self.matrix)

    def initialize_matrix(self, initial_pattern) -> list:
        if initial_pattern not in ['x', 'plus', 'random', 'null']:
            raise ValueError('Please choose a valid initial pattern')
        elif initial_pattern == 'x':
            return self.x_pattern()
        elif initial_pattern == 'plus':
            return self.plus_pattern()
        elif initial_pattern == 'random':
            return self.random_pattern()
        elif initial_pattern == 'null':
            return self.null_pattern()

    def get_alive_neighbours(self, x: int, y: int) -> int:
        total = 0
        for y_neighbour in range(y - 1, y + 2):
            if y_neighbour in [self.y_dim, -1]:
                continue
            for x_neighbour in range(x - 1, x + 2):
                if x_neighbour in [self.x_dim, -1]:
                    continue
                total += self.aux_matrix[y_neighbour][x_neighbour].state
        total -= self.aux_matrix[y][x].state
        return total

    def plus_pattern(self):
        matrix = []
        for y in range(self.y_dim):
            row = []
            for x in range(self.x_dim):
                if (self.x_dim // 2 == x) or (self.y_dim // 2 == y):
                    row.append(Block(state=1))
                else:
                    row.append(Block(state=0))
            matrix.append(row)
        return matrix

    def x_pattern(self):
        matrix = []
        for y in range(self.y_dim):
            row = []
            for x in range(self.x_dim):
                if (x == y) or (x == self.x_dim - 1 - y):
                    row.append(Block(state=1))
                else:
                    row.append(Block(state=0))
            matrix.append(row)
        return matrix

    def random_pattern(self):
        return [[Block(state=random.randint(0, 1)) for x in range(self.x_dim)] for y in range(self.y_dim)]

    def null_pattern(self):
        return [[Block(state=0) for x in range(self.x_dim)] for y in range(self.y_dim)]

