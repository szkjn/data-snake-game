import pygame

import config


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
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


def draw_button(surface, text, position, size):
    font = pygame.font.Font(None, 36)
    text_render = font.render(text, True, config.WHITE)
    rect = pygame.Rect(position, size)
    pygame.draw.rect(surface, config.WHITE, rect, 2)
    surface.blit(text_render, text_render.get_rect(center=rect.center))

def draw_text(surface, text, position, font_size, color):
    font = pygame.font.Font(None, font_size)
    text_render = font.render(text, True, color)
    surface.blit(text_render, position)

def display_welcome_page(window):
    window.fill(config.BLACK)

    # Greeting text
    draw_text(
        window, 
        "Welcome to the Game!", 
        (config.CENTERED_BUTTON_X, 50), 
        config.FONT_SIZE_XL, 
        config.WHITE
    )

    # Create and draw buttons
    play_button = Button(
        window, 
        "Play", 
        (config.CENTERED_BUTTON_X, 150), 
        (config.BUTTON_WIDTH, config.BUTTON_HEIGHT)
    )
    play_button.draw()
    quit_button = Button(
        window, 
        "Quit", 
        (config.CENTERED_BUTTON_X, 250), 
        (config.BUTTON_WIDTH, config.BUTTON_HEIGHT)
    )
    quit_button.draw()

    pygame.display.update()
