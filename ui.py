# Button Class and UI-related functions

# ------------------------------------------
# Libraries imports
# ------------------------------------------
import pygame

# ------------------------------------------
# Modules imports
# ------------------------------------------
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
    draw_aligned_text(
        window,
        f"Score: {data_point_counter}",
        window.get_size()[1] - 4 * play_zone_padding,
        cfg.FONT_SIZE_L,
        cfg.WHITE,
        "left",
        play_zone_padding,
    )


def draw_level(window, level):
    play_zone_padding = cfg.SNAKE_SIZE

    draw_aligned_text(
        window,
        f"Level: {level}",
        window.get_size()[1] - 4 * play_zone_padding,
        cfg.FONT_SIZE_L,
        cfg.WHITE,
        "right",
        play_zone_padding,
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
    window,
    snake,
    data_point,
    level,
    current_special_data_point,
    data_point_counter,
    snake_visible,
):
    window.fill(cfg.BLACK)
    if snake_visible:
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
    ascii_art_file_path = "assets/ascii/skull.txt"

    draw_centered_text(
        window,
        "Welcome to Google's Snakeopoly!",
        50,
        cfg.FONT_SIZE_XL,
        cfg.WHITE,
    )

    draw_centered_text(
        window,
        "Slither your way",
        100,
        cfg.FONT_SIZE_XL,
        cfg.WHITE,
    )

    draw_centered_text(
        window,
        "to Surveillance Sovereignty!",
        125,
        cfg.FONT_SIZE_XL,
        cfg.WHITE,
    )

    image = create_pixelated_logo("assets/120x120/googlevil.png", cfg.WHITE, target_size=(100,100))
    window.blit(image, (320,190))
    window.blit(image, (80,190))


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


def display_game_over_page(window, final_score):
    window.fill(cfg.BLACK)

    draw_centered_text(window, "GAME OVER", 100, cfg.FONT_SIZE_XL, cfg.WHITE)

    draw_centered_text(
        window, f"Score: {final_score}", 125, cfg.FONT_SIZE_XL, cfg.WHITE
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


def display_special_page(
    window, level, slug, special_data_points_info, data_point_counter
):
    window.fill(cfg.BLACK)
    ascii_art_file_path = "assets/ascii/evil.txt"

    name = next(
        (row["name"] for row in special_data_points_info if row["slug"] == slug), ""
    )
    text = next(
        (row["text"] for row in special_data_points_info if row["slug"] == slug), ""
    )

    draw_centered_text(
        window, "Congrats! You've just acquired:", 50, cfg.FONT_SIZE_XL, cfg.WHITE
    )
    draw_centered_text(window, name, 90, cfg.FONT_SIZE_XL, cfg.WHITE)
    draw_ascii_art(window, ascii_art_file_path, (30, 125), cfg.FONT_SIZE_M, cfg.WHITE)

    logo_path = f"assets/120x120/{slug}.png"
    draw_centered_logo(
        window, logo_path, 130, cfg.WHITE, pixel_size=1, target_size=(75, 75)
    )

    draw_multiline_text(
        window, text, (170, 210), cfg.FONT_SIZE_L, cfg.WHITE, cfg.WINDOW_SIZE[0] - 90
    )

    draw_centered_text(
        window,
        "(R)ESUME GAME OR (Q)UIT LIKE A COWARD",
        window.get_size()[1] - 2 * cfg.SNAKE_SIZE,
        cfg.FONT_SIZE_L,
        cfg.WHITE,
    )

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


def draw_aligned_text(surface, text, y_pos, font_size, color, alignment, padding):
    font = pygame.font.Font(font_path, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    if alignment == "left":
        text_rect.topleft = (padding, y_pos)
    elif alignment == "right":
        x_pos = surface.get_width() - text_rect.width - padding
        text_rect.topleft = (x_pos, y_pos)
    else:
        raise ValueError("Invalid alignment specified. Choose 'left' or 'right'.")

    surface.blit(text_surface, text_rect)


def draw_ascii_art(window, art_file_path, top_left_position, font_size, color):
    font = pygame.font.Font(font_path, font_size)
    x, y = top_left_position

    with open(art_file_path, "r") as file:
        for line in file:
            line_surface = font.render(line, True, color)
            window.blit(line_surface, (x, y))
            y += line_surface.get_height()  # Move to the next line


def draw_centered_logo(
    surface,
    image_path,
    y_pos,
    color,
    pixel_size=1,
    target_size=(cfg.SNAKE_SIZE, cfg.SNAKE_SIZE),
):
    """
    Draw a centered, pixelated, monochrome logo on the surface.

    :param surface: Pygame surface to draw on.
    :param image_path: Path to the original logo image.
    :param y_pos: Vertical position for the top of the logo.
    :param color: Color for the pixelated image (tuple: (R, G, B)).
    :param pixel_size: Size of each 'pixel' in the pixelated image.
    :param target_size: Size to which the original image will be scaled (width, height).
    """
    # Create the pixelated logo
    pixelated_logo = create_pixelated_logo(image_path, color, pixel_size, target_size)

    if pixelated_logo:
        # Get the rect of the pixelated logo and position it
        logo_rect = pixelated_logo.get_rect()
        logo_rect.midtop = (surface.get_width() // 2, y_pos)

        # Draw the logo on the surface
        surface.blit(pixelated_logo, logo_rect)


def create_pixelated_logo(
    image_path, color, pixel_size=1, target_size=(cfg.SNAKE_SIZE, cfg.SNAKE_SIZE)
):
    """
    Convert a PNG logo to a pixelated monochrome logo using pygame.Rect.

    :param image_path: Path to the original image.
    :param color: Color for the pixelated image (tuple: (R, G, B)).
    :param pixel_size: Size of each 'pixel' in the pixelated image.
    :return: Surface with the pixelated image.
    """
    # Load the image
    try:
        image = pygame.image.load(image_path)
    except pygame.error as e:
        print(f"Unable to load image: {e}")
        return None

    # If pixel_size is high enough, return the original image (scaled to target size)
    if pixel_size < 1.0:
        # Calculate the downscaled size for increased pixelation
        downscaled_size = max(1, int(target_size[0] * pixel_size)), max(1, int(target_size[1] * pixel_size))

        # Scale the image down to create pixelation
        downscaled_image = pygame.transform.scale(image, downscaled_size)

        # Scale the pixelated image back up to the target size
        final_image = pygame.transform.scale(downscaled_image, target_size)
    else:
        final_image = pygame.transform.scale(image, target_size)

    # Create a new surface to apply the monochrome color
    pixelated_surface = pygame.Surface(target_size)

    # Apply the monochrome color to the upscaled pixelated image
    for x in range(target_size[0]):
        for y in range(target_size[1]):
            pixel_color = final_image.get_at((x, y))
            if pixel_color.a != 0:
                pixelated_surface.set_at((x, y), color)

    return pixelated_surface
