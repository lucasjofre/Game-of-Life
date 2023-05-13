import pygame
import settings as s
from copy import deepcopy
import random
import numpy as np
from PIL import Image

class Board:
    def __init__(self, initial_pattern='x'):
        HOVER = 3
        self.patterns = ['x', 'plus', 'random', '5']
        self.x_dim = s.WINDOWS_WIDTH // s.BLOCK_SIZE
        self.y_dim = s.WINDOWS_HEIGHT // s.BLOCK_SIZE

        if (self.x_dim != s.WINDOWS_WIDTH / s.BLOCK_SIZE) or (self.y_dim != s.WINDOWS_HEIGHT / s.BLOCK_SIZE):
            raise ValueError("Invalid block quantity. Change windows and block size ratio.")

        self.initialize_matrix(initial_pattern)
        self.aux_matrix = deepcopy(self.matrix)

    def initialize_matrix(self, initial_pattern: str):
        match initial_pattern:
            case 'x':
                self.matrix = self.x_pattern()
            case 'plus':
                self.matrix = self.plus_pattern()
            case 'random':
                self.matrix = self.random_pattern()
            case '5':
                self.matrix = self.divisible_5_pattern()
            case _:
                raise ValueError(f"Please choose a valid initial pattern between: {', '.join(self.patterns)}")
    
    def initialize_from_image(self, image, x_offset=0, y_offset=0):
        img = image.convert('L')  # Convert image to grayscale
        self.start_button_initial_cells = []
        for y in range(img.height):
            for x in range(img.width):
                if y + y_offset < self.y_dim and x + x_offset < self.x_dim:  # Check if the index is within the array bounds
                    if img.getpixel((x, y)) < 128:  # If the pixel is more black than white
                        self.matrix[y + y_offset][x + x_offset] = 2  # Set the cell to alive and immortal
                        if x_offset != 0 and y_offset != 0:  # This is the start button
                            self.start_button_initial_cells.append((x + x_offset, y + y_offset))
                    else:
                        if random.random() < 0:  # 20% chance for a cell to be alive
                            self.matrix[y + y_offset][x + x_offset] = 1


    def immortal_to_normal(self, column):
        self.matrix[:, column][self.matrix[:, column] == 2] = 1

    def change_pattern(self, pattern: str):
        self.clear_board()
        self.initialize_matrix(pattern)
        self.aux_matrix = deepcopy(self.matrix)
    
    def clear_board(self):
        self.matrix = self.null_pattern()
        self.aux_matrix = deepcopy(self.matrix)

    def x_pattern(self):
        return np.array([[1 if (x == y) or (x == self.x_dim - 1 - y) else 0 for x in range(self.x_dim)] for y in range(self.y_dim)])

    def plus_pattern(self):
        return np.array([[1 if (self.x_dim // 2 == x) or (self.y_dim // 2 == y) else 0 for x in range(self.x_dim)] for y in range(self.y_dim)])

    def random_pattern(self):
        return np.array([[random.randint(0, 1) for x in range(self.x_dim)] for y in range(self.y_dim)])

    def null_pattern(self):
        return np.array([[0 for x in range(self.x_dim)] for y in range(self.y_dim)])

    def divisible_5_pattern(self):
        return np.array([[1 if not (x * y) % 5 else 0 for x in range(self.x_dim)] for y in range(self.y_dim)])

    def get_neighbour_total(self, x, y):
        total = 0
        for y_neighbour in range(y - 1, y + 2):
            if y_neighbour < 0 or y_neighbour >= self.y_dim:
                continue
            for x_neighbour in range(x - 1, x + 2):
                if x_neighbour < 0 or x_neighbour >= self.x_dim or (x_neighbour == x and y_neighbour == y):
                    continue
                total += self.aux_matrix[y_neighbour][x_neighbour]
        return total

    def update_state(self):
        self.aux_matrix = deepcopy(self.matrix)
        new_matrix = deepcopy(self.matrix)
        changed_positions = []
        for y in range(self.y_dim):
            for x in range(self.x_dim):
                if self.matrix[y][x] == 2:  # Skip immortal cells
                    continue
                total = self.get_neighbour_total(x, y)
                if self.matrix[y][x] == 1 and (total < 2 or total > 3):
                    new_matrix[y][x] = 0
                    changed_positions.append((x, y))
                elif self.matrix[y][x] == 0 and total == 3:
                    new_matrix[y][x] = 1
                    changed_positions.append((x, y))
        self.matrix = new_matrix
        return changed_positions



    def toggle_cell(self, x, y):
        self.matrix[y][x] = 0 if self.matrix[y][x] == 1 else 1
