import pygame
import sys
import random
import csv

import config
from game import Game


def main():
    pygame.init()
    window = pygame.display.set_mode(config.WINDOW_SIZE)
    pygame.display.set_caption("Data Snake Game")
    game = Game(window)
    game.run()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

exit()
# -------------------------------------------------------------------------------------
#                                   Initialize Pygame
# -------------------------------------------------------------------------------------
pygame.init()
window = pygame.display.set_mode(config.WINDOW_SIZE)
pygame.display.set_caption("Data Snake Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Snake settings
snake_size = 20
snake_speed = 7
snake_pos = [100, 60]
snake_body = [[100, 60], [80, 60], [60, 60]]
direction = "RIGHT"

# Data point settings
data_point_pos = [
    random.randrange(1, (config.WINDOW_SIZE[0] // snake_size)) * snake_size,
    random.randrange(1, (config.WINDOW_SIZE[1] // snake_size)) * snake_size,
]

clock = pygame.time.Clock()

# Load the logos
user_icon = pygame.image.load("assets/thumbnail/user_white.png")
snake_head_img = pygame.image.load("assets/thumbnail/google.png")
appliedsemantics_logo = pygame.image.load("assets/thumbnail/appliedsemantics.png")
youtube_logo = pygame.image.load("assets/thumbnail/youtube.png")
doubleclick_logo = pygame.image.load("assets/thumbnail/doubleclick.png")
admob_logo = pygame.image.load("assets/thumbnail/admob.png")

# Scale logos to fit the snake_size square
user_icon = pygame.transform.scale(user_icon, (snake_size, snake_size))
snake_head_img = pygame.transform.scale(snake_head_img, (snake_size, snake_size))

appliedsemantics_logo = pygame.transform.scale(
    appliedsemantics_logo, (snake_size, snake_size)
)
youtube_logo = pygame.transform.scale(youtube_logo, (snake_size, snake_size))
doubleclick_logo = pygame.transform.scale(doubleclick_logo, (snake_size, snake_size))
admob_logo = pygame.transform.scale(admob_logo, (snake_size, snake_size))

special_data_points_info = []
with open("competitors.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=";")
    for row in reader:
        special_data_points_info.append(row)

slug_to_logo = {
    "appliedsemantics": appliedsemantics_logo,
    "youtube": youtube_logo,
    "doubleclick": doubleclick_logo,
    "admob": admob_logo,
}

data_point_counter = 0
special_data_points = [
    appliedsemantics_logo,
    youtube_logo,
    doubleclick_logo,
    admob_logo,
]
current_special_data_point = None
current_special_data_point_slug = None


# -------------------------------------------------------------------------------------
#                                   FUNCTIONS
# -------------------------------------------------------------------------------------


def draw_snake(window, snake_body):
    for pos in snake_body:
        window.blit(snake_head_img, (pos[0], pos[1]))


def draw_data_point(window, pos):
    if current_special_data_point:
        window.blit(current_special_data_point, (pos[0], pos[1]))
    else:
        window.blit(user_icon, (pos[0], pos[1]))


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


# Make sure the restart_game function resets all necessary variables to start the game afresh
def restart_game():
    global snake_pos, snake_body, direction, data_point_pos, running
    snake_pos = [100, 60]
    snake_body = [[100, 60], [80, 60], [60, 60]]
    direction = "RIGHT"
    # Ensure data point is aligned with the grid
    data_point_pos = [
        random.randrange(0, config.WINDOW_SIZE[0] // snake_size) * snake_size,
        random.randrange(0, config.WINDOW_SIZE[1] // snake_size) * snake_size,
    ]
    running = True


def generate_data_point():
    while True:
        new_position = [
            random.randrange(0, config.WINDOW_SIZE[0] // snake_size) * snake_size,
            random.randrange(0, config.WINDOW_SIZE[1] // snake_size) * snake_size,
        ]
        if new_position not in snake_body:
            return new_position


special_data_point_collided = False


def check_collision_with_data_point():
    global snake_body, data_point_pos, data_point_counter, current_special_data_point, current_special_data_point_slug, special_data_point_collided

    if snake_pos[0] == data_point_pos[0] and snake_pos[1] == data_point_pos[1]:
        data_point_counter += 1
        if data_point_counter % 3 == 0 and not current_special_data_point:
            index = (data_point_counter // 3 - 1) % len(slug_to_logo)
            current_special_data_point_slug = list(slug_to_logo.keys())[index]
            current_special_data_point = slug_to_logo[current_special_data_point_slug]
        elif current_special_data_point:
            special_data_point_collided = True

        data_point_pos = generate_data_point()
        draw_grid()
        return True
    return False


def display_special_data_point_text(slug):

    # Get the name and text for the slug
    name = next(
        (row["name"] for row in special_data_points_info if row["slug"] == slug), ""
    )
    text = next(
        (row["text"] for row in special_data_points_info if row["slug"] == slug), ""
    )

    # Set up the square dimensions and position
    square_size = list(map(lambda x: x * 0.9, config.WINDOW_SIZE))  # Width, Height
    square_x = (config.WINDOW_SIZE[0] - square_size[0]) // 2
    square_y = (config.WINDOW_SIZE[1] - square_size[1]) // 2

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

    for x in range(0, config.WINDOW_SIZE[0], snake_size):  # Horizontal positions
        pygame.draw.line(
            window, line_color, (x, 0), (x, config.WINDOW_SIZE[1]), line_width
        )
    for y in range(0, config.WINDOW_SIZE[1], snake_size):  # Vertical positions
        pygame.draw.line(
            window, line_color, (0, y), (config.WINDOW_SIZE[0], y), line_width
        )

    # Draw white dots at intersections
    dot_color = white  # White color for the dots
    dot_size = 2  # Size of the dots
    for x in range(0, config.WINDOW_SIZE[0], snake_size):
        for y in range(0, config.WINDOW_SIZE[1], snake_size):
            pygame.draw.circle(window, dot_color, (x, y), dot_size)


# -------------------------------------------------------------------------------------
#                                   Game loop
# -------------------------------------------------------------------------------------

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"
            elif event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_c:
                restart_game()

    # Update snake position
    if direction == "RIGHT":
        snake_pos[0] += snake_size
    elif direction == "LEFT":
        snake_pos[0] -= snake_size
    elif direction == "UP":
        snake_pos[1] -= snake_size
    elif direction == "DOWN":
        snake_pos[1] += snake_size

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if not check_collision_with_data_point():
        snake_body.pop()

    if special_data_point_collided:
        display_special_data_point_text(current_special_data_point_slug)
        pygame.time.wait(3000)  # Freeze for 3 seconds
        current_special_data_point = None
        current_special_data_point_slug = None
        special_data_point_collided = False

    # Check collision with boundaries
    if (
        snake_pos[0] >= config.WINDOW_SIZE[0]
        or snake_pos[0] < 0
        or snake_pos[1] >= config.WINDOW_SIZE[1]
        or snake_pos[1] < 0
    ):
        game_over()
        pygame.time.wait(1000)
        restart_game()

    # Check collision with self
    for block in snake_body[1:]:
        if snake_pos == block:
            game_over()
            pygame.time.wait(1000)
            restart_game()

    # Update the display
    window.fill(black)
    # draw_grid()
    draw_snake(window, snake_body)
    draw_data_point(window, data_point_pos)
    pygame.display.update()

    clock.tick(snake_speed)


pygame.quit()
sys.exit()
