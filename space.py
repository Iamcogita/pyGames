import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Player settings
player_width, player_height = 50, 15
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 50
player_speed = 5
player_projectiles = []
projectile_speed = -10
projectile_size = 5

# Enemy settings
enemies = []
enemy_speed = 1
spawn_timer = 100

# Power-up settings
power_ups = []
power_up_timer = 0
POWER_UP_DURATION = 500

# Score and game state
score = 0
power_up_active = False
power_up_type = None

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = player_width
        self.height = player_height
        self.color = GREEN
        self.speed = player_speed
        self.projectile_size = projectile_size
        self.rate_of_fire = 300  # Time in ms between shots
        self.last_shot_time = 0

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.rate_of_fire:
            self.last_shot_time = current_time
            projectile = Projectile(self.x + self.width // 2, self.y, self.projectile_size)
            player_projectiles.append(projectile)

class Projectile:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = WHITE
        self.speed = projectile_speed

    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

class Enemy:
    def __init__(self, x, y, health=1):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.color = RED
        self.speed = enemy_speed
        self.health = health

    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        if self.health > 1:
            pygame.draw.rect(screen, YELLOW, (self.x, self.y - 5, self.width * (self.health / 3), 5))

class PowerUp:
    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind
        self.width = 15
        self.height = 15
        self.color = GREEN if kind == "speed" else YELLOW if kind == "rate" else WHITE

    def move(self):
        self.y += 3

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

player = Player(player_x, player_y)

def spawn_enemy():
    x = random.randint(0, WIDTH - 40)
    health = random.choice([1, 2, 3]) if random.random() > 0.7 else 1
    enemies.append(Enemy(x, 0, health))

# Game Loop
running = True
while running:
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.shoot()

    # Player movement
    player.move(keys)

    # Move and draw projectiles
    for projectile in player_projectiles[:]:
        projectile.move()
        if projectile.y < 0:
            player_projectiles.remove(projectile)
        projectile.draw()

    # Enemy spawning and movement
    if spawn_timer <= 0:
        spawn_enemy()
        spawn_timer = max(20, 100 - score // 5)  # Faster spawns over time
    else:
        spawn_timer -= 1

    for enemy in enemies[:]:
        enemy.move()
        if enemy.y > HEIGHT:
            enemies.remove(enemy)
            continue
        enemy.draw()
        # Collision with player projectiles
        for projectile in player_projectiles[:]:
            if (enemy.x < projectile.x < enemy.x + enemy.width) and (enemy.y < projectile.y < enemy.y + enemy.height):
                enemy.health -= 1
                player_projectiles.remove(projectile)
                if enemy.health <= 0:
                    enemies.remove(enemy)
                    score += 1
                    break

    # Draw power-ups
    for power_up in power_ups[:]:
        power_up.move()
        power_up.draw()
        if (player.x < power_up.x < player.x + player.width) and (player.y < power_up.y < player.y + player.height):
            power_up_type = power_up.kind
            power_up_timer = POWER_UP_DURATION
            power_up_active = True
            power_ups.remove(power_up)

    # Handle power-ups
    if power_up_active:
        if power_up_type == "speed":
            player.speed = 8
        elif power_up_type == "rate":
            player.rate_of_fire = 150
        elif power_up_type == "size":
            player.projectile_size = 10
        power_up_timer -= 1
        if power_up_timer <= 0:
            power_up_active = False
            player.speed = player_speed
            player.rate_of_fire = 300
            player.projectile_size = projectile_size

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Draw player
    player.draw()

    # Update display
    pygame.display.flip()

    # Frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()