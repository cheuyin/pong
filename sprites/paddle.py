import pygame


class Paddle(pygame.sprite.Sprite):
    """
    Paddle in a Pong game.

    Parameters:
    - screen: the game window
    - direction: either "left" or "right" to represent the left or right paddle
    """

    def __init__(self, screen: pygame.Surface, direction: str):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width = 10
        self.height = 80
        self.speed = 8
        self.color = "white"

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.color)
        self.rect: pygame.Rect = self.surface.get_rect()

        if direction == "left":
            self.rect.center = self.screen_rect.center
            self.rect.x = 50
        elif direction == "right":
            self.rect.center = self.screen_rect.center
            self.rect.x = self.screen_rect.width - 50

    def draw(self):
        self.screen.blit(self.surface, self.rect)

    def get_hit_offset(self, ball_rect: pygame.Rect) -> float:
        offset = (ball_rect.centery - self.rect.centery) / (self.height / 2)
        return max(-1.0, min(1.0, offset))

    def moveup(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed

    def movedown(self):
        if self.rect.bottom < self.screen_rect.height:
            self.rect.y += self.speed
