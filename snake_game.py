import pygame
import time
import random

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (255, 87, 87)
GREEN = (0, 255, 150)
BLUE = (30, 30, 50)
GOLD = (255, 215, 0)
PURPLE = (128, 0, 128)
BG_COLOR = (15, 15, 25)
SNAKE_COLOR = (0, 230, 118)
FOOD_COLOR = (255, 61, 0)
GRID_COLOR = (25, 25, 35)

# Screen dimensions
WIDTH = 600
HEIGHT = 400

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Clock to control the speed of the snake
clock = pygame.time.Clock()

# Snake parameters
snake_block = 10
starting_speed = 3
speed_increase_per_food = 0.5
max_speed = 25

# Font styles
font_style = pygame.font.SysFont('bahnschrift', 25)
score_font = pygame.font.SysFont('comicsansms', 35)


# Function to display the score
def Your_score(score):
    score_surf = score_font.render('Score: ' + str(score), True, WHITE)
    screen.blit(score_surf, [10, 10])


# Function to draw the snake
def our_snake(snake_block, snake_list, direction):
    for i, x in enumerate(snake_list):
        rect = [x[0], x[1], snake_block, snake_block]
        
        # Color gradient for the snake
        color_val = max(100, 230 - i * 3)
        current_color = (0, color_val, 118)
        
        if i == len(snake_list) - 1: # Head
            pygame.draw.rect(screen, SNAKE_COLOR, rect, border_radius=snake_block//2)
            # Draw eyes
            eye_size = 3
            eye_color = BLACK
            if direction == "UP":
                pygame.draw.circle(screen, eye_color, (int(x[0] + 3), int(x[1] + 3)), eye_size)
                pygame.draw.circle(screen, eye_color, (int(x[0] + 7), int(x[1] + 3)), eye_size)
            elif direction == "DOWN":
                pygame.draw.circle(screen, eye_color, (int(x[0] + 3), int(x[1] + 7)), eye_size)
                pygame.draw.circle(screen, eye_color, (int(x[0] + 7), int(x[1] + 7)), eye_size)
            elif direction == "LEFT":
                pygame.draw.circle(screen, eye_color, (int(x[0] + 3), int(x[1] + 3)), eye_size)
                pygame.draw.circle(screen, eye_color, (int(x[0] + 3), int(x[1] + 7)), eye_size)
            elif direction == "RIGHT":
                pygame.draw.circle(screen, eye_color, (int(x[0] + 7), int(x[1] + 3)), eye_size)
                pygame.draw.circle(screen, eye_color, (int(x[0] + 7), int(x[1] + 7)), eye_size)
        else: # Body
            pygame.draw.rect(screen, current_color, rect, border_radius=4)


def draw_grid():
    for x in range(0, WIDTH, snake_block * 2):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, snake_block * 2):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

def draw_food(x, y, size, pulse_val):
    glow_radius = int(size * (1.2 + pulse_val * 0.3))
    s = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(s, (255, 61, 0, 50), (glow_radius, glow_radius), glow_radius)
    screen.blit(s, (x - glow_radius + size//2, y - glow_radius + size//2))
    pygame.draw.circle(screen, FOOD_COLOR, (int(x + size/2), int(y + size/2)), int(size/2))


# Function to display messages
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [WIDTH / 6, HEIGHT / 3])


# Game loop
def gameLoop():  
    game_over = False
    game_close = False

    x1 = WIDTH / 2
    y1 = HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0

    current_direction = "RIGHT"
    pulse = 0
    pulse_dir = 1

    while not game_over:
        while game_close == True:
            screen.fill(BG_COLOR)
            message('You Lost! Press C-Play Again or Q-Quit', RED)
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and current_direction != "RIGHT":
                    x1_change = -snake_block
                    y1_change = 0
                    current_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and current_direction != "LEFT":
                    x1_change = snake_block
                    y1_change = 0
                    current_direction = "RIGHT"
                elif event.key == pygame.K_UP and current_direction != "DOWN":
                    y1_change = -snake_block
                    x1_change = 0
                    current_direction = "UP"
                elif event.key == pygame.K_DOWN and current_direction != "UP":
                    y1_change = snake_block
                    x1_change = 0
                    current_direction = "DOWN"

        # Check for boundaries
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        
        # Rendering
        screen.fill(BG_COLOR)
        draw_grid()
        
        # Pulse animation for food
        pulse += 0.1 * pulse_dir
        if pulse > 1 or pulse < 0:
            pulse_dir *= -1
            
        draw_food(foodx, foody, snake_block, pulse)

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List, current_direction)
        Your_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        # Calculate current speed based on snake length
        current_speed = min(
            max_speed,
            starting_speed + (Length_of_snake - 1) * speed_increase_per_food,
        )
        clock.tick(current_speed)

    pygame.quit()
    quit()


# Start the game
if __name__ == '__main__':
    gameLoop()