import pygame
import random

# Initialize pygame
pygame.init()

# Screen settings
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 255, 0)

# Snake settings
snake_block = 10
clock = pygame.time.Clock()
speed = 5

font = pygame.font.SysFont(None, 35)

def message(msg, color):
    text = font.render(msg, True, color)
    screen.blit(text, [width / 6, height / 3])

def game_loop():
    game_over = False
    game_close = False

    x = width / 2
    y = height / 2

    dx = 0
    dy = 0

    snake = []
    length = 1

    foodx = random.randrange(0, width - snake_block, snake_block)
    foody = random.randrange(0, height - snake_block, snake_block)

    while not game_over:

        while game_close:
            screen.fill(black)
            message("You lost! Press Q-Quit or C-Play", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -snake_block
                    dy = 0
                elif event.key == pygame.K_RIGHT:
                    dx = snake_block
                    dy = 0
                elif event.key == pygame.K_UP:
                    dx = 0
                    dy = -snake_block
                elif event.key == pygame.K_DOWN:
                    dx = 0
                    dy = snake_block

        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        x += dx
        y += dy

        screen.fill(black)

        pygame.draw.rect(screen, green, [foodx, foody, snake_block, snake_block])

        snake_head = [x, y]
        snake.append(snake_head)

        if len(snake) > length:
            del snake[0]

        for segment in snake[:-1]:
            if segment == snake_head:
                game_close = True

        for segment in snake:
            pygame.draw.rect(screen, white, [segment[0], segment[1], snake_block, snake_block])

        pygame.display.update()

        if x == foodx and y == foody:
            foodx = random.randrange(0, width - snake_block, snake_block)
            foody = random.randrange(0, height - snake_block, snake_block)
            length += 1

        clock.tick(speed)

    pygame.quit()
    quit()

game_loop()