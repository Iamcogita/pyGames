import pygame
import math
from levels import LEVELS  # Importing levels from a separate file

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game settings
FOV = math.pi / 3  # Field of view
NUM_RAYS = 120  # Number of rays cast
MAX_DEPTH = 800  # Maximum ray distance
SCALE = SCREEN_WIDTH // NUM_RAYS
PLAYER_SPEED = 3
ROTATION_SPEED = 0.002  # Adjusted for smoother mouse control
MOUSE_SENSITIVITY = 0.002

# Map settings
TILE_SIZE = 64
current_level = 0
MAP = LEVELS[current_level]["map"]  # Get map from levels
MAP_WIDTH = len(MAP[0])
MAP_HEIGHT = len(MAP)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Doom-like Sandbox Game")

# Player class
class Player:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.z = 0  # Simulate vertical movement
        self.angle = angle
        self.view_offset = 0  # For vertical look

    def move(self, keys):
        # Calculate movement vectors
        dx = math.cos(self.angle) * PLAYER_SPEED
        dy = math.sin(self.angle) * PLAYER_SPEED
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)

        # Move forward
        if keys[pygame.K_w]:
            if MAP[int((self.y + dy) // TILE_SIZE)][int(self.x // TILE_SIZE)] != "#":
                self.y += dy
            if MAP[int(self.y // TILE_SIZE)][int((self.x + dx) // TILE_SIZE)] != "#":
                self.x += dx

        # Move backward
        if keys[pygame.K_s]:
            if MAP[int((self.y - dy) // TILE_SIZE)][int(self.x // TILE_SIZE)] != "#":
                self.y -= dy
            if MAP[int(self.y // TILE_SIZE)][int((self.x - dx) // TILE_SIZE)] != "#":
                self.x -= dx

        # Strafe left
        if keys[pygame.K_a]:
            if MAP[int((self.y - cos_a * PLAYER_SPEED) // TILE_SIZE)][int(self.x // TILE_SIZE)] != "#":
                self.y -= cos_a * PLAYER_SPEED
            if MAP[int(self.y // TILE_SIZE)][int((self.x + sin_a * PLAYER_SPEED) // TILE_SIZE)] != "#":
                self.x += sin_a * PLAYER_SPEED

        # Strafe right
        if keys[pygame.K_d]:
            if MAP[int((self.y + cos_a * PLAYER_SPEED) // TILE_SIZE)][int(self.x // TILE_SIZE)] != "#":
                self.y += cos_a * PLAYER_SPEED
            if MAP[int(self.y // TILE_SIZE)][int((self.x - sin_a * PLAYER_SPEED) // TILE_SIZE)] != "#":
                self.x -= sin_a * PLAYER_SPEED

        # Vertical movement (simulating stairs or elevation)
        if keys[pygame.K_SPACE]:  # Ascend
            self.z = min(self.z + 1, 50)
        if keys[pygame.K_LSHIFT]:  # Descend
            self.z = max(self.z - 1, 0)

    def rotate_with_mouse(self):
        mouse_dx, mouse_dy = pygame.mouse.get_rel()  # Get mouse movement (x, y)
        self.angle += mouse_dx * MOUSE_SENSITIVITY
        self.view_offset += mouse_dy * 5  # Adjust vertical look
        self.view_offset = max(-100, min(100, self.view_offset))  # Limit range

# Raycasting function
def cast_rays(player):
    rays = []
    start_angle = player.angle - FOV / 2
    for ray in range(NUM_RAYS):
        angle = start_angle + ray * (FOV / NUM_RAYS)
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)

        # Ray tracing
        for depth in range(1, MAX_DEPTH):
            target_x = player.x + depth * cos_a
            target_y = player.y + depth * sin_a

            if (
                0 <= int(target_x // TILE_SIZE) < MAP_WIDTH
                and 0 <= int(target_y // TILE_SIZE) < MAP_HEIGHT
            ):
                if MAP[int(target_y // TILE_SIZE)][int(target_x // TILE_SIZE)] == "#":
                    depth *= math.cos(player.angle - angle)  # Remove fish-eye effect
                    height = TILE_SIZE * SCREEN_HEIGHT / (depth + 0.001)
                    height *= 1 - (player.z / 100)  # Simulate elevation
                    color = 255 / (1 + depth * depth * 0.0001)
                    y_offset = player.view_offset  # Apply vertical look
                    rays.append((ray * SCALE, SCREEN_HEIGHT // 2 - height // 2 + y_offset, SCALE, height, color))
                    break
    return rays

# Draw 3D view
def draw_3d(rays):
    for ray in rays:
        x, y, width, height, color = ray
        pygame.draw.rect(screen, (color, color, color), (x, y, width, height))

# Draw top-down map
def draw_top_down():
    mini_map_scale = 40 / (MAP_WIDTH * TILE_SIZE)  # Fit the map within 40px width
    mini_tile_size = TILE_SIZE * mini_map_scale

    for y, row in enumerate(MAP):
        for x, char in enumerate(row):
            color = GRAY if char == "#" else BLACK
            rect = pygame.Rect(
                x * mini_tile_size,
                y * mini_tile_size,
                mini_tile_size,
                mini_tile_size,
            )
            pygame.draw.rect(screen, color, rect)

    # Draw player starting position (red)
    start_pos = LEVELS[current_level]["start"]
    pygame.draw.rect(
        screen,
        RED,
        (
            start_pos[0] * mini_tile_size,
            start_pos[1] * mini_tile_size,
            mini_tile_size,
            mini_tile_size,
        ),
    )

    # Draw goal position (green)
    goal_pos = LEVELS[current_level]["goal"]
    pygame.draw.rect(
        screen,
        GREEN,
        (
            goal_pos[0] * mini_tile_size,
            goal_pos[1] * mini_tile_size,
            mini_tile_size,
            mini_tile_size,
        ),
    )

# Draw timer and legend
def draw_ui(timer, message=None):
    # Draw timer
    font = pygame.font.Font(None, 36)
    timer_text = font.render(f"Time: {timer:.2f}s", True, WHITE)
    timer_rect = pygame.Rect((SCREEN_WIDTH - 100) // 2, 10, 100, 60)
    pygame.draw.rect(screen, BLACK, timer_rect)
    screen.blit(timer_text, (timer_rect.x + 10, timer_rect.y + 10))

    # Draw message if any
    if message:
        message_text = font.render(message, True, GREEN if message == "GOAL" else RED)
        screen.blit(message_text, (SCREEN_WIDTH // 2 - message_text.get_width() // 2, SCREEN_HEIGHT // 2))

    # Draw legend
    legend_text = [
        "PRESS ENTER TO RETRY",
        "PRESS ESC TO QUIT",
    ]
    for i, text in enumerate(legend_text):
        legend_rendered = font.render(text, True, WHITE)
        screen.blit(legend_rendered, (10, SCREEN_HEIGHT - 40 * (len(legend_text) - i)))

# Main function
def main():
    global current_level, MAP, MAP_WIDTH, MAP_HEIGHT

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    timer = 0
    message = None
    message_time = None

    player_start = LEVELS[current_level]["start"]
    player = Player(player_start[0] * TILE_SIZE + TILE_SIZE // 2, player_start[1] * TILE_SIZE + TILE_SIZE // 2, 0)

    # Enable mouse input
    pygame.mouse.set_visible(False)  # Hide mouse cursor
    pygame.event.set_grab(True)  # Lock mouse to the window

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Restart the game
                current_level = 0
                MAP = LEVELS[current_level]["map"]
                MAP_WIDTH = len(MAP[0])
                MAP_HEIGHT = len(MAP)
                player_start = LEVELS[current_level]["start"]
                player = Player(player_start[0] * TILE_SIZE + TILE_SIZE // 2, player_start[1] * TILE_SIZE + TILE_SIZE // 2, 0)
                start_time = pygame.time.get_ticks()

        # Update timer
        timer = (pygame.time.get_ticks() - start_time) / 1000

        # Handle movement
        keys = pygame.key.get_pressed()
        player.move(keys)
        player.rotate_with_mouse()

        # Check if player reaches the goal
        goal_pos = LEVELS[current_level]["goal"]
        if int(player.x // TILE_SIZE) == goal_pos[0] and int(player.y // TILE_SIZE) == goal_pos[1]:
            if current_level + 1 < len(LEVELS):
                current_level += 1
                MAP = LEVELS[current_level]["map"]
                MAP_WIDTH = len(MAP[0])
                MAP_HEIGHT = len(MAP)
                player_start = LEVELS[current_level]["start"]
                player = Player(player_start[0] * TILE_SIZE + TILE_SIZE // 2, player_start[1] * TILE_SIZE + TILE_SIZE // 2, 0)
                start_time = pygame.time.get_ticks()
                message = "GOAL"
                message_time = pygame.time.get_ticks()
            else:
                message = "YOU WIN"
                message_time = pygame.time.get_ticks()
        
        # Display message for a short duration
        if message_time and pygame.time.get_ticks() - message_time > (2000 if message == "GOAL" else 4000):
            if message == "YOU WIN":
                running = False
            message = None
            message_time = None

        # Raycasting and rendering
        rays = cast_rays(player)
        draw_3d(rays)
        draw_top_down()
        draw_ui(timer, message)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()