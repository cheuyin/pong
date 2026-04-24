import pygame


class Paddle(pygame.sprite.Sprite):

    def __init__(self, screen: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen

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
        self.rect.y -= self.speed

    def movedown(self):
        self.rect.y += self.speed
