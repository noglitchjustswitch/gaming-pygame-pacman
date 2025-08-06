import pygame
import sys
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
GHOST_SPEED = 3
PACMAN_SPEED = 3
BLACK = (0, 0, 0)
POWER_DURATION = 5000  # 5 seconds

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blinky, Inky & Clyde vs Pac-Man")
clock = pygame.time.Clock()

# Helper to load and scale sprites
def load_scaled(path, size=(50, 50)):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(image, size)

# Load Blinky frames
blinky_frames = [load_scaled(f'assets/ghost_images/blinkyright{n}.png') for n in [1, 2]]
blinky_blue_frames = [load_scaled(f'assets/ghost_images/power{n}.png') for n in [1, 2]]
blinky_eyes = load_scaled('assets/ghost_images/eyes.png')

# Load Inky frames
inky_frames = [load_scaled(f'assets/ghost_images/inkyright{n}.png') for n in [1, 2]]

# Load Clyde frames
clyde_frames = [load_scaled(f'assets/ghost_images/clyderight{n}.png') for n in [1, 2]]

# Load Pac-Man frames
pacman_frames = [load_scaled(f'assets/player_images/pacman{n}.png') for n in [1, 2, 3]]

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

# Ghost house (cage)
HOME_WIDTH, HOME_HEIGHT = 100, 60
home_rect = pygame.Rect(
    WIDTH // 2 - HOME_WIDTH // 2,
    HEIGHT // 2 - HOME_HEIGHT // 2,
    HOME_WIDTH,
    HOME_HEIGHT
)

# Cage collision walls
wall_thickness = 6
opening_width = 70
gap_left = (HOME_WIDTH - opening_width) // 2
gap_right = HOME_WIDTH - gap_left - opening_width
bottom_y = home_rect.bottom - wall_thickness

cage_left_wall = pygame.Rect(home_rect.left, home_rect.top, wall_thickness, HOME_HEIGHT)
cage_right_wall = pygame.Rect(home_rect.right - wall_thickness, home_rect.top, wall_thickness, HOME_HEIGHT)
cage_top_wall = pygame.Rect(home_rect.left, home_rect.top, HOME_WIDTH, wall_thickness)
cage_bottom_left = pygame.Rect(home_rect.left, bottom_y, gap_left, wall_thickness)
cage_bottom_right = pygame.Rect(home_rect.left + gap_left + opening_width, bottom_y, gap_right, wall_thickness)
cage_walls = [cage_left_wall, cage_right_wall, cage_top_wall, cage_bottom_left, cage_bottom_right]

def prevent_wall_collision(rect, dx, dy, walls):
    future_rect = rect.move(dx, dy)
    for wall in walls:
        if future_rect.colliderect(wall):
            return 0, 0
    return dx, dy

# Sprites & positions
blinky_rect = blinky_frames[0].get_rect(topleft=(100, 100))
inky_rect = inky_frames[0].get_rect(topleft=(150, 100))
clyde_rect = clyde_frames[0].get_rect(topleft=(200, 100))
pacman_rect = pacman_frames[0].get_rect(topleft=(400, 300))
pacman_pos_x = float(pacman_rect.x)
pacman_pos_y = float(pacman_rect.y)

# Animation indices
blinky_frame_index = 0
inky_frame_index = 0
clyde_frame_index = 0
pacman_frame_index = 0
blinky_anim_timer = 0
inky_anim_timer = 0
clyde_anim_timer = 0
pacman_anim_timer = 0

BLINKY_ANIM_SPEED = 200
INKY_ANIM_SPEED = 200
CLYDE_ANIM_SPEED = 200
PACMAN_ANIM_SPEED = 150

# States
blinky_state = "normal"
inky_state = "normal"
clyde_state = "normal"
power_timer = 0
pacman_caught = False

# Clyde random movement
clyde_dir = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
clyde_change_timer = 0

# Main loop
running = True
while running:
    dt = clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # === Ghost Movement ===

    # Blinky (WASD)
    blinky_dx = blinky_dy = 0
    if keys[pygame.K_a]:
        blinky_dx = -GHOST_SPEED
    if keys[pygame.K_d]:
        blinky_dx = GHOST_SPEED
    if keys[pygame.K_w]:
        blinky_dy = -GHOST_SPEED
    if keys[pygame.K_s]:
        blinky_dy = GHOST_SPEED
    if blinky_state != "eyes":
        blinky_dx, blinky_dy = prevent_wall_collision(blinky_rect, blinky_dx, blinky_dy, cage_walls)
    blinky_rect.x += blinky_dx
    blinky_rect.y += blinky_dy

    # Inky (IJKL)
    inky_dx = inky_dy = 0
    if keys[pygame.K_j]:
        inky_dx = -GHOST_SPEED
    if keys[pygame.K_l]:
        inky_dx = GHOST_SPEED
    if keys[pygame.K_i]:
        inky_dy = -GHOST_SPEED
    if keys[pygame.K_k]:
        inky_dy = GHOST_SPEED
    if inky_state != "eyes":
        inky_dx, inky_dy = prevent_wall_collision(inky_rect, inky_dx, inky_dy, cage_walls)
    inky_rect.x += inky_dx
    inky_rect.y += inky_dy

    # Clyde (random)
    clyde_change_timer += dt
    if clyde_change_timer > 1000:
        clyde_change_timer = 0
        clyde_dir = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
    clyde_dx = clyde_dir[0] * GHOST_SPEED
    clyde_dy = clyde_dir[1] * GHOST_SPEED
    if clyde_state != "eyes":
        clyde_dx, clyde_dy = prevent_wall_collision(clyde_rect, clyde_dx, clyde_dy, cage_walls)
    clyde_rect.x += clyde_dx
    clyde_rect.y += clyde_dy

    # === Manual Respawn ===
    def respawn_ghost(state, key, ghost_rect, ghost_name):
        if state == "eyes" and keys[key] and home_rect.collidepoint(ghost_rect.center):
            ghost_rect.midtop = (home_rect.centerx, home_rect.bottom + 2)  # Move below cage
            print(f"{ghost_name} manually respawned.")
            return "normal"
        return state

    blinky_state = respawn_ghost(blinky_state, pygame.K_SPACE, blinky_rect, "Blinky")
    inky_state = respawn_ghost(inky_state, pygame.K_RETURN, inky_rect, "Inky")
    clyde_state = respawn_ghost(clyde_state, pygame.K_BACKSPACE, clyde_rect, "Clyde")


    # === Pac-Man Movement ===
    if not pacman_caught:
        pacman_anim_timer += dt
        if pacman_anim_timer >= PACMAN_ANIM_SPEED:
            pacman_anim_timer = 0
            pacman_frame_index = (pacman_frame_index + 1) % len(pacman_frames)

    pacman_dx, pacman_dy = 0, 0
    if keys[pygame.K_LEFT]:
        pacman_dx = -PACMAN_SPEED
    elif keys[pygame.K_RIGHT]:
        pacman_dx = PACMAN_SPEED
    if keys[pygame.K_UP]:
        pacman_dy = -PACMAN_SPEED
    elif keys[pygame.K_DOWN]:
        pacman_dy = PACMAN_SPEED

    pacman_pos_x += pacman_dx
    pacman_pos_y += pacman_dy
    pacman_pos_x = max(0, min(WIDTH - pacman_rect.width, pacman_pos_x))
    pacman_pos_y = max(0, min(HEIGHT - pacman_rect.height, pacman_pos_y))
    pacman_rect.x = int(pacman_pos_x)
    pacman_rect.y = int(pacman_pos_y)

    # Animation timers
    blinky_anim_timer += dt
    inky_anim_timer += dt
    clyde_anim_timer += dt
    if blinky_anim_timer >= BLINKY_ANIM_SPEED:
        blinky_anim_timer = 0
        blinky_frame_index = (blinky_frame_index + 1) % 2
    if inky_anim_timer >= INKY_ANIM_SPEED:
        inky_anim_timer = 0
        inky_frame_index = (inky_frame_index + 1) % 2
    if clyde_anim_timer >= CLYDE_ANIM_SPEED:
        clyde_anim_timer = 0
        clyde_frame_index = (clyde_frame_index + 1) % 2

    # === Power Pellet ===
    if not power_pellet_eaten and pacman_rect.colliderect(power_pellet_rect):
        power_pellet_eaten = True
        blinky_state = inky_state = clyde_state = "vulnerable"
        power_timer = POWER_DURATION

    if blinky_state == "vulnerable" or inky_state == "vulnerable" or clyde_state == "vulnerable":
        power_timer -= dt
        if power_timer <= 0:
            if blinky_state == "vulnerable": blinky_state = "normal"
            if inky_state == "vulnerable": inky_state = "normal"
            if clyde_state == "vulnerable": clyde_state = "normal"

    # === Ghost Eaten ===
    if blinky_state == "vulnerable" and pacman_rect.colliderect(blinky_rect):
        blinky_state = "eyes"
    if inky_state == "vulnerable" and pacman_rect.colliderect(inky_rect):
        inky_state = "eyes"
    if clyde_state == "vulnerable" and pacman_rect.colliderect(clyde_rect):
        clyde_state = "eyes"

    # === Pac-Man Caught ===
    if not pacman_caught:
        if blinky_state == "normal" and pacman_rect.colliderect(blinky_rect):
            pacman_caught = True
        elif inky_state == "normal" and pacman_rect.colliderect(inky_rect):
            pacman_caught = True
        elif clyde_state == "normal" and pacman_rect.colliderect(clyde_rect):
            pacman_caught = True

    # === Drawing ===
    cage_x = home_rect.x
    cage_y = home_rect.y
    cage_w = HOME_WIDTH
    cage_h = HOME_HEIGHT

    # Draw cage walls
    pygame.draw.rect(screen, (255, 255, 255), (cage_x, cage_y, cage_w, wall_thickness))
    pygame.draw.rect(screen, (255, 255, 255), (cage_x, cage_y, wall_thickness, cage_h))
    pygame.draw.rect(screen, (255, 255, 255), (cage_x + cage_w - wall_thickness, cage_y, wall_thickness, cage_h))
    pygame.draw.rect(screen, (255, 255, 255), (cage_x, bottom_y, gap_left, wall_thickness))
    pygame.draw.rect(screen, (255, 255, 255), (cage_x + gap_left + opening_width, bottom_y, gap_right, wall_thickness))

    if not power_pellet_eaten:
        pygame.draw.circle(screen, (255, 255, 0), power_pellet_center, POWER_RADIUS)

    # Draw ghosts
    def draw_ghost(state, frame_index, rect, normal_frames):
        if state == "eyes":
            screen.blit(blinky_eyes, rect)
        elif state == "vulnerable":
            screen.blit(blinky_blue_frames[frame_index], rect)
        else:
            screen.blit(normal_frames[frame_index], rect)

    draw_ghost(blinky_state, blinky_frame_index, blinky_rect, blinky_frames)
    draw_ghost(inky_state, inky_frame_index, inky_rect, inky_frames)
    draw_ghost(clyde_state, clyde_frame_index, clyde_rect, clyde_frames)

    if not pacman_caught:
        screen.blit(pacman_frames[pacman_frame_index], pacman_rect)
    else:
        font = pygame.font.SysFont(None, 48)
        text = font.render("Pac-Man Caught!", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()
