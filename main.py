import pygame
import sys

from sprites.paddle import Paddle
from sprites.ball import Ball


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pong")
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.game_active = True
        self.player1 = Paddle(self.screen, "left")
        self.player2 = Paddle(self.screen, "right")
        self.ball = Ball(self.screen, self.player1, self.player2)
        self.winning_score = 3
        self.player1_score = 0
        self.player2_score = 0

    def run_game(self):
        while self.game_active:
            # Process Inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.player2.moveup()
            if keys[pygame.K_DOWN]:
                self.player2.movedown()
            if keys[pygame.K_w]:
                self.player1.moveup()
            if keys[pygame.K_s]:
                self.player1.movedown()

            # Reset Screen
            self.screen.fill("black")

            # Update
            self.ball.update()

            # Draw Sprites
            self.player1.draw()
            self.player2.draw()
            self.ball.draw()

            # Update Screen
            pygame.display.flip()

            # 60 fps Clock Tick
            self.clock.tick(60)


if __name__ == "__main__":
    pong = Game()
    pong.run_game()
