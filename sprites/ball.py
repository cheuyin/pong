import math
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
        self.initial_speed = settings.BALL_INITIAL_SPEED
        self.speed = self.initial_speed
        self.direction = self.random_starting_direction()
        self.color = settings.WHITE

        self.surface = pygame.Surface((self.size, self.size))
        self.surface.fill(self.color)
        self.rect: pygame.Rect = self.surface.get_rect()

        self.ball_hit_sound = pygame.mixer.Sound("assets/sounds/ball_hit_sound.wav")

        self.reset()

    def reset(self):
        self.rect.center = self.screen_rect.center
        self.x = self.rect.x
        self.y = self.rect.y
        self.speed = self.initial_speed
        self.direction = self.random_starting_direction()

    def random_starting_direction(self):
        left_or_right = random.choice([-1, 1])
        angle = random.uniform(-1, 1)
        return pygame.Vector2(left_or_right, angle).normalize()

    def update(self):
        self.calculate_new_xy()

        self.rect.x = self.x
        self.rect.y = self.y

        if self.player1.rect.colliderect(self.rect):
            self._resolve_paddle_collision(self.player1)
        elif self.player2.rect.colliderect(self.rect):
            self._resolve_paddle_collision(self.player2)
        elif self.rect.top <= 0:
            self.direction.y *= -1
            self.y = 1
            self.ball_hit_sound.play()
        elif self.rect.bottom >= self.screen_rect.height:
            self.direction.y *= -1
            self.y = self.screen_rect.height - self.size
            self.ball_hit_sound.play()

        self.rect.x = self.x
        self.rect.y = self.y

    def _resolve_paddle_collision(self, paddle: Paddle):
        self.ball_hit_sound.play()
        overlap_x = min(self.rect.right, paddle.rect.right) - max(self.rect.left, paddle.rect.left)
        overlap_y = min(self.rect.bottom, paddle.rect.bottom) - max(self.rect.top, paddle.rect.top)

        if overlap_y < overlap_x:  # Ball hits the top or bottom of the paddle
            self.direction.y *= -1
            if self.rect.centery < paddle.rect.centery:
                self.y = paddle.rect.top - self.size
            else:
                self.y = paddle.rect.bottom
        else:  # Ball hits the face of the paddle
            offset = paddle.get_hit_offset(self.rect)
            angle = offset * math.radians(75)
            x_dir = 1 if self.direction.x < 0 else -1
            self.direction = pygame.Vector2(x_dir * math.cos(angle), math.sin(angle))
            if self.rect.centerx < paddle.rect.centerx:
                self.x = paddle.rect.left - self.size
            else:
                self.x = paddle.rect.right
            self.speed += settings.BALL_SPEED_INCREMENT

    def calculate_new_xy(self):
        self.x += self.speed * self.direction.x
        self.y += self.speed * self.direction.y

    def draw(self):
        pygame.draw.circle(self.screen, settings.WHITE,
                           self.rect.center, self.rect.width / 2)
