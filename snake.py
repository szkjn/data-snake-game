import pygame
import config


class Snake:
    def __init__(self):
        # Initial settings
        self.size = config.SNAKE_SIZE
        self.position = [100, 60]  # Starting position
        self.body = [[100, 60], [80, 60], [60, 60]]  # Initial body segments
        self.direction = "RIGHT"
        self.head_img = pygame.image.load("assets/thumbnail/google.png")
        self.head_img = pygame.transform.scale(self.head_img, (self.size, self.size))

    def update_direction(self, new_direction):
        """Update the direction of the snake."""
        opposite_directions = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT",
        }
        if new_direction != opposite_directions[self.direction]:
            self.direction = new_direction

    def move(self):
        """Move the snake in the current direction."""
        if self.direction == "RIGHT":
            self.position[0] += self.size
        elif self.direction == "LEFT":
            self.position[0] -= self.size
        elif self.direction == "UP":
            self.position[1] -= self.size
        elif self.direction == "DOWN":
            self.position[1] += self.size

        # Update body
        self.body.insert(0, list(self.position))
        self.body.pop()

    def grow(self):
        """Add a new segment to the snake's body."""
        self.body.insert(0, list(self.position))

    def draw(self, window):
        """Draw the snake on the window."""
        for segment in self.body:
            window.blit(self.head_img, (segment[0], segment[1]))

    def check_collision_with_self(self):
        """Check if the snake has collided with itself."""
        for segment in self.body[1:]:
            if self.position == segment:
                return True
        return False

    def check_collision_with_boundaries(self, window_size):
        """Check if the snake has collided with the window boundaries."""
        if (
            self.position[0] >= window_size[0]
            or self.position[0] < 0
            or self.position[1] >= window_size[1]
            or self.position[1] < 0
        ):
            return True
        return False
