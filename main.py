import pygame
import sys
from time import sleep
import settings

from sprites.paddle import Paddle
from sprites.ball import Ball
from sprites.scoreboard import Scoreboard
from game_stats import GameStats


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(settings.WINDOW_CAPTION)
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.game_active = True
        self.player1 = Paddle(self.screen, "left")
        self.player2 = Paddle(self.screen, "right")
        self.winner: settings.Player
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
            self._draw_game_end_message()

        pygame.display.flip()

    def _check_ball_out_of_bounds(self):
        ball_rect = self.ball.rect
        if ball_rect.right <= 0:
            self._round_over(settings.Player.PLAYER_2)
        elif ball_rect.left >= self.screen_rect.width:
            self._round_over(settings.Player.PLAYER_1)

    def _round_over(self, player_that_won):
        sleep(0.5)
        if player_that_won == settings.Player.PLAYER_1:
            self.stats.player1_score += 1
        elif player_that_won == settings.Player.PLAYER_2:
            self.stats.player2_score += 1
        self.scoreboard.prep_player_scores()
        self.ball.reset()

        if self.stats.player1_score == settings.WINNING_SCORE:
            self.winner = settings.Player.PLAYER_1
            self._game_over()
        elif self.stats.player2_score == settings.WINNING_SCORE:
            self.winner = settings.Player.PLAYER_2
            self._game_over()

    def _game_over(self):
        self.game_active = False
        self._prep_game_end_message()

    def _reset_game(self):
        self.game_active = True
        self.ball.reset()
        self.stats.player1_score = 0
        self.stats.player2_score = 0
        self.scoreboard.prep_player_scores()

    def _prep_game_end_message(self):
        winner_message_font = pygame.font.SysFont(
            settings.PRIMARY_FONT, settings.MEDIUM_TEXT)
        winner_message = winner_message_font.render(
            f"Winner: {self.winner.value}", True, settings.WHITE)
        play_again_message_font = pygame.font.SysFont(
            settings.PRIMARY_FONT, settings.SMALL_TEXT)
        play_again_message = play_again_message_font.render(
            "Press space to restart", True, settings.GREY)

        vertical_gap = 20

        height = winner_message.get_rect().height + \
            play_again_message.get_rect().height + vertical_gap
        width = max(winner_message.get_rect().width,
                    play_again_message.get_rect().height)

        parent = pygame.Surface((width, height))
        winner_message_rect = winner_message.get_rect()
        winner_message_rect.centerx = parent.get_rect().centerx
        winner_message_rect.y = 0

        play_again_message_rect = play_again_message.get_rect()
        play_again_message_rect.centerx = parent.get_rect().centerx
        play_again_message_rect.y = winner_message_rect.bottom + vertical_gap

        parent.blit(winner_message, winner_message_rect)
        parent.blit(play_again_message, play_again_message_rect)

        self.game_end_message = parent

    def _draw_game_end_message(self):
        game_end_message_rect = self.game_end_message.get_rect()
        game_end_message_rect.center = self.screen_rect.center
        self.screen.blit(self.game_end_message, game_end_message_rect)


if __name__ == "__main__":
    pong = Game()
    pong.run_game()
