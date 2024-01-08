# Configuration settings for the game

# ------------------------------------------
# Libraries imports
# ------------------------------------------
import pygame

# ------------------------------------------
# Constants
# ------------------------------------------

# General
WINDOW_SIZE = (500, 400)
BLACK = (0, 0, 0)
WHITE = (200, 255, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Snake
SNAKE_SIZE = 20
SNAKE_SPEED = 8
SPECIALS_RATE = 2

# Button
BUTTON_WIDTH = SNAKE_SIZE * 4
BUTTON_HEIGHT = SNAKE_SIZE * 2
CENTERED_BUTTON_X = (WINDOW_SIZE[0] / 2) - (BUTTON_WIDTH / 2)

# Text
FONT_SIZE_XL = 30
FONT_SIZE_L = 20
FONT_SIZE_M = 13

# Play Zone
PLAY_ZONE_PADDING = SNAKE_SIZE

TEST = [[SNAKE_SIZE, SNAKE_SIZE]]

PLAY_ZONE_RECT = pygame.Rect(
    SNAKE_SIZE,
    SNAKE_SIZE,
    WINDOW_SIZE[0] - 2 * PLAY_ZONE_PADDING,
    WINDOW_SIZE[1] - 5 * PLAY_ZONE_PADDING,
)

# Freeze
FREEZE_TIMER = 999
