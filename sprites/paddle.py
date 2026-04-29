import pygame
import settings


class Paddle(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, direction: str, color=None):
        pygame.sprite.Sprite.__init__(self)

        self.name: str = ""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width = settings.PADDLE_WIDTH
        self.height = settings.PADDLE_HEIGHT
        self.speed = settings.PADDLE_SPEED
        self.color = color or settings.WHITE

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.color)
        self.rect: pygame.Rect = self.surface.get_rect()

        if direction == "left":
            self.rect.center = self.screen_rect.center
            self.rect.x = settings.PADDLE_EDGE_OFFSET
        elif direction == "right":
            self.rect.center = self.screen_rect.center
            self.rect.x = self.screen_rect.width - settings.PADDLE_EDGE_OFFSET

    def update(self):
        pass

    def reset(self):
        self.rect.centery = self.screen_rect.centery

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
