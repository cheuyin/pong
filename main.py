import pygame
import sys
from time import sleep
import settings

from sprites.paddle import Paddle
from sprites.ball import Ball
from sprites.scoreboard import Scoreboard
from sprites.text import Text

from game_stats import GameStats


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(settings.WINDOW_CAPTION)
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_active = True
        self.player1 = Paddle(self.screen, "left")
        self.player2 = Paddle(self.screen, "right")
        self.ball = Ball(self.screen, self.player1, self.player2)
        self.stats = GameStats()
        self.scoreboard = Scoreboard(self.screen, self.stats)
        self.game_end_message: pygame.Surface

    def run_game(self):
        while True:
            # Process Inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and not self.game_active:
                    if pygame.key.get_just_pressed()[pygame.K_SPACE]:
                        self._reset_game()

            if self.game_active:
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
        self.screen.fill(settings.SCREEN_BG_COLOR)
        self.player1.draw()
        self.player2.draw()
        if self.game_active:  # Only draw ball when game is active
            self.ball.draw()
        self.scoreboard.show_score()

        if not self.game_active:
            self.game_end_message1.draw()
            self.game_end_message2.draw()

        pygame.display.flip()

    def _check_ball_out_of_bounds(self):
        screen_rect = self.screen.get_rect()
        ball_rect = self.ball.rect
        if ball_rect.right <= 0:
            self._round_over("Player 2")
        elif ball_rect.left >= screen_rect.width:
            self._round_over("Player 1")

    def _round_over(self, player_that_won):
        sleep(0.5)
        if player_that_won == "Player 1":
            self.stats.player1_score += 1
        elif player_that_won == "Player 2":
            self.stats.player2_score += 1
        self.scoreboard.prep_player_scores()
        self.ball.reset()

        if self.stats.player1_score == settings.WINNING_SCORE:
            self._game_over("Player 1")
        elif self.stats.player2_score == settings.WINNING_SCORE:
            self._game_over("Player 2")

    def _game_over(self, player_that_won):
        self.game_active = False
        screen_rect = self.screen.get_rect()
        self.game_end_message1 = Text(
            f"Winner: {player_that_won}", settings.MEDIUM_TEXT, screen_rect.centerx, screen_rect.centery, self.screen)
        self.game_end_message2 = Text(
            f"Press space to restart", settings.SMALL_TEXT, screen_rect.centerx, screen_rect.centery + 50, self.screen, settings.GREY)

    def _reset_game(self):
        self.game_active = True
        self.ball.reset()
        self.stats.player1_score = 0
        self.stats.player2_score = 0
        self.scoreboard.prep_player_scores()

    def _prep_game_end_message(self):
        pass

    def _draw_game_end_message(self):
        pass


if __name__ == "__main__":
    pong = Game()
    pong.run_game()
