import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display window
window_size = (400, 300)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Data Snake Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Snake settings
snake_size = 20
snake_speed = 7
snake_pos = [100, 60]
snake_body = [[100, 60], [80, 60], [60, 60]]
direction = "RIGHT"

# Data point settings
data_point_pos = [random.randrange(1, (window_size[0]//snake_size)) * snake_size,
                  random.randrange(1, (window_size[1]//snake_size)) * snake_size]

clock = pygame.time.Clock()

# Load the logos
user_icon = pygame.image.load('assets/user_white.png')
snake_head_img = pygame.image.load('assets/google_sm.png')
youtube_logo = pygame.image.load('assets/youtube_sm.png')
doubleclick_logo = pygame.image.load('assets/doubleclick_sm.png')
admob_logo = pygame.image.load('assets/admob_sm.png')

# Scale logos to fit the snake_size square
user_icon = pygame.transform.scale(user_icon, (snake_size, snake_size))
snake_head_img = pygame.transform.scale(snake_head_img, (snake_size, snake_size))
youtube_logo = pygame.transform.scale(youtube_logo, (snake_size, snake_size))
doubleclick_logo = pygame.transform.scale(doubleclick_logo, (snake_size, snake_size))
admob_logo = pygame.transform.scale(admob_logo, (snake_size, snake_size))


def draw_snake(window, snake_body):
    for pos in snake_body:
        window.blit(snake_head_img, (pos[0], pos[1]))
        # if pos == snake_body[0]:
        #     window.blit(snake_head_img, (pos[0], pos[1]))
        # else:
        #     pygame.draw.rect(window, white, [pos[0], pos[1], snake_size, snake_size])


def draw_data_point(window, pos):
    if current_special_data_point:
        window.blit(current_special_data_point, (pos[0], pos[1]))
    else:
        window.blit(user_icon, (pos[0], pos[1]))
        # pygame.draw.rect(window, red, [pos[0], pos[1], snake_size, snake_size])

def game_over():
    font = pygame.font.SysFont(None, 55)
    message = font.render('Game Over! Press C-Continue or Q-Quit', True, red)
    window.blit(message, [window_size[0]//6, window_size[1]//3])
    pygame.display.flip()

def restart_game():
    global snake_pos, snake_body, direction, data_point_pos, running
    snake_pos = [100, 60]
    snake_body = [[100, 60], [80, 60], [60, 60]]
    direction = "RIGHT"
    # Ensure data point is aligned with the grid
    data_point_pos = [random.randrange(0, window_size[0] // snake_size) * snake_size,
                      random.randrange(0, window_size[1] // snake_size) * snake_size]
    running = True

data_point_counter = 0
special_data_points = [youtube_logo, doubleclick_logo, admob_logo]
current_special_data_point = None

def check_collision_with_data_point():
    global snake_body, data_point_pos, data_point_counter, current_special_data_point
    if snake_pos[0] == data_point_pos[0] and snake_pos[1] == data_point_pos[1]:
        data_point_counter += 1
        if data_point_counter % 3 == 0:
            current_special_data_point = special_data_points[(data_point_counter // 3 - 1) % len(special_data_points)]
        else:
            current_special_data_point = None
        data_point_pos = [random.randrange(0, window_size[0] // snake_size) * snake_size,
                          random.randrange(0, window_size[1] // snake_size) * snake_size]
        return True
    return False

def draw_grid():
    # Draw faint lines
    line_color = (50, 50, 50)  # Gray color for the lines
    line_width = 3  # New width for the lines

    for x in range(0, window_size[0], snake_size):  # Horizontal positions
        pygame.draw.line(window, line_color, (x, 0), (x, window_size[1]), line_width)
    for y in range(0, window_size[1], snake_size):  # Vertical positions
        pygame.draw.line(window, line_color, (0, y), (window_size[0], y), line_width)


    # Draw white dots at intersections
    dot_color = (255, 255, 255)  # White color for the dots
    dot_size = 2  # Size of the dots
    for x in range(0, window_size[0], snake_size):  
        for y in range(0, window_size[1], snake_size):
            pygame.draw.circle(window, dot_color, (x, y), dot_size)


# Inside your game loop, after updating positions
print("Snake Position:", snake_pos)
print("Data Point Position:", data_point_pos)

# Game loop
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

    # Check collision with boundaries
    if (snake_pos[0] >= window_size[0] or snake_pos[0] < 0 or
        snake_pos[1] >= window_size[1] or snake_pos[1] < 0):
        game_over()
        pygame.time.wait(2000)  # Wait for 2 seconds
        restart_game()

    # Check collision with self
    for block in snake_body[1:]:
        if snake_pos == block:
            game_over()
            pygame.time.wait(2000)  # Wait for 2 seconds
            restart_game()

    # Update the display
    window.fill(black)
    draw_grid()
    draw_snake(window, snake_body)
    draw_data_point(window, data_point_pos)
    pygame.display.update()

    clock.tick(snake_speed)

# Quit Pygame
pygame.quit()
sys.exit()
