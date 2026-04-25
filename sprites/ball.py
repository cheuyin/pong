import pygame
import math
import random


class Ball(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.size = 20
        self.speed = 5
        self.angle = self.generate_random_angle_rad()
        self.color = "yellow"

        self.surface = pygame.Surface((self.size, self.size))
        self.surface.fill(self.color)
        self.rect: pygame.Rect = self.surface.get_rect()

        self.center_ball()

    def center_ball(self):
        self.rect.center = self.screen_rect.center

    def update(self):
        new_xy = self.calculate_new_xy(
            self.rect.x, self.rect.y, self.speed, self.angle)
        self.rect.x = new_xy[0]
        self.rect.y = new_xy[1]

    def calculate_new_xy(self, old_x, old_y, speed, angle_rad) -> tuple[float, float]:
        new_x = old_x + speed * math.cos(angle_rad)
        new_y = old_y + speed * math.sin(angle_rad)
        return (new_x, new_y)

    def generate_random_angle_rad(self):
        random_rad = random.uniform(0, 2 * math.pi)
        return random_rad

    def draw(self):
        self.screen.blit(self.surface, self.rect)
