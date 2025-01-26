import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game objects
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15

# Paddle positions
player1_x, player1_y = 10, (HEIGHT // 2 - PADDLE_HEIGHT // 2)
player2_x, player2_y = WIDTH - 20, (HEIGHT // 2 - PADDLE_HEIGHT // 2)

# Ball position and speed
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx, ball_dy = 4, 4

# Speeds
paddle_speed = 5

# Scores
player1_score = 0
player2_score = 0

# Fonts
font = pygame.font.Font(None, 74)

# Clock
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1_y > 0:
        player1_y -= paddle_speed
    if keys[pygame.K_s] and player1_y < HEIGHT - PADDLE_HEIGHT:
        player1_y += paddle_speed
    if keys[pygame.K_UP] and player2_y > 0:
        player2_y -= paddle_speed
    if keys[pygame.K_DOWN] and player2_y < HEIGHT - PADDLE_HEIGHT:
        player2_y += paddle_speed

    # Update ball position
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball collision with top and bottom walls
    if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
        ball_dy *= -1

    # Ball collision with paddles
    if (player1_x < ball_x < player1_x + PADDLE_WIDTH and player1_y < ball_y < player1_y + PADDLE_HEIGHT) or \
       (player2_x < ball_x + BALL_SIZE < player2_x + PADDLE_WIDTH and player2_y < ball_y < player2_y + PADDLE_HEIGHT):
        ball_dx *= -1

    # Ball out of bounds
    if ball_x <= 0:
        player2_score += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_dx *= -1
    if ball_x >= WIDTH:
        player1_score += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_dx *= -1

    # Draw everything
    screen.fill(BLACK)
    
    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, (player1_x, player1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (player2_x, player2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

    # Draw center line
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Draw scores
    player1_text = font.render(str(player1_score), True, WHITE)
    player2_text = font.render(str(player2_score), True, WHITE)
    screen.blit(player1_text, (WIDTH // 4, 20))
    screen.blit(player2_text, (WIDTH * 3 // 4, 20))

    # Update display
    pygame.display.flip()

    # Frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
