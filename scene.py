# scene.py
import pygame
from button import Button
from board import Board
import settings as s

class Scene:
    def __init__(self, game):
        self.game = game
        self.fps = 60  # default FPS

    def get_fps(self):
        return self.fps

    def handle_events(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass


class MainMenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.fps = 10
        self.start_button = Button(200, 200, 200, 100, 'Start', function=self.start_game)
        # Initialize the board with the "Game of Life" pattern
        self.board = Board()
        self.board.clear_board()
        self.board.initialize_from_image('game_of_life.png')
        self.start_time = pygame.time.get_ticks()

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.is_over(event.pos):
                self.start_button.click()

    def update(self):
        # After 5 seconds, start applying the rules
        if pygame.time.get_ticks() - self.start_time > 3000:
            self.board.update_state()

    def draw(self):
        # Draw the board
        for y in range(self.board.y_dim):
            for x in range(self.board.x_dim):
                color = s.BLACK if self.board.matrix[y][x] == 0 else s.GREEN
                pygame.draw.rect(self.game.screen, color, pygame.Rect(x * s.BLOCK_SIZE, y * s.BLOCK_SIZE, s.BLOCK_SIZE, s.BLOCK_SIZE))
        # Draw the button
        self.start_button.draw(self.game.screen)

    def start_game(self):
        self.game.change_scene(GameScene(self.game))


class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.board = Board()
        self.pause = True
        self.mouse_down = False
        self.last_cell = None
        self.mode = 'paint'

        self.buttons = [
            Button(20, 20, 100, 50, 'X Pattern', function=self.board.change_pattern, params=('x',)),
            Button(140, 20, 100, 50, 'Plus Pattern', function=self.board.change_pattern, params=('plus',)),
            Button(260, 20, 100, 50, 'Random Pattern', function=self.board.change_pattern, params=('random',)),
            Button(380, 20, 100, 50, '5 Pattern', function=self.board.change_pattern, params=('5',))
        ]
        self.draw_board()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mousebuttondown(event.button, event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_mousebuttonup(event.button)
        elif event.type == pygame.MOUSEMOTION:
            self.handle_mousemotion(event.pos)

        self.update_buttons()

    def update(self):
        if not self.pause:
            self.update_board()

    def draw(self):
        self.draw_board()
        for button in self.buttons:
            button.draw(self.game.screen)

    def quit_game(self):
            pygame.quit()
            exit()

    def handle_keydown(self, key):
        if key == pygame.K_SPACE:
            self.pause = not self.pause
            print(f"Game pause state: {self.pause}")
        elif key == pygame.K_p:  # Press 'p' to switch to 'paint' mode
            self.mode = 'paint'
        elif key == pygame.K_e:  # Press 'e' to switch to 'erase' mode
            self.mode = 'erase'

    def handle_mousebuttondown(self, button, pos):
        if button == 1:  # Left mouse button
            self.mouse_down = True
            self.handle_mouse_click(*pos)
            # Check if a button was clicked
            for button in self.buttons:
                if button.is_over(pos):
                    pattern_changed = button.click()
                    if pattern_changed:  # If the pattern was changed
                        self.pause = True  # Pause the game
                        self.draw_board()  # Redraw the board immediately

    def handle_mousebuttonup(self, button):
        if button == 1:  # Left mouse button
            self.mouse_down = False
            self.last_cell = None  # Reset last cell when the mouse button is released

    def handle_mousemotion(self, pos):
        if self.mouse_down:
            self.handle_mouse_click(*pos)

    def update_buttons(self):
        for button in self.buttons:
            if button.is_over(pygame.mouse.get_pos()):
                button.color = s.LIGHT_GREY
            else:
                button.color = s.GREY
            button.draw(self.game.screen)

    def handle_mouse_click(self, x, y):
        cell_x, cell_y = x // s.BLOCK_SIZE, y // s.BLOCK_SIZE
        if 0 <= cell_x < self.board.x_dim and 0 <= cell_y < self.board.y_dim:
            if self.mode == 'paint' and self.board.matrix[cell_y][cell_x] == 0:  # Only paint dead cells
                self.board.toggle_cell(cell_x, cell_y)
                self.draw_block(self.board.matrix[cell_y][cell_x], (cell_x, cell_y))
            elif self.mode == 'erase' and self.board.matrix[cell_y][cell_x] == 1:  # Only erase live cells
                self.board.toggle_cell(cell_x, cell_y)
                self.draw_block(self.board.matrix[cell_y][cell_x], (cell_x, cell_y))

    def update_board(self):
        changed_positions = self.board.update_state()
        print(f"Updating board. Changed positions: {changed_positions}")
        for x, y in changed_positions:
            self.draw_block(self.board.matrix[y][x], (x, y))

    def draw_board(self):
        for y in range(self.board.y_dim):
            for x in range(self.board.x_dim):
                self.draw_block(self.board.matrix[y][x], (x, y))

    def draw_block(self, state, position):
        color = s.BLACK if state == 0 else s.GREEN
        pygame.draw.rect(self.game.screen, color, pygame.Rect(position[0] * s.BLOCK_SIZE,
                                                        position[1] * s.BLOCK_SIZE,
                                                        s.BLOCK_SIZE, s.BLOCK_SIZE))
