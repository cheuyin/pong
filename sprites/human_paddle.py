import pygame
from sprites.paddle import Paddle


class HumanPaddle(Paddle):
    def __init__(self, screen: pygame.Surface, direction: str, up_key: int, down_key: int):
        super().__init__(screen, direction)
        self.up_key = up_key
        self.down_key = down_key

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.up_key]:
            self.moveup()
        if keys[self.down_key]:
            self.movedown()
