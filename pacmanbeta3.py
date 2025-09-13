# Build Pac-Man from Scratch in Python with Pygame!!
import copy
from board import boards
import pygame
import math

pygame.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 950
ANIM_SPEED = 200
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
clock = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
pygame.display.set_caption('Pac-Man')
flicker_timer = 0
flicker_interval = 300  # milliseconds (adjust this to change flicker speed)
flicker_state = False
level = copy.deepcopy(boards)
color = 'blue'
color_won = 'white'
color_normal = 'blue'
board_color_speed = 2
start = pygame.mixer.Sound('assets/Sounds/start.wav')
death = pygame.mixer.Sound('assets/Sounds/death_0.wav')
scared = pygame.mixer.Sound('assets/Sounds/fright.wav')
blinky_eyes = pygame.mixer.Sound('assets/Sounds/eyes.wav')
pinky_eyes = pygame.mixer.Sound('assets/Sounds/eyes.wav')
inky_eyes = pygame.mixer.Sound('assets/Sounds/eyes.wav')
clyde_eyes = pygame.mixer.Sound('assets/Sounds/eyes.wav')
blinky_eaten_sound = pygame.mixer.Sound('assets/Sounds/eat_ghost.wav')
pinky_eaten_sound = pygame.mixer.Sound('assets/Sounds/eat_ghost.wav')
inky_eaten_sound = pygame.mixer.Sound('assets/Sounds/eat_ghost.wav')
clyde_eaten_sound = pygame.mixer.Sound('assets/Sounds/eat_ghost.wav')
eat_dot = pygame.mixer.Sound('assets/Sounds/eat_dot_0.wav')
siren = pygame.mixer.Sound('assets/Sounds/siren0.wav')
intermission = pygame.mixer.Sound('assets/Sounds/intermission.wav')
eat_fruit = pygame.mixer.Sound('assets/Sounds/eat_fruit.wav')
siren_playing = False
blinky_eaten_played = False
inky_eaten_played = False
pinky_eaten_played = False
clyde_eaten_played = False
death_played = False
start_played = False
scared_played = False
start.play()
start_played = False
blinky_eyes_played = False
inky_eyes_played = False
pinky_eyes_played = False
clyde_eyes_played = False
intermission_played = False
PI = math.pi
player_images = []
ghost_images = []
for i in range(1, 4):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/pacman{i}h.png'), (45, 45)))
for i in range(1, 2):
    ghost_images.append(pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blinkyright{i}.png'), (45, 45)))
def load_scaled(path, size=(45, 45)):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(image, size)
#blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blinkyright1.png'), (45, 45))
blinky_frames = [load_scaled(f'assets/ghost_images/blinkyright{n}.png') for n in [1, 2]]
pacman1 = pygame.transform.scale(pygame.image.load(f'assets/player_images/pacman1.png'), (38, 45))
pacman2 = pygame.transform.scale(pygame.image.load(f'assets/player_images/pacman2.png'), (25, 45))
#pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pinkyright1.png'), (45, 45))
pinky_frames = [load_scaled(f'assets/ghost_images/pinkyright{n}.png') for n in [1, 2]]
#inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/inkyright1.png'), (45, 45))
inky_frames = [load_scaled(f'assets/ghost_images/inkyright{n}.png') for n in [1, 2]]
#clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/clyderight1.png'), (45, 45))
clyde_frames = [load_scaled(f'assets/ghost_images/clyderight{n}.png') for n in [1, 2]]
spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/power1.png'), (45, 45))
spooked_white_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerwhite.png'), (45, 45))
dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/eyesright.png'), (45, 45))
lives_img = pygame.transform.scale(pygame.image.load(f'assets/player_images/lives.png'), (35, 35))
icon = pygame.transform.scale(pygame.image.load(f'assets/player_images/pacman1.png'), (50, 50))
cherry_img = pygame.transform.scale(pygame.image.load(f'assets/fruits/cherry.png'), (45, 45))
# Global dictionary to store ghost eye images per direction
EYE_IMAGES = {
    0: pygame.transform.scale(pygame.image.load('assets/ghost_images/eyesright.png'), (45, 45)),
    1: pygame.transform.scale(pygame.image.load('assets/ghost_images/eyesleft.png'), (45, 45)),
    2: pygame.transform.scale(pygame.image.load('assets/ghost_images/eyesup.png'), (45, 45)),
    3: pygame.transform.scale(pygame.image.load('assets/ghost_images/eyesdown.png'), (45, 45)),
}

pygame.display.set_icon(icon)
player_x = 430
player_y = 663
direction = 0
blinky_x = 430
blinky_y = 330
blinky_direction = 0
inky_x = 370
inky_y = 420
inky_direction = 2
pinky_x = 430
pinky_y = 420
pinky_direction = 2
clyde_x = 490
clyde_y = 420
clyde_direction = 2
cherry_x = 434
cherry_y = 495
cherry_rect = cherry_img.get_rect(topleft=(cherry_x, cherry_y))
cherry_collected = False
cherry_timer = 0
CHERRY_RESPAWN_TIME = 20_000
counter = 0
flicker = False
# R, L, U, D
turns_allowed = [False, False, False, False]
direction_command = 0
current_spooked = spooked_img
player_speed = 2
score = 0
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False]
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y), scared_played]
blinky_dead = False
inky_dead = False
clyde_dead = False
pinky_dead = False
blinky_box = False
inky_box = False
clyde_box = False
pinky_box = False
moving = False
ghost_speeds = [2, 2, 2, 2]
startup_counter = 0
lives = 3
cherry = 1
game_over = False
game_won = False
first_loop_done = False

class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id, anim_timer):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()        
        self.animation_timer = anim_timer
        self.frame_index = 0
        self.rect = self.draw()
        

    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            #screen.blit(self.img, (self.x_pos, self.y_pos))
            self.get_frame_index()
            screen.blit(self.img[self.frame_index], (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(current_spooked, (self.x_pos, self.y_pos))
        else:
            dead_img = EYE_IMAGES[self.direction]
            screen.blit(dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect
   
    def get_frame_index(self):
        if self.animation_timer >= ANIM_SPEED:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % 2

    def check_collisions(self):
        # R, L, U, D
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box

    def move_clyde(self):
    # r, l, u, d
    # clyde is going to turn whenever advantageous for pursuit
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
                    
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
                    
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed    
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed            
        
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
    
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos = -30
        return self.x_pos, self.y_pos, self.direction

    def move_blinky(self):
    # r, l, u, d
    # blinky is going to turn whenever colliding with walls, otherwise continue sraight
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
                    
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
                    
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed    
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed            
        
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed 
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos = -30
        return self.x_pos, self.y_pos, self.direction

    def move_inky(self):
        # r, l, u, d
        # inky turns up or down at any point to pursue, but left and right only on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
                    
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
                    
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed    
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed            
        
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed 
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos = -30
        return self.x_pos, self.y_pos, self.direction

    def move_pinky(self):
    # r, l, u, d
    # pinky is going to turn left or right whenever advantageous, but up or down only on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
                    
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
                    
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed    
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed            
        
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed 
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos = -30
        return self.x_pos, self.y_pos, self.direction

def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(lives_img, (35, 35)), (650 + i * 40, 915))
    for i in range(cherry):
        screen.blit(pygame.transform.scale(cherry_img, (35, 35)), (150 + i * 40, 915))
    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300], 0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('GAME OVER! Space bar to restart!', True, 'red')
        screen.blit(gameover_text, (100, 300))
    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300], 0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gamewon_text = font.render('Victory! Space bar to restart!', True, 'green')
        screen.blit(gamewon_text, (100, 300))

        
    
        

def toggle_color(color):
    if game_won:
        color_to_use = color_won if color == color_normal else color_normal
    else:
        color_to_use = color_normal
    return color_to_use

def toggle_siren(enable):
    if enable:
        siren.play(loops=-1)
    else:
        siren.stop()
    enable = not enable
    return enable

 

def check_collisions(scor, power, power_count, eaten_ghosts):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH//30
    if 0 < player_x < 870:
        if level[center_y//num1][center_x// num2] == 1:
            level[center_y//num1][center_x// num2] = 0
            scor += 10
            if not (player_x == 430 and player_y == 663):
                eat_dot.play(loops=1)
        if level[center_y//num1][center_x// num2] == 2:
            level[center_y//num1][center_x// num2] = 0
            scor += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
            eat_dot.play(loops=1)
    return scor, power, power_count, eaten_ghosts



def draw_board(color):
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 14)
            if level[i][j] == 3:
                wall_color = toggle_color(color) if flicker_state else color
                pygame.draw.line(screen, wall_color, (j * num2 + (0.5 * num2), i*num1), (j * num2 + (0.5 * num2), i*num1 + num1), 3)
                #pygame.draw.line(screen, toggle_color(color) if game_won == False else color_normal, (j * num2 + (0.5 * num2), i*num1), (j * num2 + (0.5 * num2), i*num1 + num1), 3)
            if level[i][j] == 4:
                wall_color = toggle_color(color) if flicker_state else color
                pygame.draw.line(screen, wall_color, (j * num2, i*num1 + (0.5*num1)), (j * num2 + num2, i*num1 + (0.5*num1)), 3)
            if level[i][j] == 5:
                wall_color = toggle_color(color) if flicker_state else color
                pygame.draw.arc(screen, wall_color,[(j*num2 - (num2*0.4)) - 2, (i * num1 + (0.5*num1)), num2, num1], 0, PI/2, 3)
            if level[i][j] == 6:
                wall_color = toggle_color(color) if flicker_state else color
                pygame.draw.arc(screen, wall_color, [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                wall_color = toggle_color(color) if flicker_state else color
                pygame.draw.arc(screen, wall_color,[(j*num2 + (num2*0.5)), (i * num1 - (0.4*num1)), num2, num1], PI, 3*PI/2, 3)
            if level[i][j] == 8:
                wall_color = toggle_color(color) if flicker_state else color
                pygame.draw.arc(screen, wall_color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3*PI / 2, 2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'pink', (j * num2, i*num1 + (0.5*num1)), (j * num2 + num2, i*num1 + (0.5*num1)), 3)
    return color
            

def draw_player():
    index = (counter // 3) % len(player_images)
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_images[index], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[index], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[index], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[index], 270), (player_x, player_y))

def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH//30)
    num3 = 15
    # check collisions based on center x and center y of player +/- fudge number
    if centerx //30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3)//num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3)//num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery//num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery//num1][(centerx + num2) // num2] < 3:
                    turns[0] = True

        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1)//num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1)//num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery//num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery//num1][(centerx + num3) // num2] < 3:
                    turns[0] = True

    else:
        turns[0] = True
        turns[1] = True

    return turns


def move_player(play_x, play_y):
    #r, l, u, d
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y

def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, scared_played ):
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not scared_played:
            scared.play(loops=-1)
            scared_played = True
        if not blinky.dead and not eaten_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.dead and eaten_ghost[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead and not eaten_ghost[1]:
            ink_target = (runaway_x, player_y)
        elif not inky.dead and eaten_ghost[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead and not eaten_ghost[2]:
            pink_target = (player_x, runaway_y)
        elif not pinky.dead and eaten_ghost[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead and not eaten_ghost[3]:
            clyd_target = (450, 450)
        elif not clyde.dead and eaten_ghost[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    else:
        scared.stop()
        scared_played = False
        if not blinky.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
        
 
    return [blink_target, ink_target, pink_target, clyd_target, scared_played]



run = True
while run:
    timer.tick(fps)
    dt = clock.tick(60)
    current_time = pygame.time.get_ticks()  # milliseconds since pygame.init()
    if current_time - flicker_timer > flicker_interval:
        flicker_timer = current_time
        flicker_state = not flicker_state
        

    if counter < 19:
        counter += 1
        if counter > 13:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]
        siren_playing = toggle_siren(True)
    if startup_counter < 240 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True
    if powerup and power_counter >= 480:
        current_spooked = spooked_white_img
    elif powerup and power_counter <= 480:
        current_spooked = spooked_img
    cherry_timer += dt



    screen.fill('black')
    draw_board(toggle_color(color))
    center_x = player_x + 23
    center_y = player_y + 24
    if powerup:
        ghost_speeds = [1, 1, 1, 1]
        #if siren_playing:
        siren_playing = toggle_siren(False)    
    else:
        ghost_speeds = [2, 2, 2, 2]
        if not siren_playing and not first_loop_done:
            siren_playing = toggle_siren(True)
    if eaten_ghost[0] and not blinky_eaten_played:
        blinky_eaten_sound.play()
        blinky_eaten_played = True
        ghost_speeds[0] = 2
    elif not powerup:
        blinky_eaten_played = False
        ghost_speeds[0] = 2
    elif eaten_ghost[0]:
        ghost_speeds[0] = 2
    if eaten_ghost[1] and not inky_eaten_played:
        inky_eaten_sound.play()
        inky_eaten_played = True
        ghost_speeds[1] = 2
    elif not powerup:
        inky_eaten_played = False
        ghost_speeds[1] = 2
    elif eaten_ghost[1]:
        ghost_speeds[1] = 2
    if eaten_ghost[2] and not pinky_eaten_played:
        pinky_eaten_sound.play()
        pinky_eaten_played = True
        ghost_speeds[2] = 2
    elif not powerup:
        pinky_eaten_played = False
        ghost_speeds[2] = 2
    elif eaten_ghost[2]:
        ghost_speeds[2] = 2
    if eaten_ghost[3] and not clyde_eaten_played:
        clyde_eaten_sound.play()
        clyde_eaten_played = True
        ghost_speeds[3] = 2
    elif not powerup:
        clyde_eaten_played = False
        ghost_speeds[3] = 2
    elif eaten_ghost[3]:
        ghost_speeds[3] = 2
    if blinky_dead:
        ghost_speeds[0] = 4
    if inky_dead:
        ghost_speeds[1] = 4
    if pinky_dead:
        ghost_speeds[2] = 4
    if clyde_dead:
        ghost_speeds[3] = 4
    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False

    

    if game_won and not intermission_played:
        intermission.play()
        intermission_played = True
    
    if game_won:    
        siren_playing = toggle_siren(False)
        scared.stop()
        blinky_eyes.stop()
        pinky_eyes.stop()
        inky_eyes.stop()
        clyde_eyes.stop()
        player_speed = 0
        ghost_speeds[0] = 0
        ghost_speeds[1] = 0
        ghost_speeds[2] = 0
        ghost_speeds[3] = 0
        blinky_x = 430
        blinky_y = 330
        blinky_direction = 0
        inky_x = 370
        inky_y = 420
        inky_direction = 2
        pinky_x = 430
        pinky_y = 420
        pinky_direction = 2
        clyde_x = 490
        clyde_y = 420
        clyde_direction = 2


        

    if game_over:
        siren_playing = toggle_siren(False)
        player_speed = 0
        ghost_speeds[0] = 0
        ghost_speeds[1] = 0
        ghost_speeds[2] = 0
        ghost_speeds[3] = 0
        player_x = 370
        player_y = 420
        blinky_x = 430
        blinky_y = 330
        blinky_direction = 0
        inky_x = 370
        inky_y = 420
        inky_direction = 2
        pinky_x = 430
        pinky_y = 420
        pinky_direction = 2
        clyde_x = 490
        clyde_y = 420
        clyde_direction = 2
        

    #toggle_color(color)
    if cherry_collected:
        cherry_timer += dt    
    if cherry_collected and cherry_timer >= CHERRY_RESPAWN_TIME:
        cherry_collected = False
        cherry_timer = 0        
    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 5, 2)
    cherry_rect.topleft = (cherry_x, cherry_y)
    if not cherry_collected:
        screen.blit(cherry_img, (cherry_rect))
    if not cherry_collected and player_circle.colliderect(cherry_rect):
        cherry_collected = True
        score += 100
        eat_fruit.play() 

    draw_player()
    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_frames, blinky_direction, blinky_dead,
                   blinky_box, 0, dt)
    inky = Ghost(inky_x, inky_y, targets[1], ghost_speeds[1], inky_frames, inky_direction, inky_dead,
                 inky_box, 1, dt)
    pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_frames, pinky_direction, pinky_dead,
                  pinky_box, 2, dt)
    clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speeds[3], clyde_frames, clyde_direction, clyde_dead,
                  clyde_box, 3, dt)
    scared_played = targets[4]
    draw_misc()
    targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y, scared_played)
    center_x = player_x + 23
    center_y = player_y + 24
    check_position(center_x, center_y)
    turns_allowed = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
        if not blinky_dead and not blinky.in_box:
            blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
        else:
            blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
        if not pinky_dead and not pinky.in_box:
            pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
        else:
            pinky_x, pinky_y, pinky_direction = pinky.move_blinky()
        if not inky_dead and not inky.in_box:
            inky_x, inky_y, inky_direction = inky.move_inky()
        else:
            inky_x, inky_y, inky_direction = inky.move_blinky()
        if not clyde_dead and not clyde.in_box:
            clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
        else:
            clyde_x, clyde_y, clyde_direction = clyde.move_blinky()
    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)
    # add to if not powerup to check if eaten ghosts
    if not powerup:
        if (player_circle.colliderect(blinky.rect) and not blinky.dead) or \
                (player_circle.colliderect(inky.rect) and not inky.dead) or \
                (player_circle.colliderect(pinky.rect) and not pinky.dead) or \
                (player_circle.colliderect(clyde.rect) and not clyde.dead) and not death_played:
            if lives > 0:
                blinky_eyes.stop()
                pinky_eyes.stop()
                inky_eyes.stop()
                clyde_eyes.stop()
                scared.stop()
                lives -= 1
                death.play()
                death_played = False
                startup_counter = 0
                powerup = False
                power_counter = 0
                player_x = 430
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 430
                blinky_y = 330
                blinky_direction = 0
                inky_x = 370
                inky_y = 420
                inky_direction = 2
                pinky_x = 430
                pinky_y = 420
                pinky_direction = 2
                clyde_x = 490
                clyde_y = 420
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                targets = [(player_x, player_y,), (player_x, player_y), (player_x, player_y), (player_x, player_y), scared_played]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
                siren_playing = toggle_siren(False)

        if powerup and player_circle.colliderect(blinky.rect) and eaten_ghost[0] and not blinky.dead:
            if lives > 0:
                lives -= 1
                startup_counter = 0
                powerup = False
                power_counter = 0
                player_x = 430
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 430
                blinky_y = 330
                blinky_direction = 0
                inky_x = 370
                inky_y = 420
                inky_direction = 2
                pinky_x = 430
                pinky_y = 420
                pinky_direction = 2
                clyde_x = 490
                clyde_y = 420
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                targets = [(player_x, player_y,), (player_x, player_y), (player_x, player_y), (player_x, player_y), scared_played]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
        if powerup and player_circle.colliderect(inky.rect) and eaten_ghost[1] and not inky.dead:
            if lives > 0:
                lives -= 1
                startup_counter = 0
                powerup = False
                power_counter = 0
                player_x = 430
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 430
                blinky_y = 330
                blinky_direction = 0
                inky_x = 370
                inky_y = 420
                inky_direction = 2
                pinky_x = 430
                pinky_y = 420
                pinky_direction = 2
                clyde_x = 490
                clyde_y = 420
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                targets = [(player_x, player_y,), (player_x, player_y), (player_x, player_y), (player_x, player_y), scared_played]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
        if powerup and player_circle.colliderect(pinky.rect) and eaten_ghost[2] and not pinky.dead:
            if lives > 0:
                lives -= 1
                startup_counter = 0
                powerup = False
                power_counter = 0
                player_x = 430
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 430
                blinky_y = 330
                blinky_direction = 0
                inky_x = 370
                inky_y = 420
                inky_direction = 2
                pinky_x = 430
                pinky_y = 420
                pinky_direction = 2
                clyde_x = 490
                clyde_y = 420
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                targets = [(player_x, player_y,), (player_x, player_y), (player_x, player_y), (player_x, player_y), scared_played]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
        if powerup and player_circle.colliderect(clyde.rect) and eaten_ghost[3]and not clyde.dead:
            if lives > 0:
                lives -= 1
                startup_counter = 0
                powerup = False
                power_counter = 0
                player_x = 430
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 430
                blinky_y = 330
                blinky_direction = 0
                inky_x = 370
                inky_y = 420
                inky_direction = 2
                pinky_x = 430
                pinky_y = 420
                pinky_direction = 2
                clyde_x = 490
                clyde_y = 420
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                targets = [(player_x, player_y,), (player_x, player_y), (player_x, player_y), (player_x, player_y), scared_played]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
    if powerup and player_circle.colliderect(blinky.rect) and not blinky.dead and not eaten_ghost[0]:
        blinky_dead = True
        eaten_ghost[0] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(inky.rect) and not inky.dead and not eaten_ghost[1]:
        inky_dead = True
        eaten_ghost[1] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(pinky.rect) and not pinky.dead and not eaten_ghost[2]:
        pinky_dead = True
        eaten_ghost[2] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(clyde.rect) and not clyde.dead and not eaten_ghost[3]:
        clyde_dead = True
        eaten_ghost[3] = True
        score += (2 ** eaten_ghost.count(True)) * 100



                                                                                                                                                                                                                                                                          


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_over or game_won):
                lives -= 1
                startup_counter = 0
                blinky_eyes.stop()
                pinky_eyes.stop()
                inky_eyes.stop()
                clyde_eyes.stop() 
                scared.stop()
                intermission.stop()
                intermission_played = False
                start.play()
                powerup = False
                power_counter = 0
                player_x = 430
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 430
                blinky_y = 330
                blinky_direction = 0
                inky_x = 370
                inky_y = 420
                inky_direction = 2
                pinky_x = 430
                pinky_y = 420
                pinky_direction = 2
                clyde_x = 490
                clyde_y = 420
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                targets = [(player_x, player_y,), (player_x, player_y), (player_x, player_y), (player_x, player_y), scared_played]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
                score = 0
                lives = 3
                level = copy.deepcopy(boards)
                game_over = False
                game_won = False
                color = 'blue'
                player_speed = 2
                siren_playing = toggle_siren(True)
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3 and not game_won and not powerup:
                player_speed = 0
                ghost_speeds[0] = 0
                ghost_speeds[1] = 0
                ghost_speeds[2] = 0
                ghost_speeds[3] = 0
            if event.button == 1 and not game_won:
                player_speed = 2
                ghost_speeds[0] = 2
                ghost_speeds[1] = 0
                ghost_speeds[2] = 0
                ghost_speeds[3] = 0
                



    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897

    if blinky_dead and not blinky.in_box and not blinky_eyes_played:
        blinky_eyes.play(loops=-1)
        blinky_eyes_played = True
    elif blinky.in_box:
        blinky_eyes_played = False
    if inky_dead and not inky.in_box and not inky_eyes_played:
        inky_eyes.play(loops=-1)
        inky_eyes_played = True
    elif inky.in_box:
        inky_eyes_played = False
    if pinky_dead and not pinky.in_box and not pinky_eyes_played:
        pinky_eyes.play(loops=-1)
        pinky_eyes_played = True
    elif pinky.in_box:
        pinky_eyes_played = False
    if clyde_dead and not clyde.in_box and not clyde_eyes_played:
        clyde_eyes.play(loops=-1)
        clyde_eyes_played = True
    elif clyde.in_box:
        clyde_eyes_played = False
        
    
    if blinky.in_box and blinky_dead:
        blinky_dead = False
        blinky_eyes.stop()
    if inky.in_box and inky_dead: 
        inky_dead = False
        inky_eyes.stop()
    if pinky.in_box and pinky_dead:
        pinky_dead = False
        pinky_eyes.stop()
    if clyde.in_box and clyde_dead:
        clyde_dead = False
        clyde_eyes.stop()
    first_loop_done = True




    pygame.display.flip()
pygame.quit()
