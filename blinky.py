import pygame

pygame.init()

# Screen setup
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Load Blinky images
pacman_images = []
blinky_images = []
for i in range(1, 3):
    img = pygame.image.load(f'assets/ghost_images/blinky{i}.png').convert_alpha()
    blinky_images.append(pygame.transform.scale(img, (45, 45)))



blinky_counter = 0
blinky_x, blinky_y = 100, 100  # Example position

def draw_blinky(x, y):
    global blinky_counter
    index = (blinky_counter // 10) % len(blinky_images)
    screen.blit(blinky_images[index], (x, y))
    blinky_counter = (blinky_counter + 1) % (len(blinky_images) * 10)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Clear screen with black
    draw_blinky(blinky_x, blinky_y)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
