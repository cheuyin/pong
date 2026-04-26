import pygame
import sys
from time import sleep

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
        self.bg_color = "black"
        self.scoreboard = Scoreboard(self)

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
            self.player1_score += 1
        elif player_that_won == "player 2":
            self.player2_score += 1
        self.scoreboard.prep_player_scores()
        self.ball.reset()

        print("===== SCORE =====")
        print(f"Player 1: {self.player1_score}")
        print(f"Player 2: {self.player2_score}")


class Scoreboard:
    def __init__(self, game: Game):
        self.game = game
        self.screen_rect = game.screen.get_rect()
        self.text_color = (30, 30, 30)
        self.font_size = 64
        self.font = pygame.font.SysFont(None, self.font_size)

        self.prep_player_scores()

    def prep_player_scores(self):
        player_1_score_str = f"{self.game.player1_score}"
        player_2_score_str = f"{self.game.player2_score}"

        self.player_1_score_img = self.font.render(
            player_1_score_str, True, self.text_color)
        self.player_2_score_img = self.font.render(
            player_2_score_str, True, self.text_color)

        self.player_1_score_img_rect = self.player_1_score_img.get_rect()
        self.player_1_score_img_rect.left = self.screen_rect.left
        self.player_1_score_img_rect.top = self.screen_rect.top

        self.player_2_score_img_rect = self.player_2_score_img.get_rect()
        self.player_2_score_img_rect.right = self.screen_rect.right
        self.player_2_score_img_rect.top = self.screen_rect.top

    def show_score(self):
        self.game.screen.blit(self.player_1_score_img,
                              self.player_1_score_img_rect)
        self.game.screen.blit(self.player_2_score_img,
                              self.player_2_score_img_rect)


if __name__ == "__main__":
    pong = Game()
    pong.run_game()
