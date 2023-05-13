import pygame
from sys import exit
import settings as s
from scene import MainMenuScene

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((s.WINDOWS_WIDTH, s.WINDOWS_HEIGHT))
        pygame.display.set_caption('Game of Life')
        self.clock = pygame.time.Clock()
        self.current_scene = MainMenuScene(self)

    def change_scene(self, scene):
        self.current_scene = scene

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.current_scene.get_fps())
            print("FPS: ", self.clock.get_fps())

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            else:
                self.current_scene.handle_events(event)

    def update(self):
        self.current_scene.update()

    def draw(self):
        self.current_scene.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
