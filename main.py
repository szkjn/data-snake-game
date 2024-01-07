import pygame
import sys
import random
import csv

import cfg
from game import Game


def main():
    pygame.init()
    window = pygame.display.set_mode(cfg.WINDOW_SIZE)
    pygame.display.set_caption("Data Snake Game")
    game = Game(window)
    game.run()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

exit()

# -------------------------------------------------------------------------------------
#                                   FUNCTIONS
# -------------------------------------------------------------------------------------


def draw_button_text(text, start_x, start_y, color):
    for letter in text:
        # Draw a white background rectangle
        pygame.draw.rect(window, color, [start_x, start_y, snake_size, snake_size])

        # Render the letter
        font = pygame.font.SysFont(None, 30)
        letter_surface = font.render(letter, True, black)
        letter_x = start_x + (snake_size - letter_surface.get_width()) // 2
        letter_y = start_y + (snake_size - letter_surface.get_height()) // 2
        window.blit(letter_surface, (letter_x, letter_y))

        # Move to next grid unit
        start_x += snake_size


def game_over():
    global data_point_counter, running
    font = pygame.font.SysFont(None, 30)  # Adjust font size to fit the grid unit
    messages = [
        "Game Over !",
        "You've stuffed",
        "yourself with",
        f"{data_point_counter} data pts!",
    ]

    # Set starting position for the message
    x_start = 2 * snake_size
    y_start = 4 * snake_size

    # Render each letter
    for message in messages:
        for letter in message:
            # Draw a white background rectangle
            pygame.draw.rect(window, white, [x_start, y_start, snake_size, snake_size])

            # Render the letter in black
            letter_surface = font.render(letter, True, black)
            letter_x = x_start + (snake_size - letter_surface.get_width()) // 2
            letter_y = y_start + (snake_size - letter_surface.get_height()) // 2
            window.blit(letter_surface, (letter_x, letter_y))

            # Move to next grid unit
            x_start += snake_size

        # Move to the next line
        y_start += snake_size
        x_start = 2 * snake_size

    # # Adjust button positions based on grid
    play_again_button = pygame.Rect(
        4 * snake_size, 10 * snake_size, 3 * snake_size, snake_size
    )
    quit_button = pygame.Rect(
        8 * snake_size, 10 * snake_size, 3 * snake_size, snake_size
    )

    pygame.draw.rect(window, [0, 255, 0], play_again_button)  # Green play again button
    pygame.draw.rect(window, [255, 0, 0], quit_button)  # Red quit button

    # Draw the button text
    draw_button_text("Play", 4 * snake_size, 10 * snake_size, green)
    draw_button_text("Quit", 8 * snake_size, 10 * snake_size, red)

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if play_again_button.collidepoint(mouse_pos):
                    waiting_for_input = False
                    running = (
                        False  # Set running to False to exit the current game loop
                    )
                    restart_game()  # Restart the game
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    waiting_for_input = False
                    running = (
                        False  # Set running to False to exit the current game loop
                    )
                    restart_game()  # Restart the game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def display_special_data_point_text(slug):

    # Get the name and text for the slug
    name = next(
        (row["name"] for row in special_data_points_info if row["slug"] == slug), ""
    )
    text = next(
        (row["text"] for row in special_data_points_info if row["slug"] == slug), ""
    )

    # Set up the square dimensions and position
    square_size = list(map(lambda x: x * 0.9, cfg.WINDOW_SIZE))  # Width, Height
    square_x = (cfg.WINDOW_SIZE[0] - square_size[0]) // 2
    square_y = (cfg.WINDOW_SIZE[1] - square_size[1]) // 2

    # Draw the square
    pygame.draw.rect(
        window, black, [square_x, square_y, square_size[0], square_size[1]]
    )
    pygame.draw.rect(
        window, white, [square_x, square_y, square_size[0], square_size[1]], 2
    )  # Border

    # Set up text and logo
    font = pygame.font.SysFont(None, 22)
    messages = ["CONGRATS ::)", "YOU'VE JUST ACQUIRED :", f"{name}"]
    for i, message in enumerate(messages):
        message_surface = font.render(message, True, white)
        window.blit(message_surface, (square_x + 10, square_y + (i + 1) * 30))

    # Draw the logo
    logo = slug_to_logo[slug]
    window.blit(logo, (square_x + (square_size[0] - snake_size) // 2, square_y + 120))

    text_surface = font.render(text, True, white)
    window.blit(text_surface, (square_x + 10, square_y + 150))

    pygame.display.update()


def draw_grid():
    # Draw faint lines
    line_color = (50, 50, 50)  # Gray color for the lines
    line_width = 3  # New width for the lines

    for x in range(0, cfg.WINDOW_SIZE[0], snake_size):  # Horizontal positions
        pygame.draw.line(
            window, line_color, (x, 0), (x, cfg.WINDOW_SIZE[1]), line_width
        )
    for y in range(0, cfg.WINDOW_SIZE[1], snake_size):  # Vertical positions
        pygame.draw.line(
            window, line_color, (0, y), (cfg.WINDOW_SIZE[0], y), line_width
        )

    # Draw white dots at intersections
    dot_color = white  # White color for the dots
    dot_size = 2  # Size of the dots
    for x in range(0, cfg.WINDOW_SIZE[0], snake_size):
        for y in range(0, cfg.WINDOW_SIZE[1], snake_size):
            pygame.draw.circle(window, dot_color, (x, y), dot_size)


# -------------------------------------------------------------------------------------
#                                   Game loop
# -------------------------------------------------------------------------------------

if special_data_point_collided:
    display_special_data_point_text(current_special_data_point_slug)
    pygame.time.wait(3000)  # Freeze for 3 seconds
    current_special_data_point = None
    current_special_data_point_slug = None
    special_data_point_collided = False
