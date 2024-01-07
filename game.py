import pygame
import config
import random
import csv
from snake import Snake
from datapoint import DataPoint, SpecialDataPoint


class Game:
    def __init__(self, window):
        self.window = window
        self.snake = Snake()
        self.data_point = DataPoint()
        self.clock = pygame.time.Clock()
        self.running = True

        self.data_point_counter = 0
        self.slug_to_logo = self.load_slug_to_logo()
        self.current_special_data_point = None
        self.current_special_data_point_slug = None
        self.special_data_point_collided = False

    def load_slug_to_logo(self):
        """Load slug to logo mapping."""
        slug_to_logo = {
            "appliedsemantics": pygame.image.load(
                "assets/thumbnail/appliedsemantics.png"
            ),
            "youtube": pygame.image.load("assets/thumbnail/youtube.png"),
            "doubleclick": pygame.image.load("assets/thumbnail/doubleclick.png"),
            "admob": pygame.image.load("assets/thumbnail/admob.png"),
        }
        # Scale logos to fit the snake size
        for slug, logo in slug_to_logo.items():
            slug_to_logo[slug] = pygame.transform.scale(
                logo, (config.SNAKE_SIZE, config.SNAKE_SIZE)
            )
        return slug_to_logo

    def load_special_data_points(self):
        """Load special data points from the CSV file."""
        special_data_points_info = []
        with open("competitors.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                special_data_points_info.append(row)
        return special_data_points_info

    def generate_data_point_pos(self):
        """Generate a random position for a data point."""
        return [
            random.randrange(1, (config.WINDOW_SIZE[0] // config.SNAKE_SIZE))
            * config.SNAKE_SIZE,
            random.randrange(1, (config.WINDOW_SIZE[1] // config.SNAKE_SIZE))
            * config.SNAKE_SIZE,
        ]

    def run(self):
        while self.running:
            self.handle_events()
            self.update_game_state()
            self.render()
            self.clock.tick(config.SNAKE_SPEED)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)

    def handle_keydown(self, event):
        if event.key == pygame.K_LEFT:
            self.snake.update_direction("LEFT")
        elif event.key == pygame.K_RIGHT:
            self.snake.update_direction("RIGHT")
        elif event.key == pygame.K_UP:
            self.snake.update_direction("UP")
        elif event.key == pygame.K_DOWN:
            self.snake.update_direction("DOWN")

    def update_game_state(self):
        self.snake.move()

        if self.check_collision_with_data_point():
            self.handle_data_point_collision()
            return
        elif self.check_collision_with_special_data_point():
            self.handle_special_data_point_collision()
            return

        if (
            self.snake.check_collision_with_self()
            or self.snake.check_collision_with_boundaries(config.WINDOW_SIZE)
        ):
            self.game_over()
            self.restart_game()

    def render(self):
        self.window.fill(config.BLACK)
        self.snake.draw(self.window)

        # Draw the regular data point if it exists
        if self.data_point is not None:
            self.data_point.draw(self.window)

        # Draw the special data point if it exists
        if self.current_special_data_point is not None:
            self.current_special_data_point.draw(self.window)

        pygame.display.update()

    def game_over(self):
        # Implement game over logic
        pass

    def restart_game(self):
        # Implement restart game logic
        self.snake = Snake()
        self.data_point_pos = self.generate_data_point_pos()

    def create_special_data_point(self, slug):
        """Create a special data point based on the slug."""
        logo_path = self.slug_to_logo[slug]
        self.current_special_data_point = SpecialDataPoint(logo_path)

    def check_collision_with_data_point(self):
        """Check if the snake has collided with a data point."""
        head_position = self.snake.body[0]

        if self.data_point:
            if head_position == self.data_point.position:
                return True
        return False

    def check_collision_with_special_data_point(self):
        """Check if the snake has collided with a special data point."""
        head_position = self.snake.body[0]

        if (
            self.current_special_data_point
            and head_position == self.current_special_data_point.position
        ):
            # self.handle_special_data_point_collision()
            print("SPECIAL COLLISION")
            return True

        return False

    def handle_data_point_collision(self):
        """Handle the logic when the snake collides with a data point."""
        self.snake.grow()
        self.data_point_counter += 1

        if self.data_point_counter % config.SPECIALS_RATE == 0:
            print("REGULAR COLLISION to SPECIAL")
            index = (self.data_point_counter // config.SPECIALS_RATE) % len(self.slug_to_logo)
            slug = list(self.slug_to_logo.keys())[index]
            self.create_special_data_point(slug)
            self.data_point = None
        else:
            print("REGULAR COLLISION")
            self.data_point.reset_position()  # Generate a new regular data point

    def handle_special_data_point_collision(self):
        """Handle the logic when the snake collides with a special data point."""
        self.snake.grow()
        print(self.data_point_counter)

        # Recreate a new data point randomly
        self.data_point = DataPoint()
        self.data_point.reset_position()

        # Remove the current special data point
        self.current_special_data_point = None