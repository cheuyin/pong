import pygame
import settings
from game_stats import GameStats


class Scoreboard:
    def __init__(self, window: pygame.Surface, stats: GameStats):
        self.window = window
        self.window_rect = window.get_rect()
        self.text_color = settings.LIGHT_GREY
        self.font = settings.LARGE_TEXT
        self.stats = stats

        self.prep_player_scores()

    def prep_player_scores(self):
        player_1_score_str = f"{self.stats.player1_score}"
        player_2_score_str = f"{self.stats.player2_score}"

        self.player_1_score_img = self.font.render(
            player_1_score_str, True, self.text_color)
        self.player_2_score_img = self.font.render(
            player_2_score_str, True, self.text_color)

        self.player_1_score_img_rect = self.player_1_score_img.get_rect()
        self.player_1_score_img_rect.centerx = self.window_rect.centerx - settings.SCOREBOARD_CENTER_OFFSET
        self.player_1_score_img_rect.top += settings.SCOREBOARD_TOP_PADDING

        self.player_2_score_img_rect = self.player_2_score_img.get_rect()
        self.player_2_score_img_rect.centerx = self.window_rect.centerx + settings.SCOREBOARD_CENTER_OFFSET
        self.player_2_score_img_rect.top += settings.SCOREBOARD_TOP_PADDING

    def show_score(self):
        self.window.blit(self.player_1_score_img,
                         self.player_1_score_img_rect)
        self.window.blit(self.player_2_score_img,
                         self.player_2_score_img_rect)
