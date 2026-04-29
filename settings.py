from enum import Enum


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (220, 220, 220)
LIGHT_GREY = (30, 30, 30)
AI_PADDLE_COLOR = (220, 80, 80)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WINDOW_CAPTION = "Pong"
SCREEN_BG_COLOR = BLACK
WINNING_SCORE = 3

BALL_INITIAL_SPEED = 8
BALL_SPEED_INCREMENT = 0.5

PRIMARY_FONT = None

SMALL_TEXT = 24
MEDIUM_TEXT = 48
LARGE_TEXT = 64


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

AI_DIFFICULTY = Difficulty.MEDIUM
