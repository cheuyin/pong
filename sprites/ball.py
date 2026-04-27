import pygame
import math
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
        self.angle = 0
        self.color = settings.WHITE

        self.surface = pygame.Surface((self.size, self.size))
        self.surface.fill(self.color)
        self.rect: pygame.Rect = self.surface.get_rect()

        self.reset()

    def reset(self):
        self.rect.center = self.screen_rect.center
        self.x = self.rect.x
        self.y = self.rect.y
        self.angle = self.generate_random_angle_rad()

    def update(self):
        if self.player1.rect.colliderect(self.rect) or self.player2.rect.colliderect(self.rect):
            new_x = math.cos(self.angle) * -1
            new_y = math.sin(self.angle)
            self.angle = math.atan2(new_y, new_x)
        elif self.check_hit_top_bottom_walls():
            # Invert y coord
            new_x = math.cos(self.angle)
            new_y = math.sin(self.angle) * -1
            self.angle = math.atan2(new_y, new_x)

        self.calculate_new_xy()

        self.rect.x = self.x
        self.rect.y = self.y

    def check_hit_top_bottom_walls(self):
        return self.rect.top <= 0 or self.rect.bottom >= self.screen_rect.height

    def calculate_new_xy(self):
        self.x = self.x + self.speed * math.cos(self.angle)
        self.y = self.y + self.speed * math.sin(self.angle)

    def generate_random_angle_rad(self):
        random_rad = random.uniform(0, 2 * math.pi)
        return random_rad

    def draw(self):
        self.screen.blit(self.surface, self.rect)
