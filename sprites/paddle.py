import pygame


class Paddle(pygame.sprite.Sprite):

    def __init__(self, screen: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width = 20
        self.height = 100
        self.speed = 5
        self.color = "white"

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.color)
        self.rect: pygame.Rect = self.surface.get_rect()

        self.rect.center = self.screen.get_rect().center

    def draw(self):
        self.screen.blit(self.surface, self.rect)

    def moveup(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed

    def movedown(self):
        if self.rect.bottom < self.screen_rect.height:
            self.rect.y += self.speed
