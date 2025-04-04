# Import required modules
import pygame, sys
from pygame.locals import *
import random, time

# Initialize Pygame
pygame.init()

# Set the game speed and clock
FPS = 60
FramePerSec = pygame.time.Clock()

# Define some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set screen size and game variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5  # Initial enemy speed
SCORE = 0  # Number of enemies avoided
COINS_COLLECTED = 0  # Number of coins collected

# Set fonts for displaying text
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load background image and set up the screen
background = pygame.image.load("AnimatedStreet.png")
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# Enemy class (cars you need to avoid)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")  # Load enemy image
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  # Random x, start from top

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)  # Move enemy down
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1  # Increase score if enemy goes off screen
            self.rect.top = 0  # Reset to top
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)  # New random x

# Player class (your car)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")  # Load player image
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)  # Set player starting position

    def move(self):
        # Handle left/right movement based on key press
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

# Coin class (collect these to earn points)
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin.jpg")  # Load coin image
        self.image = pygame.transform.scale(self.image, (30, 30))  # Resize to fit
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)  # Start at random x

    def move(self):
        self.rect.move_ip(0, SPEED)  # Move coin down
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = 0  # Reset to top
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Create game objects
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Group sprites for easier updates
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Create event that increases speed every second
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Game loop
while True:
    # Check for events
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5  # Gradually increase game difficulty
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw background
    DISPLAYSURF.blit(background, (0, 0))

    # Show score and coins
    score_text = font_small.render("Score: " + str(SCORE), True, BLACK)
    coin_text = font_small.render("Coins: " + str(COINS_COLLECTED), True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 100, 10))

    # Draw and update all sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Check for collision with enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()  # Remove all sprites from screen
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Check for collision with coin
    if pygame.sprite.spritecollideany(P1, coins):
        COINS_COLLECTED += 1
        # Move coin to new position after collecting
        C1.rect.top = 0
        C1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    # Refresh screen
    pygame.display.update()
    FramePerSec.tick(FPS)  # Limit the game to 60 FPS
