from enum import Enum

import pygame

MENU_SELECTION_COLOR = (255, 215, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (220, 220, 220)
LIGHT_GREY = (30, 30, 30)
AI_PADDLE_COLOR = (255, 215, 0)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WINDOW_CAPTION = "Pong"
SCREEN_BG_COLOR = BLACK
WINNING_SCORE = 3

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 80
PADDLE_SPEED = 8
PADDLE_EDGE_OFFSET = 50

BALL_SIZE = 20
BALL_INITIAL_SPEED = 8
BALL_SPEED_INCREMENT = 0.5
BALL_MAX_DEFLECTION_DEGREES = 75

SCOREBOARD_CENTER_OFFSET = 100
SCOREBOARD_TOP_PADDING = 20

CENTER_LINE_DASH_LENGTH = 12
CENTER_LINE_GAP_LENGTH = 8

ROUND_PAUSE_MS = 500

PRIMARY_FONT_FILE = "assets/fonts/Jersey10-Regular.ttf"

pygame.font.init()

SMALL_TEXT = pygame.font.Font(PRIMARY_FONT_FILE, 24)
MEDIUM_TEXT = pygame.font.Font(PRIMARY_FONT_FILE, 48)
LARGE_TEXT = pygame.font.Font(PRIMARY_FONT_FILE, 64)


class Player(Enum):
    PLAYER_1 = "Player 1"
    PLAYER_2 = "Player 2"


class Difficulty(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


AI_DIFFICULTY_SETTINGS = {
    Difficulty.EASY:   {"speed_multiplier": 0.45, "error": 75},
    Difficulty.MEDIUM: {"speed_multiplier": 0.70, "error": 40},
    Difficulty.HARD:   {"speed_multiplier": 1.00, "error": 25},
}
