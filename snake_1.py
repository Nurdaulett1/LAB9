import pygame
import sys
import random
import time

pygame.init()

width, height = 500, 500
cell_size = 10
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("SNAKE")

black = (0, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

snake_pos = [100, 100]
snake_body = [[100, 100], [90, 100], [80, 100]]

snake = pygame.image.load('snake.jpg').convert_alpha()
snake = pygame.transform.scale(snake, (cell_size, cell_size))

class Food:
    def __init__(self):
        self.rect = self.generate_food_rect()
        self.weight = random.randint(1, 5)
        self.creation_time = time.time()
        self.image = pygame.image.load("apple.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))

    def generate_food_rect(self):
        while True:
            x = random.randint(0, (width - cell_size) // cell_size) * cell_size
            y = random.randint(0, (height - cell_size) // cell_size) * cell_size
            if [x, y] not in snake_body:
                return pygame.Rect(x, y, cell_size, cell_size)

    def is_expired(self, expiration_time=5):
        return time.time() - self.creation_time > expiration_time

apple = Food()
font = pygame.font.SysFont("Verdana", 20)

direction = 'RIGHT'
change_to = direction
clock = pygame.time.Clock()
score = 0
level = 1
speed = 10
Running = True

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'

    direction = change_to

    if direction == 'UP':
        snake_pos[1] -= cell_size
    elif direction == 'DOWN':
        snake_pos[1] += cell_size
    elif direction == 'RIGHT':
        snake_pos[0] += cell_size
    elif direction == 'LEFT':
        snake_pos[0] -= cell_size

    snake_pos[0] %= width
    snake_pos[1] %= height
    snake_body.insert(0, list(snake_pos))

    if pygame.Rect(snake_pos[0], snake_pos[1], cell_size, cell_size).colliderect(apple.rect):
        score += apple.weight
        if score // 4 + 1 > level:
            level += 1
            speed += 2
        apple = Food()
    else:
        snake_body.pop()

    if apple.is_expired():
        apple = Food()

    screen.fill(black)
    screen.blit(apple.image, apple.rect.topleft)

    for block in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(block[0], block[1], cell_size, cell_size))

    score_text = font.render(f"Score: {score}", True, white)
    level_text = font.render(f"Level: {level}", True, white)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (400, 10))

    pygame.display.flip()
    clock.tick(speed)
