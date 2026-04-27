import pygame


class Text(pygame.sprite.Sprite):
    def __init__(self, msg: str, text_size, x: int, y: int, screen: pygame.Surface, color=(255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.font = pygame.font.SysFont(None, text_size)
        self.font_image = self.font.render(msg, True, color)
        self.rect: pygame.Rect = self.font_image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def draw(self):
        self.screen.blit(self.font_image, self.rect)
