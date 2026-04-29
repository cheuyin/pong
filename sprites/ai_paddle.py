import random
import pygame
import settings
from sprites.ball import Ball
from sprites.paddle import Paddle


class AIPaddle(Paddle):
    ball: Ball  # injected after Ball is constructed

    def __init__(self, screen: pygame.Surface, direction: str, difficulty: settings.Difficulty):
        super().__init__(screen, direction, color=settings.AI_PADDLE_COLOR)
        config = settings.AI_DIFFICULTY_SETTINGS[difficulty]
        self.speed = max(1, round(self.speed * config["speed_multiplier"]))
        self.error = config["error"]
        self._target_y = float(self.rect.centery)
        self._prev_ball_dir_x = 0

    def reset(self):
        super().reset()
        self._target_y = float(self.rect.centery)
        self._prev_ball_dir_x = 0

    def update(self):
        ball_dir_x = 1 if self.ball.direction.x > 0 else -1
        if ball_dir_x != self._prev_ball_dir_x:
            if self._ball_approaching():
                self._target_y = self._predict_intercept_y(
                ) + random.uniform(-self.error, self.error)
            self._prev_ball_dir_x = ball_dir_x

        if self.rect.centery < self._target_y - self.speed:
            self.movedown()
        elif self.rect.centery > self._target_y + self.speed:
            self.moveup()

    def _ball_approaching(self) -> bool:
        return (self.ball.direction.x > 0 and self.ball.rect.centerx < self.rect.centerx) or \
               (self.ball.direction.x < 0 and self.ball.rect.centerx > self.rect.centerx)

    def _predict_intercept_y(self) -> float:
        if self.ball.direction.x == 0:
            return self.ball.rect.centery

        distance_x = abs(self.rect.centerx - self.ball.rect.centerx)
        velocity_x = abs(self.ball.speed * self.ball.direction.x)
        time_to_reach = distance_x / velocity_x

        predicted_y = self.ball.rect.centery + self.ball.speed * \
            self.ball.direction.y * time_to_reach

        height = self.screen_rect.height
        while predicted_y < 0 or predicted_y > height:
            if predicted_y < 0:
                predicted_y = -predicted_y
            else:
                predicted_y = 2 * height - predicted_y

        return predicted_y
