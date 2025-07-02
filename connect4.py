import numpy as np
import pygame
import sys
import time
import random
import math

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = SQUARESIZE // 2 - 5

WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)

# Colors
BLACK = (0, 0, 0)
RED = (220, 20, 60)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)
GREEN = (50, 205, 50)

# Init
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Connect Four: Player vs Computer")
clock = pygame.time.Clock()

font = pygame.font.SysFont("comicsansms", 48)
small_font = pygame.font.SysFont("comicsansms", 36)

# Music
pygame.mixer.init()
pygame.mixer.music.load("background music.mp3")
pygame.mixer.music.play(-1)

# Score
player_score = 0
computer_score = 0


def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def winning_move(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if all(board[r][c + i] == piece for i in range(4)):
                return True

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True

    return False


def draw_score():
    score_text = small_font.render(f"Player: {player_score}  Computer: {computer_score}", True, WHITE)
    screen.blit(score_text, (10, 10))


def draw_board(board, color_shift):
    for y in range(HEIGHT):
        color = (
            int(70 + 50 * math.sin((y + color_shift) * 0.03)) % 256,
            int(30 + 100 * math.cos((y + color_shift) * 0.01)) % 256,
            int(200 + 30 * math.sin((y + color_shift) * 0.02)) % 256
        )
        pygame.draw.rect(screen, color, (0, y, WIDTH, 1))

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLACK, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE), 2)
            pygame.draw.circle(screen, BLACK, (c * SQUARESIZE + SQUARESIZE // 2,
                                               r * SQUARESIZE + SQUARESIZE + SQUARESIZE // 2), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            color = None
            if board[r][c] == 1:
                color = RED
            elif board[r][c] == 2:
                color = YELLOW

            if color:
                pygame.draw.circle(screen, color,
                                   (c * SQUARESIZE + SQUARESIZE // 2,
                                    HEIGHT - (r * SQUARESIZE + SQUARESIZE // 2)),
                                   RADIUS)

    draw_score()
    pygame.display.update()


def animate_piece(col, row, piece, board, color_shift):
    for drop_y in range(0, HEIGHT - row * SQUARESIZE, 20):
        draw_board(board, color_shift)
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
        color = RED if piece == 1 else YELLOW
        pygame.draw.circle(screen, color, (col * SQUARESIZE + SQUARESIZE // 2, drop_y + SQUARESIZE // 2), RADIUS)
        draw_score()
        pygame.display.update()
        time.sleep(0.01)
    drop_piece(board, row, col, piece)
    draw_board(board, color_shift)


def animated_start_button():
    scale = 1.0
    growing = True
    while True:
        screen.fill(BLACK)
        title = font.render("Connect Four", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 120))

        scale += 0.01 if growing else -0.01
        if scale >= 1.1:
            growing = False
        elif scale <= 1.0:
            growing = True

        button_width = int(200 * scale)
        button_height = int(60 * scale)
        button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height)
        pygame.draw.rect(screen, GREEN, button_rect, border_radius=15)
        text = small_font.render("Start Game", True, WHITE)
        screen.blit(text, (button_rect.centerx - text.get_width() // 2, button_rect.centery - text.get_height() // 2))

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return


# Game Init
board = create_board()
turn = 0
color_shift = 0

animated_start_button()
draw_board(board, color_shift)

while True:
    color_shift += 1
    draw_board(board, color_shift)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if turn == 0:
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                posx = event.pos[0]
                pygame.draw.circle(screen, RED, (posx, SQUARESIZE // 2), RADIUS)
                draw_score()
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = posx // SQUARESIZE

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    animate_piece(col, row, 1, board, color_shift)

                    if winning_move(board, 1):
                        player_score += 1
                        win_text = font.render("Player Wins!", True, WHITE)
                        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 50))
                        pygame.display.update()
                        time.sleep(3)
                        board = create_board()
                        draw_board(board, color_shift)
                    else:
                        turn = 1

    if turn == 1:
        pygame.time.wait(500)
        valid_columns = [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]
        col = random.choice(valid_columns)
        row = get_next_open_row(board, col)
        animate_piece(col, row, 2, board, color_shift)

        if winning_move(board, 2):
            computer_score += 1
            win_text = font.render("Computer Wins!", True, WHITE)
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 50))
            pygame.display.update()
            time.sleep(3)
            board = create_board()
            draw_board(board, color_shift)
        else:
            turn = 0

