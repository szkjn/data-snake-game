import pygame

import cfg

font_path = 'assets/font/VT323/VT323-Regular.ttf'

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
    play_zone_rect = pygame.Rect(cfg.SNAKE_SIZE, cfg.SNAKE_SIZE, 
                                 window.get_size()[0] - 2 * cfg.SNAKE_SIZE, 
                                 window.get_size()[1] - 5 * cfg.SNAKE_SIZE)
    pygame.draw.rect(window, cfg.WHITE, play_zone_rect, 1)


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


def display_welcome_page(window):
    window.fill(cfg.BLACK)

    draw_text(
        window,
        "Welcome to the Game!",
        (cfg.CENTERED_BUTTON_X, 50),
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

    draw_text(window, "Game Over !", (50, 50), cfg.FONT_SIZE_XL, cfg.WHITE)

    draw_text(
        window, f"Score : {data_point_counter}", (50, 75), cfg.FONT_SIZE_XL, cfg.WHITE
    )

    # Create and draw buttons
    play_button = Button(
        window,
        "(P)lay Again",
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


def display_special_page(window, slug, special_data_points_info):
    window.fill(cfg.BLACK)

    name = next(
        (row["name"] for row in special_data_points_info if row["slug"] == slug), ""
    )
    text = next(
        (row["text"] for row in special_data_points_info if row["slug"] == slug), ""
    )

    draw_text(window, "Congrats !", (25, 50), cfg.FONT_SIZE_XL, cfg.WHITE)
    draw_text(window, f"You've just acquired {name}", (25, 75), cfg.FONT_SIZE_XL, cfg.WHITE)
    draw_text(window, text, (25, 125), cfg.FONT_SIZE_L, cfg.WHITE)

    # Create and draw buttons
    play_button = Button(
        window,
        "(R)ESUME",
        (cfg.CENTERED_BUTTON_X, 150),
        (cfg.BUTTON_WIDTH, cfg.BUTTON_HEIGHT),
    )
    play_button.draw()
    
    draw_play_zone(window)
    pygame.display.update()
