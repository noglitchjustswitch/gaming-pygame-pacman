import pygame
import sys
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
BLINKY_SPEED = 5
PACMAN_SPEED = 3
BLACK = (0, 0, 0)
POWER_DURATION = 5000  # 5 seconds

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Inky vs Pac-Man with Power Pellet")
clock = pygame.time.Clock()

# Helper to load and scale sprites
def load_scaled(path, size=(50, 50)):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(image, size)

# Load Blinky frames
blinky_frames = [
    load_scaled(f'assets/ghost_images/inkyright{n}.png') for n in [1, 2]
]
blinky_blue_frames = [
    load_scaled(f'assets/ghost_images/power.png') for n in [1, 2]
]
blinky_eyes = load_scaled('assets/ghost_images/eyes.png')  # Eyes sprite

# Load Pac-Man frames
pacman_frames = [
    load_scaled(f'assets/player_images/pacman{n}.png') for n in [1, 2, 3]
]

# Power Pellet setup
POWER_RADIUS = 15
power_pellet_center = (WIDTH // 2, HEIGHT // 2)
power_pellet_rect = pygame.Rect(
    power_pellet_center[0] - POWER_RADIUS,
    power_pellet_center[1] - POWER_RADIUS,
    POWER_RADIUS * 2,
    POWER_RADIUS * 2
)
power_pellet_eaten = False

# Home base setup
HOME_BASE_WIDTH, HOME_BASE_HEIGHT = 60, 60
blinky_home_rect = pygame.Rect(
    WIDTH // 2 - HOME_BASE_WIDTH // 2,
    HEIGHT // 2 - HOME_BASE_HEIGHT // 2,
    HOME_BASE_WIDTH,
    HOME_BASE_HEIGHT
)

# Rects and animation indices
blinky_rect = blinky_frames[0].get_rect(topleft=(100, 100))
pacman_rect = pacman_frames[0].get_rect(topleft=(400, 300))
pacman_pos_x = float(pacman_rect.x)
pacman_pos_y = float(pacman_rect.y)

blinky_frame_index = 0
pacman_frame_index = 0
blinky_anim_timer = 0
pacman_anim_timer = 0
BLINKY_ANIM_SPEED = 200
PACMAN_ANIM_SPEED = 150

# Movement and timers
pacman_dx, pacman_dy = 0, 0
direction_change_timer = 0
DIRECTION_CHANGE_INTERVAL = 1000

# States
blinky_state = "normal"  # 'normal', 'vulnerable', 'eyes'
blinky_eye_speed = 4
power_timer = 0
pacman_caught = False

# Main game loop
running = True
while running:
    dt = clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # === BLINKY MOVEMENT (player-controlled when normal/vulnerable/eyes) ===
    if blinky_state in ["normal", "vulnerable", "eyes"]:
        if keys[pygame.K_LEFT]:
            blinky_rect.x -= BLINKY_SPEED
        if keys[pygame.K_RIGHT]:
            blinky_rect.x += BLINKY_SPEED
        if keys[pygame.K_UP]:
            blinky_rect.y -= BLINKY_SPEED
        if keys[pygame.K_DOWN]:
            blinky_rect.y += BLINKY_SPEED

    # Keep Blinky in bounds
    blinky_rect.x = max(0, min(WIDTH - blinky_rect.width, blinky_rect.x))
    blinky_rect.y = max(0, min(HEIGHT - blinky_rect.height, blinky_rect.y))

    # === Manual respawn of Blinky when in eyes mode by pressing Space, only if inside home base ===
    if blinky_state == "eyes" and keys[pygame.K_SPACE]:
        if blinky_home_rect.collidepoint(blinky_rect.center):
            blinky_state = "normal"
            print("Inky manually respawned inside home base.")


    # === PAC-MAN ANIMATION & MOVEMENT ===
    if not pacman_caught:
        pacman_anim_timer += dt
    if pacman_anim_timer >= PACMAN_ANIM_SPEED:
        pacman_anim_timer = 0
        pacman_frame_index = (pacman_frame_index + 1) % len(pacman_frames)

    if blinky_state == "vulnerable":
        dx = blinky_rect.centerx - pacman_rect.centerx
        dy = blinky_rect.centery - pacman_rect.centery
        distance = (dx**2 + dy**2) ** 0.5
        if distance != 0:
            pacman_dx = PACMAN_SPEED * dx / distance
            pacman_dy = PACMAN_SPEED * dy / distance
        else:
            pacman_dx, pacman_dy = 0, 0
    else:
        dx_blinky = blinky_rect.centerx - pacman_rect.centerx
        dy_blinky = blinky_rect.centery - pacman_rect.centery
        dist_blinky = (dx_blinky**2 + dy_blinky**2) ** 0.5

        dx_pellet = power_pellet_center[0] - pacman_rect.centerx
        dy_pellet = power_pellet_center[1] - pacman_rect.centery
        dist_pellet = (dx_pellet**2 + dy_pellet**2) ** 0.5

        RUN_AWAY_DISTANCE = 150

        if not power_pellet_eaten:
            if dist_blinky < RUN_AWAY_DISTANCE and dist_blinky != 0:
                pacman_dx = -PACMAN_SPEED * dx_blinky / dist_blinky
                pacman_dy = -PACMAN_SPEED * dy_blinky / dist_blinky
            else:
                if dist_pellet != 0:
                    pacman_dx = PACMAN_SPEED * dx_pellet / dist_pellet
                    pacman_dy = PACMAN_SPEED * dy_pellet / dist_pellet
                else:
                    pacman_dx, pacman_dy = 0, 0
        else:
            direction_change_timer += dt
            if direction_change_timer >= DIRECTION_CHANGE_INTERVAL:
                direction_change_timer = 0
                direction = random.choice(['left', 'right', 'up', 'down', 'stop'])
                if direction == 'left':
                    pacman_dx, pacman_dy = -PACMAN_SPEED, 0
                elif direction == 'right':
                    pacman_dx, pacman_dy = PACMAN_SPEED, 0
                elif direction == 'up':
                    pacman_dx, pacman_dy = 0, -PACMAN_SPEED
                elif direction == 'down':
                    pacman_dx, pacman_dy = 0, PACMAN_SPEED
                else:
                    pacman_dx, pacman_dy = 0, 0

    pacman_pos_x += pacman_dx
    pacman_pos_y += pacman_dy
    pacman_pos_x = max(0, min(WIDTH - pacman_rect.width, pacman_pos_x))
    pacman_pos_y = max(0, min(HEIGHT - pacman_rect.height, pacman_pos_y))
    pacman_rect.x = int(pacman_pos_x)
    pacman_rect.y = int(pacman_pos_y)

    # === BLINKY ANIMATION ===
    blinky_anim_timer += dt
    if blinky_anim_timer >= BLINKY_ANIM_SPEED:
        blinky_anim_timer = 0
        blinky_frame_index = (blinky_frame_index + 1) % 2

    # === Power Pellet ===
    if not power_pellet_eaten and pacman_rect.colliderect(power_pellet_rect):
        power_pellet_eaten = True
        blinky_state = "vulnerable"
        power_timer = POWER_DURATION
        print("Power pellet eaten! Inky is vulnerable!")

    # === Power Timer Handling ===
    if blinky_state == "vulnerable":
        power_timer -= dt
        if power_timer <= 0:
            blinky_state = "normal"
            print("Inky is back to normal.")

    # === Blinky Eaten by Pac-Man ===
    if blinky_state == "vulnerable" and pacman_rect.colliderect(blinky_rect):
        blinky_state = "eyes"
        print("Pac-Man ate Inky! Inky is returning to base as eyes.")

    # === Blinky Catches Pac-Man ===
    if blinky_state == "normal" and blinky_rect.colliderect(pacman_rect):
        pacman_caught = True
        pacman_dx = pacman_dy = 0
        print("Inky caught Pac-Man!")

    # === DRAWING ===
    # Draw home base
    pygame.draw.rect(screen, (60, 60, 60), blinky_home_rect, border_radius=10)

    # Power Pellet
    if not power_pellet_eaten:
        pygame.draw.circle(screen, (255, 255, 0), power_pellet_center, POWER_RADIUS)

    # Draw Blinky
    if blinky_state == "eyes":
        screen.blit(blinky_eyes, blinky_rect)
    elif blinky_state == "vulnerable":
        screen.blit(blinky_blue_frames[blinky_frame_index], blinky_rect)
    else:
        screen.blit(blinky_frames[blinky_frame_index], blinky_rect)

    # Draw Pac-Man
    if not pacman_caught:
        screen.blit(pacman_frames[pacman_frame_index], pacman_rect)

    # End text
    if pacman_caught:
        font = pygame.font.SysFont(None, 48)
        text = font.render("Pac-Man Caught!", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()
