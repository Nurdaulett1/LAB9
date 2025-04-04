import pygame,sys
from pygame.locals import *
import random

pygame.init()
color1 = pygame.Color(0, 0, 0)         # Black
color2 = pygame.Color(255, 255, 255)   # White
color3 = pygame.Color(128, 128, 128)   # Grey
color4 = pygame.Color(255, 0, 0)       # Red
height = 800
width = 800
screen = pygame.display.set_mode((height,width))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()
running = True



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160,520)
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print('AAAAAAAAAAA')
    
    pygame.display.update()
    clock.tick(60)