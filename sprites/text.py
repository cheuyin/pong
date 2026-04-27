import pygame


class Text(pygame.sprite.Sprite):
    def __init__(self, msg: str, x: int, y: int, screen: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.color = "white"
        self.font = pygame.font.SysFont(None, 48)
        self.font_image = self.font.render(msg, True, "white")
        self.rect: pygame.Rect = self.font_image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def draw(self):
        self.screen.blit(self.font_image, self.rect)
