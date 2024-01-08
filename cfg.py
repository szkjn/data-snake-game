# Configuration settings for the game
import pygame

# Window settings
WINDOW_SIZE = (500, 400)

# Colors
BLACK = (0, 0, 0)
WHITE = (200, 255, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Snake settings
SNAKE_SIZE = 20
SNAKE_SPEED = 11
SPECIALS_RATE = 2

# Button settings
BUTTON_WIDTH = SNAKE_SIZE * 4
BUTTON_HEIGHT = SNAKE_SIZE * 2
CENTERED_BUTTON_X = (WINDOW_SIZE[0] / 2) - (BUTTON_WIDTH / 2)

# Text settings
FONT_SIZE_XL = 30
FONT_SIZE_L = 20
FONT_SIZE_M = 14

# Play zone
PLAY_ZONE_PADDING = SNAKE_SIZE

TEST = [[SNAKE_SIZE, SNAKE_SIZE]]

PLAY_ZONE_RECT = pygame.Rect(
    SNAKE_SIZE,
    SNAKE_SIZE,
    WINDOW_SIZE[0] - 2 * PLAY_ZONE_PADDING,
    WINDOW_SIZE[1] - 5 * PLAY_ZONE_PADDING,
)

# Freeze and blinking
FREEZE_TIMER = 999

