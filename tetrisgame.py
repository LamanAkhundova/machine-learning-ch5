import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Block size
BLOCK_SIZE = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]  # J
]

# Tetromino colors
COLORS = [CYAN, MAGENTA, GREEN, RED, YELLOW, ORANGE, BLUE]

# Define the game board
BOARD_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
BOARD_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
board = [[BLACK for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = BOARD_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def draw(self, screen):
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col]:
                    pygame.draw.rect(screen, self.color,
                                     (self.x * BLOCK_SIZE + col * BLOCK_SIZE,
                                      self.y * BLOCK_SIZE + row * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))

    def move(self, dx, dy):
        if not self.collides(dx, dy, self.shape):
            self.x += dx
            self.y += dy

    def rotate(self):
        new_shape = list(zip(*self.shape[::-1]))
        if not self.collides(0, 0, new_shape):
            self.shape = new_shape

    def collides(self, dx, dy, shape):
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col]:
                    new_x = self.x + dx + col
                    new_y = self.y + dy + row
                    if new_x < 0 or new_x >= BOARD_WIDTH or new_y >= BOARD_HEIGHT or new_y >= 0 and board[new_y][new_x] != BLACK:
                        return True
        return False

def clear_lines():
    global board
    new_board = [row for row in board if any(col == BLACK for col in row)]
    lines_cleared = BOARD_HEIGHT - len(new_board)
    board = [[BLACK for _ in range(BOARD_WIDTH)] for _ in range(lines_cleared)] + new_board

def main():
    clock = pygame.time.Clock()
    falling_piece = Tetromino()
    fall_time = 0

    running = True
    while running:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    falling_piece.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    falling_piece.move(1, 0)
                if event.key == pygame.K_DOWN:
                    falling_piece.move(0, 1)
                if event.key == pygame.K_UP:
                    falling_piece.rotate()

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time >= 500:
            fall_time = 0
            if not falling_piece.collides(0, 1, falling_piece.shape):
                falling_piece.move(0, 1)
            else:
                for row in range(len(falling_piece.shape)):
                    for col in range(len(falling_piece.shape[row])):
                        if falling_piece.shape[row][col]:
                            board[falling_piece.y + row][falling_piece.x + col] = falling_piece.color
                clear_lines()
                falling_piece = Tetromino()
                if falling_piece.collides(0, 0, falling_piece.shape):
                    running = False

        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                pygame.draw.rect(SCREEN, board[row][col],
                                 (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        falling_piece.draw(SCREEN)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
