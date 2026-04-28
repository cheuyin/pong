import pygame
import random
import settings
from sprites.paddle import Paddle


class Ball(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, player1: Paddle, player2: Paddle):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.player1 = player1
        self.player2 = player2

        self.size = 20
        self.x = 0
        self.y = 0
        self.speed = 8
        self.direction = self.random_starting_direction()
        self.color = settings.WHITE

        self.surface = pygame.Surface((self.size, self.size))
        self.surface.fill(self.color)
        self.rect: pygame.Rect = self.surface.get_rect()

        self.reset()

    def reset(self):
        self.rect.center = self.screen_rect.center
        self.x = self.rect.x
        self.y = self.rect.y
        self.direction = self.random_starting_direction()

    def random_starting_direction(self):
        left_or_right = random.choice([-1, 1])
        angle = random.uniform(-1, 1)
        return pygame.Vector2(left_or_right, angle).normalize()

    def update(self):
        oldRect = self.rect.copy()

        self.calculate_new_xy()

        self.rect.x = self.x
        self.rect.y = self.y

        if self.player1.rect.colliderect(self.rect):
            if oldRect.bottom <= self.player1.rect.top:
                self.direction.y *= -1
                self.y = self.player1.rect.top - self.size
            elif oldRect.top >= self.player1.rect.bottom:
                self.direction.y *= -1
                self.y = self.player1.rect.bottom
            else:
                self.direction.x *= -1
        elif self.player2.rect.colliderect(self.rect):
            if oldRect.bottom <= self.player2.rect.top:
                self.direction.y *= -1
                self.y = self.player2.rect.top - self.size
            elif oldRect.top >= self.player2.rect.bottom:
                self.direction.y *= -1
                self.y = self.player2.rect.bottom
            else:
                self.direction.x *= -1
        elif self.check_hit_top_bottom_walls():
            self.direction.y *= -1

        self.rect.x = self.x
        self.rect.y = self.y

    def check_hit_top_bottom_walls(self):
        return self.rect.top <= 0 or self.rect.bottom >= self.screen_rect.height

    def calculate_new_xy(self):
        self.x += self.speed * self.direction.x
        self.y += self.speed * self.direction.y

    def draw(self):
        pygame.draw.circle(self.screen, settings.WHITE,
                           self.rect.center, self.rect.width / 2)
