import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 448, 576  # Classic Pac-Man size
TILE_SIZE = 32
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Clone")

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Player settings
player_size = TILE_SIZE
player_speed = 4

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = YELLOW
        self.direction = "STOP"
        self.lives = 3
        self.score = 0

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2), TILE_SIZE // 2 - 2)

    def move(self, maze):
        next_x, next_y = self.x, self.y
        if self.direction == "LEFT":
            next_x -= player_speed
        elif self.direction == "RIGHT":
            next_x += player_speed
        elif self.direction == "UP":
            next_y -= player_speed
        elif self.direction == "DOWN":
            next_y += player_speed

        if not self.collides_with_walls(next_x, next_y, maze):
            self.x = next_x
            self.y = next_y

    def collides_with_walls(self, x, y, maze):
        for wall in maze:
            if wall.collidepoint(x + TILE_SIZE // 2, y + TILE_SIZE // 2):
                return True
        return False

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.direction = random.choice(["LEFT", "RIGHT", "UP", "DOWN"])

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, TILE_SIZE, TILE_SIZE))

    def move(self, maze):
        next_x, next_y = self.x, self.y
        if self.direction == "LEFT":
            next_x -= player_speed // 2
        elif self.direction == "RIGHT":
            next_x += player_speed // 2
        elif self.direction == "UP":
            next_y -= player_speed // 2
        elif self.direction == "DOWN":
            next_y += player_speed // 2

        if not self.collides_with_walls(next_x, next_y, maze):
            self.x = next_x
            self.y = next_y
        else:
            self.direction = random.choice(["LEFT", "RIGHT", "UP", "DOWN"])

    def collides_with_walls(self, x, y, maze):
        for wall in maze:
            if wall.collidepoint(x + TILE_SIZE // 2, y + TILE_SIZE // 2):
                return True
        return False

class Pellet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = WHITE

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2), 4)

# Create maze walls
maze = []
for y in range(0, HEIGHT, TILE_SIZE):
    for x in range(0, WIDTH, TILE_SIZE):
        if x == 0 or y == 0 or x == WIDTH - TILE_SIZE or y == HEIGHT - TILE_SIZE or (x % (TILE_SIZE * 4) == 0 and y % (TILE_SIZE * 3) == 0):
            maze.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

# Create player, ghosts, and pellets
player = Player(WIDTH // 2, HEIGHT - TILE_SIZE * 2)
ghosts = [Ghost(TILE_SIZE, TILE_SIZE, RED), Ghost(WIDTH - TILE_SIZE * 2, TILE_SIZE, BLUE)]
pellets = [Pellet(x, y) for x in range(TILE_SIZE, WIDTH - TILE_SIZE, TILE_SIZE) for y in range(TILE_SIZE, HEIGHT - TILE_SIZE, TILE_SIZE) if random.random() < 0.2]

# Game Loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.direction = "LEFT"
            elif event.key == pygame.K_RIGHT:
                player.direction = "RIGHT"
            elif event.key == pygame.K_UP:
                player.direction = "UP"
            elif event.key == pygame.K_DOWN:
                player.direction = "DOWN"

    # Update player and ghost positions
    player.move(maze)
    for ghost in ghosts:
        ghost.move(maze)

    # Check collisions with ghosts
    for ghost in ghosts:
        if abs(player.x - ghost.x) < TILE_SIZE and abs(player.y - ghost.y) < TILE_SIZE:
            player.lives -= 1
            player.x, player.y = WIDTH // 2, HEIGHT - TILE_SIZE * 2
            if player.lives <= 0:
                running = False

    # Check collisions with pellets
    for pellet in pellets[:]:
        if abs(player.x - pellet.x) < TILE_SIZE // 2 and abs(player.y - pellet.y) < TILE_SIZE // 2:
            pellets.remove(pellet)
            player.score += 10

    # Draw maze, player, ghosts, and pellets
    for wall in maze:
        pygame.draw.rect(screen, BLUE, wall)

    player.draw()

    for ghost in ghosts:
        ghost.draw()

    for pellet in pellets:
        pellet.draw()

    # Display score and lives
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {player.score}", True, WHITE)
    lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 120, 10))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()
