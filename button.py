import pygame
import settings as s

class Button:
    def __init__(self, x, y, width, height, text=None, image=None, highlighted_color=s.WHITE, function=None, params=None):
        if image is not None:
            self.image_normal = self.load_and_scale_image(image, (width, height))
            self.image_highlighted = self.create_highlighted_image(self.image_normal, highlighted_color)
        else:
            self.image_normal = pygame.Surface((width, height))
            self.image_highlighted = pygame.Surface((width, height))
            self.image_highlighted.fill(highlighted_color)

        self.image = self.image_normal
        self.rect = self.image.get_rect()

        if text:
            font = pygame.font.Font(None, 20)
            text_image = font.render(text, True, s.BLACK)
            text_rect = text_image.get_rect(center=self.rect.center)
            self.image_normal.blit(text_image, text_rect)
            self.image_highlighted.blit(text_image, text_rect)

        self.rect.topleft = (x, y)

        self.function = function
        self.params = params

    def load_and_scale_image(self, image, size):
        # Convert PIL Image to Pygame Surface
        mode = image.mode
        size = image.size
        data = image.tobytes()

        pygame_image = pygame.image.fromstring(data, size, mode)

        # Scale the image
        pygame_image = pygame.transform.scale(pygame_image, size)

        return pygame_image

    def create_highlighted_image(self, image, color):
        highlighted_image = pygame.Surface(image.get_size())
        highlighted_image.fill(color)
        highlighted_image.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        return highlighted_image

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.image_highlighted
        else:
            self.image = self.image_normal

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def click(self):
        if self.function:
            if self.params:
                self.function(*self.params)
            else:
                self.function()

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        if self.rect.x < pos[0] < self.rect.x + self.rect.width:
            if self.rect.y < pos[1] < self.rect.y + self.rect.height:
                return True
        return False
