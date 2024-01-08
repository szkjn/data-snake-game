import sys
import pygame
import random
import csv

import cfg
import ui
from snake import Snake
from datapoint import DataPoint, SpecialDataPoint


class Game:
    def __init__(self, window):
        self.window = window
        self.state = "WELCOME_STATE"
        self.snake = Snake()
        self.data_point = DataPoint(self.snake.body)
        self.clock = pygame.time.Clock()
        self.running = True

        self.level = "Search Supremacist"
        self.final_score = 0

        self.data_point_counter = 0
        self.slug_to_logo = self.load_slug_to_logo()
        self.current_special_data_point = None
        self.current_special_data_point_slug = None
        self.special_data_point_collided = False

        self.play_button_rect = pygame.Rect(100, 150, 200, 50)
        self.quit_button_rect = pygame.Rect(100, 250, 200, 50)

        self.special_data_points_info = self.load_special_data_points()
        self.special_data_points_queue = [row["slug"] for row in self.special_data_points_info]


    def load_slug_to_logo(self):
        """Load slug to logo mapping."""
        slug_to_logo = {
            "appliedsemantics": pygame.image.load(
                "assets/thumbnail/appliedsemantics.png"
            ),
            "keyhole": pygame.image.load("assets/thumbnail/google.png"),
            "android": pygame.image.load("assets/thumbnail/google.png"),
            "youtube": pygame.image.load("assets/thumbnail/youtube.png"),
            "doubleclick": pygame.image.load("assets/thumbnail/doubleclick.png"),
            "admob": pygame.image.load("assets/thumbnail/admob.png"),
            "ita": pygame.image.load("assets/thumbnail/google.png"),
            "motorola": pygame.image.load("assets/thumbnail/google.png"),
            "waze": pygame.image.load("assets/thumbnail/google.png"),
            "nest": pygame.image.load("assets/thumbnail/google.png"),
            "deepmind": pygame.image.load("assets/thumbnail/google.png"),
            "firebase": pygame.image.load("assets/thumbnail/google.png"),
            "looker": pygame.image.load("assets/thumbnail/google.png"),
        }
        # Scale logos to fit the snake size
        for slug, logo in slug_to_logo.items():
            slug_to_logo[slug] = pygame.transform.scale(
                logo, (cfg.SNAKE_SIZE, cfg.SNAKE_SIZE)
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

    def run(self):
        while self.running:
            if self.state == "WELCOME_STATE":
                self.handle_welcome_page_events()
                ui.display_welcome_page(self.window)
            elif self.state == "PLAY_STATE":
                self.handle_events()
                self.update_game_state()
                ui.display_play_page(
                    self.window,
                    self.snake,
                    self.data_point,
                    self.level,
                    self.current_special_data_point,
                    self.data_point_counter,
                )
                self.clock.tick(cfg.SNAKE_SPEED)
            elif self.state == "SPECIAL_STATE":
                self.handle_special_page_events()
                ui.display_special_page(
                    self.window,
                    self.level,
                    self.current_special_data_point_slug,
                    self.special_data_points_info,
                    self.data_point_counter,
                )
            elif self.state == "GAME_OVER_STATE":
                self.handle_game_over_page_events()
                ui.display_game_over_page(self.window, self.final_score)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
                if event.key == pygame.K_q:
                    self.running = False

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
            self.state = "SPECIAL_STATE"
            return

        if (
            self.snake.check_collision_with_self()
            or self.snake.check_collision_with_boundaries(cfg.WINDOW_SIZE)
        ):
            self.final_score = self.data_point_counter
            self.state = "GAME_OVER_STATE"
            self.restart_game()

    def restart_game(self):
        """Implement restart game logic."""
        self.snake = Snake()
        self.data_point = DataPoint(self.snake.body)
        self.data_point_counter = 0
        self.current_special_data_point = None
        self.current_special_data_point_slug = None
        self.special_data_point_collided = False
        # self.data_point_pos = self.generate_data_point_pos()
        self.special_data_points_queue = [row["slug"] for row in self.special_data_points_info]

    def create_special_data_point(self, slug):
        """Create a special data point based on the slug."""
        # special_logo = self.slug_to_logo[slug]
        # self.current_special_data_point = SpecialDataPoint(
        #     special_logo, self.snake.body
        # )
        # self.current_special_data_point_slug = slug
        if self.special_data_points_queue:
            next_slug = self.special_data_points_queue.pop(0)  # Get the next slug
            special_logo = self.slug_to_logo[next_slug]
            self.current_special_data_point = SpecialDataPoint(special_logo, self.snake.body)
            self.current_special_data_point_slug = next_slug

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
            return True

        return False

    def handle_data_point_collision(self):
        """Handle the logic when the snake collides with a data point."""
        self.snake.grow()
        self.data_point_counter += 1

        if self.data_point_counter % cfg.SPECIALS_RATE == 0:
            index = (self.data_point_counter // cfg.SPECIALS_RATE) % len(
                self.slug_to_logo
            )
            slug = list(self.slug_to_logo.keys())[index]
            self.create_special_data_point(slug)
            self.data_point = None
        else:
            # Generate a new regular data point
            self.data_point.reset_position(self.snake.body)

    def handle_special_data_point_collision(self):
        """Handle the logic when the snake collides with a special data point."""
        self.snake.grow()

        # Update level based on the current special data point
        self.level = next(
            (row["level"] for row in self.special_data_points_info if row["slug"] == self.current_special_data_point_slug),
        )

        # Recreate a new data point randomly
        self.data_point = DataPoint(self.snake.body)

        # Remove the current special data point
        self.current_special_data_point = None

    def handle_welcome_page_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.state = "PLAY_STATE"
                elif event.key == pygame.K_q:
                    self.running = False

    def handle_game_over_page_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.state = "PLAY_STATE"
                elif event.key == pygame.K_q:
                    self.running = False

    def handle_special_page_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.state = "PLAY_STATE"
