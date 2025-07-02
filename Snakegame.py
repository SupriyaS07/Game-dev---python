import pygame
import time
import random


pygame.init()

# Set display width and height
width = 600
height = 400

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
yellow = (255, 255, 102)

# Snake block size and speed
block_size = 10
initial_speed = 15

# Set up display
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 20)

# Background animation setup
bg_circles = []
for _ in range(50):
    bg_circles.append([
        random.randint(0, width),
        random.randint(0, height),
        random.randint(1, 3),
        random.choice([white, blue, yellow])
    ])
    # Load and play background music
pygame.mixer.music.load("background music.mp3")  # Ensure this file exists in your directory
pygame.mixer.music.play(-1)  # Loop indefinitely

def draw_background():
    window.fill(black)
    for circle in bg_circles:
        pygame.draw.circle(window, circle[3], (circle[0], circle[1]), circle[2])
        circle[1] += 1
        if circle[1] > height:
            circle[0] = random.randint(0, width)
            circle[1] = 0

def message(msg, color, x, y):
    mesg = font_style.render(msg, True, color)
    window.blit(mesg, [x, y])

def your_score(score):
    value = score_font.render("Score: " + str(score), True, yellow)
    window.blit(value, [10, 10])

def pause_menu():
    paused = True
    while paused:
        draw_background()
        message("Game Paused. Press R to Resume or Q to Quit", yellow, width / 8, height / 2)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_r:
                    paused = False

def main_menu():
    menu = True
    while menu:
        draw_background()
        message("Welcome to Snake Game!", yellow, width / 4, height / 4)
        message("Press S to Start or Q to Quit", white, width / 4.5, height / 2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_s:
                    menu = False
                    gameLoop()

def gameLoop():
    game_over = False
    game_close = False

    x = width / 2
    y = height / 2
    x_change = 0
    y_change = 0

    snake_list = []
    length_of_snake = 1

    food_count = 1
    food_positions = [
        [round(random.randrange(0, width - block_size) / 10.0) * 10.0,
         round(random.randrange(0, height - block_size) / 10.0) * 10.0]
        for _ in range(food_count)
    ]

    speed = initial_speed

    while not game_over:
        while game_close:
            draw_background()
            message("You Lost! Press Q-Quit or C-Play Again", red, width / 6, height / 3)
            your_score(length_of_snake - 1)
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
                if event.key == pygame.K_LEFT:
                    x_change = -block_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = block_size
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -block_size
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = block_size
                    x_change = 0
                elif event.key == pygame.K_p:
                    pause_menu()

        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        x += x_change
        y += y_change
        draw_background()

        for food in food_positions:
            pygame.draw.rect(window, green, [food[0], food[1], block_size, block_size])

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        for block in snake_list:
            pygame.draw.rect(window, blue, [block[0], block[1], block_size, block_size])

        your_score(length_of_snake - 1)
        pygame.display.update()

        new_food_positions = []
        for food in food_positions:
            if x == food[0] and y == food[1]:
                length_of_snake += 1
                speed += 0.5
                for _ in range(length_of_snake // 5 + 1):
                    new_x = round(random.randrange(0, width - block_size) / 10.0) * 10.0
                    new_y = round(random.randrange(0, height - block_size) / 10.0) * 10.0
                    new_food_positions.append([new_x, new_y])
            else:
                new_food_positions.append(food)
        food_positions = new_food_positions

        clock.tick(int(speed))

    pygame.quit()
    quit()

main_menu()
