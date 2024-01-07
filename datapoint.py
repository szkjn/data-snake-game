import pygame
import config
import random

class DataPoint:
    def __init__(self, snake_body):
        self.position = self.generate_random_position(snake_body)
        self.image = pygame.transform.scale(
            pygame.image.load("assets/thumbnail/user_white.png"),
            (config.SNAKE_SIZE, config.SNAKE_SIZE),
        )

    def generate_random_position(self, snake_body):
        """Generate a random position for the data point."""
        while True:
            position = [
                random.randrange(1, (config.WINDOW_SIZE[0] // config.SNAKE_SIZE))
                * config.SNAKE_SIZE,
                random.randrange(1, (config.WINDOW_SIZE[1] // config.SNAKE_SIZE))
                * config.SNAKE_SIZE,
            ]

            if position not in snake_body:
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
        self.special_logo = pygame.transform.scale(special_logo, (config.SNAKE_SIZE, config.SNAKE_SIZE))
    
    def draw(self, window):
        """Draw the special data point on the given window."""
        window.blit(self.special_logo, (self.position[0], self.position[1]))
