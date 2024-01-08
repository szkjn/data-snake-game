# DataPoint Class

# ------------------------------------------
# Libraries imports
# ------------------------------------------
import pygame
import random

# ------------------------------------------
# Modules imports
# ------------------------------------------
import cfg


class DataPoint:
    def __init__(self, snake_body):
        self.position = self.generate_random_position(snake_body)
        self.image = pygame.transform.scale(
            pygame.image.load("assets/sm/user_white.png"),
            (cfg.SNAKE_SIZE, cfg.SNAKE_SIZE),
        )

    def generate_random_position(self, snake_body):
        """Generate a random position for the data point."""
        while True:
            x = random.randrange(
                cfg.PLAY_ZONE_RECT.left, cfg.PLAY_ZONE_RECT.right, cfg.SNAKE_SIZE
            )
            y = random.randrange(
                cfg.PLAY_ZONE_RECT.top, cfg.PLAY_ZONE_RECT.bottom, cfg.SNAKE_SIZE
            )
            position = [x, y]

            # Create a rect for the position to check if it's inside the play zone
            position_rect = pygame.Rect(x, y, cfg.SNAKE_SIZE, cfg.SNAKE_SIZE)

            if position not in snake_body and cfg.PLAY_ZONE_RECT.contains(
                position_rect
            ):
                return position

    def draw(self, window):
        """Draw the data point on the given window."""
        window.blit(self.image, (self.position[0], self.position[1]))

    def reset_position(self, snake_body):
        """Reset the position of the data point."""
        self.position = self.generate_random_position(snake_body)


class SpecialDataPoint(DataPoint):
    def __init__(self, special_logo, snake_body):
        super().__init__(snake_body)
        self.special_logo = pygame.transform.scale(
            special_logo, (cfg.SNAKE_SIZE, cfg.SNAKE_SIZE)
        )

    def draw(self, window):
        """Draw the special data point on the given window."""
        window.blit(self.special_logo, (self.position[0], self.position[1]))
