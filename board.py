import settings as s
from copy import deepcopy
import random
import numpy as np


class Board:
    def __init__(self, initial_pattern='x'):
        self.patterns = ['x', 'plus', 'random', '5']
        self.x_dim = s.WINDOWS_WIDTH // s.BLOCK_SIZE
        self.y_dim = s.WINDOWS_HEIGHT // s.BLOCK_SIZE
        # Allow only whole numbers for x_dim and y_dim
        if (self.x_dim != s.WINDOWS_WIDTH / s.BLOCK_SIZE) or (self.y_dim != s.WINDOWS_HEIGHT / s.BLOCK_SIZE):
            raise ValueError("Invalid block quantity. Change windows and block size ratio.")
        self.matrix = self.initialize_matrix(initial_pattern)
        self.aux_matrix = deepcopy(self.matrix)

    def initialize_matrix(self, initial_pattern: str) -> np.array:
        match initial_pattern:
            case 'x':
                return self.x_pattern()
            case 'plus':
                return self.plus_pattern()
            case 'random':
                return self.random_pattern()
            case '5':
                return self.divisible_5_pattern()
            case _:
                raise ValueError(f"Please choose a valid initial pattern between: {', '.join(self.patterns)}")

    def plus_pattern(self) -> np.array:
        return np.array([[1 if (self.x_dim // 2 == x) or (self.y_dim // 2 == y) else 0 for x in range(self.x_dim)]
                         for y in range(self.y_dim)])

    def x_pattern(self) -> np.array:
        return np.array([[1 if (x == y) or (x == self.x_dim - 1 - y) else 0 for x in range(self.x_dim)]
                         for y in range(self.y_dim)])

    def random_pattern(self) -> np.array:
        return np.array([[random.randint(0, 1) for x in range(self.x_dim)] for y in range(self.y_dim)])

    def null_pattern(self) -> np.array:
        return np.array([[0 for x in range(self.x_dim)] for y in range(self.y_dim)])

    def divisible_5_pattern(self) -> np.array:
        return np.array([[1 if not (x * y) % 5 else 0 for x in range(self.x_dim)] for y in range(self.y_dim)])
