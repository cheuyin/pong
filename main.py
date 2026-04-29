from enum import Enum
import pygame
import sys
from time import sleep
import settings

from menu import Menu
from sprites.human_paddle import HumanPaddle
from sprites.ai_paddle import AIPaddle
from sprites.ball import Ball
from sprites.paddle import Paddle
from sprites.scoreboard import Scoreboard
from game_stats import GameStats


class GameState(Enum):
    MENU_GAME_MODE = "menu_game_mode"
    MENU_DIFFICULTY = "menu_difficulty"
    PLAYING = "playing"
    GAME_OVER = "game_over"


GAME_MODES = ["Human vs. Human", "Human vs. AI"]

DIFFICULTY_OPTIONS: list[tuple[str, settings.Difficulty]] = [
    ("Easy", settings.Difficulty.EASY),
    ("Medium", settings.Difficulty.MEDIUM),
    ("Hard", settings.Difficulty.HARD),
]


class Game:
    player1: Paddle
    player2: Paddle
    ball: Ball
    stats: GameStats
    scoreboard: Scoreboard
    winner: Paddle
    game_end_message: pygame.Surface

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(settings.WINDOW_CAPTION)
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.round_win_sound = pygame.mixer.Sound(
            "assets/sounds/round_win.wav")

        self.opponent_menu = Menu(self.screen, "PONG", GAME_MODES)
        self.difficulty_menu = Menu(
            self.screen, "AI Difficulty", [label for label, _ in DIFFICULTY_OPTIONS])
        self.state = GameState.MENU_GAME_MODE

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self._handle_event(event)

            if self.state == GameState.PLAYING:
                self.player1.update()
                self.player2.update()
                self.ball.update()
                self._check_ball_out_of_bounds()

            self._draw_screen()
            self.clock.tick(60)

    def _handle_event(self, event: pygame.event.Event):
        if self.state == GameState.MENU_GAME_MODE:
            selected = self.opponent_menu.handle_event(event)
            if selected is None:
                return
            if GAME_MODES[selected] == "Human vs. Human":
                player2 = HumanPaddle(
                    self.screen, "right", pygame.K_UP, pygame.K_DOWN)
                player2.name = "Player 2"
                self._start_game(player2)
            else:
                self.difficulty_menu.reset()
                self.state = GameState.MENU_DIFFICULTY

        elif self.state == GameState.MENU_DIFFICULTY:
            selected = self.difficulty_menu.handle_event(event)
            if selected is None:
                return
            _, difficulty = DIFFICULTY_OPTIONS[selected]
            player2 = AIPaddle(self.screen, "right", difficulty)
            player2.name = "AI"
            self._start_game(player2)

        elif self.state == GameState.GAME_OVER:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._reset_game()

    def _start_game(self, player2: Paddle):
        self.player1 = HumanPaddle(self.screen, "left", pygame.K_w, pygame.K_s)
        self.player1.name = "Player 1"
        self.player2 = player2
        self.ball = Ball(self.screen, self.player1, self.player2)
        if isinstance(self.player2, AIPaddle):
            self.player2.ball = self.ball
        self.stats = GameStats()
        self.scoreboard = Scoreboard(self.screen, self.stats)
        self.state = GameState.PLAYING

    def _draw_center_line(self):
        x = self.screen_rect.centerx
        dash_length = 12
        gap_length = 8
        y = 0
        while y < self.screen_rect.height:
            pygame.draw.line(self.screen, settings.GREY, (x, y),
                             (x, min(y + dash_length, self.screen_rect.height)))
            y += dash_length + gap_length

    def _draw_screen(self):
        if self.state == GameState.MENU_GAME_MODE:
            self.opponent_menu.draw()
        elif self.state == GameState.MENU_DIFFICULTY:
            self.difficulty_menu.draw()
        else:
            self.screen.fill(settings.SCREEN_BG_COLOR)
            self._draw_center_line()
            self.player1.draw()
            self.player2.draw()
            if self.state == GameState.PLAYING:
                self.ball.draw()
            self.scoreboard.show_score()
            if self.state == GameState.GAME_OVER:
                self._draw_game_end_message()

        pygame.display.flip()

    def _check_ball_out_of_bounds(self):
        ball_rect = self.ball.rect
        if ball_rect.right <= 0:
            self._round_over(settings.Player.PLAYER_2)
        elif ball_rect.left >= self.screen_rect.width:
            self._round_over(settings.Player.PLAYER_1)

    def _round_over(self, player_that_won):
        self.round_win_sound.play()
        sleep(0.5)
        if player_that_won == settings.Player.PLAYER_1:
            self.stats.player1_score += 1
        elif player_that_won == settings.Player.PLAYER_2:
            self.stats.player2_score += 1
        self.scoreboard.prep_player_scores()
        self.ball.reset()
        self.player1.reset()
        self.player2.reset()

        if self.stats.player1_score == settings.WINNING_SCORE:
            self.winner = self.player1
            self._game_over()
        elif self.stats.player2_score == settings.WINNING_SCORE:
            self.winner = self.player2
            self._game_over()

    def _game_over(self):
        self.state = GameState.GAME_OVER
        self._prep_game_end_message()

    def _reset_game(self):
        self.state = GameState.PLAYING
        self.ball.reset()
        self.player1.reset()
        self.player2.reset()
        self.stats.player1_score = 0
        self.stats.player2_score = 0
        self.scoreboard.prep_player_scores()

    def _prep_game_end_message(self):
        winner_message_font = settings.SMALL_TEXT
        winner_message = winner_message_font.render(
            f"Winner: {self.winner.name}", True, settings.WHITE)
        play_again_message_font = settings.SMALL_TEXT
        play_again_message = play_again_message_font.render(
            "Press space to restart", True, settings.GREY)

        vertical_gap = 20

        height = winner_message.get_rect().height + \
            play_again_message.get_rect().height + vertical_gap
        width = max(winner_message.get_rect().width,
                    play_again_message.get_rect().width)

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
