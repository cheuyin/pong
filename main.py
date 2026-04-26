import pygame
import sys
from time import sleep

from sprites.paddle import Paddle
from sprites.ball import Ball
from sprites.scoreboard import Scoreboard

from game_stats import GameStats


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
        self.stats = GameStats()
        self.bg_color = "black"
        self.scoreboard = Scoreboard(self.screen, self.stats)

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

            self.ball.update()
            self._check_ball_out_of_bounds()

            self._draw_screen()

            self.clock.tick(60)

    def _draw_screen(self):
        self.screen.fill(self.bg_color)
        self.player1.draw()
        self.player2.draw()
        self.ball.draw()
        self.scoreboard.show_score()

        pygame.display.flip()

    def _check_ball_out_of_bounds(self):
        screen_rect = self.screen.get_rect()
        ball_rect = self.ball.rect
        if ball_rect.right <= 0:
            self._round_over("player 2")
        elif ball_rect.left >= screen_rect.width:
            self._round_over("player 1")

    def _round_over(self, player_that_won):
        sleep(0.5)
        if player_that_won == "player 1":
            self.stats.player1_score += 1
        elif player_that_won == "player 2":
            self.stats.player2_score += 1
        self.scoreboard.prep_player_scores()
        self.ball.reset()


if __name__ == "__main__":
    pong = Game()
    pong.run_game()
