import pygame
import config
import random


class DataPoint:
    def __init__(self):
        self.position = self.generate_random_position()
        self.image = pygame.transform.scale(
            pygame.image.load("assets/thumbnail/user_white.png"),
            (config.SNAKE_SIZE, config.SNAKE_SIZE),
        )

    def generate_random_position(self):
        """Generate a random position for the data point."""
        return [
            random.randrange(1, (config.WINDOW_SIZE[0] // config.SNAKE_SIZE))
            * config.SNAKE_SIZE,
            random.randrange(1, (config.WINDOW_SIZE[1] // config.SNAKE_SIZE))
            * config.SNAKE_SIZE,
        ]

    def draw(self, window):
        """Draw the data point on the given window."""
        window.blit(self.image, (self.position[0], self.position[1]))

    def reset_position(self):
        """Reset the position of the data point."""
        self.position = self.generate_random_position()


class SpecialDataPoint(DataPoint):
    def __init__(self, special_image):
        super().__init__()
        self.special_image = pygame.transform.scale(special_image, (config.SNAKE_SIZE, config.SNAKE_SIZE))
    
    def draw(self, window):
        """Draw the special data point on the given window."""
        window.blit(self.special_image, (self.position[0], self.position[1]))
