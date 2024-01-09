# Configuration settings for the game

# ------------------------------------------
# Libraries imports
# ------------------------------------------
import pygame

# ------------------------------------------
# Constants
# ------------------------------------------

# General
WINDOW_RATIO = 5/4
WINDOW_WIDTH = 500
WINDOW_WIDTH = 800
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_WIDTH/WINDOW_RATIO)
WINDOW_UNIT = int(WINDOW_WIDTH/25)
COLOR_MODE = "NIGHT"
if COLOR_MODE == "NIGHT":
    BLACK = (0, 0, 0)
    WHITE = (200, 255, 200)
elif COLOR_MODE == "DAY":
    BLACK = (200, 255, 200)
    WHITE = (0, 0, 0)

# Snake

SNAKE_SIZE = WINDOW_UNIT
SNAKE_SPEED = 6
SPECIALS_RATE = 2

# Button
BUTTON_WIDTH = SNAKE_SIZE * 4
BUTTON_HEIGHT = SNAKE_SIZE * 2
CENTERED_BUTTON_X = (WINDOW_SIZE[0] / 2) - (BUTTON_WIDTH / 2)

# Text
FONT_SIZE_XL = int(WINDOW_UNIT * 1.3)
FONT_SIZE_L = WINDOW_UNIT
FONT_SIZE_M = int(WINDOW_UNIT*0.5)
FONT_SIZE_S = int(WINDOW_UNIT*0.3)

# Play Zone
PLAY_ZONE_PADDING = SNAKE_SIZE
PLAY_ZONE_RECT = pygame.Rect(
    SNAKE_SIZE,
    SNAKE_SIZE,
    WINDOW_SIZE[0] - 2 * PLAY_ZONE_PADDING,
    WINDOW_SIZE[1] - 5 * PLAY_ZONE_PADDING,
)
PLAY_ZONE_WIDTH = PLAY_ZONE_RECT[2]- PLAY_ZONE_RECT[0]
PLAY_ZONE_HEIGHT = PLAY_ZONE_RECT[3]- PLAY_ZONE_RECT[1]

# Freeze
FREEZE_TIMER = 999
