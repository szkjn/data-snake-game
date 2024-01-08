import pygame

import cfg

font_path = "assets/font/VT323/VT323-Regular.ttf"


class Button:
    def __init__(self, surface, text, position, size):
        self.surface = surface
        self.text = text
        self.rect = pygame.Rect(position, size)

    def draw(self):
        # Draw the button
        draw_button(self.surface, self.text, self.rect.topleft, self.rect.size)

    def is_clicked(self, event):
        # Check if the button is clicked
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
            event.pos
        )


def draw_play_zone(window):
    pygame.draw.rect(window, cfg.WHITE, cfg.PLAY_ZONE_RECT, 1)

def draw_score_counter(window, data_point_counter):
    play_zone_padding = cfg.SNAKE_SIZE
    draw_text(
        window,
        f"Score: {data_point_counter}",
        (25, window.get_size()[1] - 4 * play_zone_padding),
        cfg.FONT_SIZE_L,
        cfg.WHITE,
    )

def draw_level(window, level):
    play_zone_padding = cfg.SNAKE_SIZE

    draw_text(
        window,
        f"Level: {level}",
        (150, window.get_size()[1] - 4 * play_zone_padding),
        cfg.FONT_SIZE_L,
        cfg.WHITE,
    )


def draw_button(surface, text, position, size):
    font = pygame.font.Font(font_path, cfg.FONT_SIZE_L)
    text_render = font.render(text, True, cfg.WHITE)
    rect = pygame.Rect(position, size)
    pygame.draw.rect(surface, cfg.WHITE, rect, 1)
    surface.blit(text_render, text_render.get_rect(center=rect.center))


def draw_text(surface, text, position, font_size, color):
    font = pygame.font.Font(font_path, font_size)
    text_render = font.render(text, True, color)
    surface.blit(text_render, position)


def display_play_page(
    window, snake, data_point, level, current_special_data_point, data_point_counter
):
    window.fill(cfg.BLACK)
    snake.draw(window)

    # Draw the regular data point if it exists
    if data_point is not None:
        data_point.draw(window)

    # Draw the special data point if it exists
    if current_special_data_point is not None:
        current_special_data_point.draw(window)

    # Draw the play zone border
    play_zone_padding = cfg.SNAKE_SIZE
    play_zone_rect = pygame.Rect(
        play_zone_padding,
        play_zone_padding,
        window.get_size()[0] - 2 * play_zone_padding,
        window.get_size()[1] - 5 * play_zone_padding,
    )
    pygame.draw.rect(window, cfg.WHITE, play_zone_rect, 1)  # 1 is the border width

    draw_score_counter(window, data_point_counter)
    draw_level(window, level)
    pygame.display.update()


def display_welcome_page(window):
    window.fill(cfg.BLACK)

    draw_centered_text(
        window,
        "Welcome to the Game!",
        100,
        cfg.FONT_SIZE_XL,
        cfg.WHITE,
    )

    play_button = Button(
        window,
        "(P)LAY",
        (cfg.CENTERED_BUTTON_X, 200),
        (cfg.BUTTON_WIDTH, cfg.BUTTON_HEIGHT),
    )
    play_button.draw()
    quit_button = Button(
        window,
        "(Q)UIT",
        (cfg.CENTERED_BUTTON_X, 250),
        (cfg.BUTTON_WIDTH, cfg.BUTTON_HEIGHT),
    )
    quit_button.draw()

    draw_play_zone(window)
    pygame.display.update()


def display_game_over_page(window, data_point_counter):
    window.fill(cfg.BLACK)

    draw_centered_text(window, "GAME OVER", 100, cfg.FONT_SIZE_XL, cfg.WHITE)

    draw_centered_text(
        window, f"Score: {data_point_counter}", 125, cfg.FONT_SIZE_XL, cfg.WHITE
    )

    # Create and draw buttons
    play_button = Button(
        window,
        "(P)lay",
        (cfg.CENTERED_BUTTON_X, 200),
        (cfg.BUTTON_WIDTH, cfg.BUTTON_HEIGHT),
    )
    play_button.draw()
    quit_button = Button(
        window,
        "(Q)uit",
        (cfg.CENTERED_BUTTON_X, 250),
        (cfg.BUTTON_WIDTH, cfg.BUTTON_HEIGHT),
    )
    quit_button.draw()

    draw_play_zone(window)
    pygame.display.update()


def display_special_page(window, level, slug, special_data_points_info, data_point_counter):
    window.fill(cfg.BLACK)
    ascii_art_file_path = 'assets/ascii/evil.txt'

    name = next(
        (row["name"] for row in special_data_points_info if row["slug"] == slug), ""
    )
    text = next(
        (row["text"] for row in special_data_points_info if row["slug"] == slug), ""
    )

    draw_centered_text(window, "Congrats !", 50, cfg.FONT_SIZE_XL, cfg.WHITE)
    draw_centered_text(
        window, "You've just acquired:", 75, cfg.FONT_SIZE_XL, cfg.WHITE
    )
    draw_centered_text(
        window, name, 100, cfg.FONT_SIZE_XL, cfg.WHITE
    )
    draw_ascii_art(window, ascii_art_file_path, (30, 125), cfg.FONT_SIZE_M, cfg.WHITE)

    draw_multiline_text(
        window, text, (165, 150), cfg.FONT_SIZE_L, cfg.WHITE, cfg.WINDOW_SIZE[0] - 100
    )

    # Create and draw buttons
    play_button = Button(
        window,
        "(R)ESUME",
        (cfg.CENTERED_BUTTON_X, 260),
        (cfg.BUTTON_WIDTH, cfg.BUTTON_HEIGHT),
    )
    play_button.draw()

    draw_play_zone(window)
    draw_score_counter(window, data_point_counter)
    draw_level(window, level)

    pygame.display.update()


def draw_multiline_text(surface, text, position, font_size, color, max_line_width):
    text = f'"{text}"'
    font = pygame.font.Font(font_path, font_size)
    words = text.split(" ")
    space = font.size(" ")[0]  # Width of a space.
    x, y = position
    line = []

    for word in words:
        word_surface = font.render(word, True, color)
        word_width, word_height = word_surface.get_size()
        if x + word_width >= max_line_width:
            # If the line width exceeds the limit, render the line and reset it
            surface.blit(font.render(" ".join(line), True, color), (position[0], y))
            line = [word]
            y += word_height  # Move to the next line
            x = position[0]
        else:
            line.append(word)
            x += word_width + space

    # Render the last line
    surface.blit(font.render(" ".join(line), True, color), (position[0], y))


def draw_centered_text(surface, text, y_pos, font_size, color):
    font = pygame.font.Font(font_path, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    text_rect.midtop = (surface.get_width() / 2, y_pos)

    surface.blit(text_surface, text_rect)


def draw_ascii_art(window, art_file_path, top_left_position, font_size, color):
    font = pygame.font.Font(font_path, font_size)
    x, y = top_left_position

    with open(art_file_path, 'r') as file:
        for line in file:
            line_surface = font.render(line, True, color)
            window.blit(line_surface, (x, y))
            y += line_surface.get_height()  # Move to the next line
