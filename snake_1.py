# Import necessary libraries
import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()

# Set the width and height of the game window
width, height = 500, 500
cell_size = 10  # Each cell the snake moves in is 10x10 pixels

# Create the game window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("SNAKE")  # Set the window title

# Define some colors using RGB format
black = (0, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

# Initialize the snake's starting position and body
snake_pos = [100, 100]  # The head of the snake
snake_body = [[100, 100], [90, 100], [80, 100]]  # List of segments representing the snake's body

# Load and scale the image for the snake's head
snake = pygame.image.load('snake.jpg').convert_alpha()
snake = pygame.transform.scale(snake, (cell_size, cell_size))

# Class for handling food (apple) properties and behavior
class Food:
    def __init__(self):
        self.rect = self.generate_food_rect()  # Position of the apple
        self.weight = random.randint(1, 5)  # How many points the apple gives (random 1 to 5)
        self.creation_time = time.time()  # When the apple was created (used to expire it)
        self.image = pygame.image.load("apple.png").convert_alpha()  # Load apple image
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))  # Resize apple

    # Generate random position for the apple that doesn't collide with the snake's body
    def generate_food_rect(self):
        while True:
            x = random.randint(0, (width - cell_size) // cell_size) * cell_size
            y = random.randint(0, (height - cell_size) // cell_size) * cell_size
            if [x, y] not in snake_body:
                return pygame.Rect(x, y, cell_size, cell_size)

    # Check if the apple has been on the screen too long (default 5 seconds)
    def is_expired(self, expiration_time=5):
        return time.time() - self.creation_time > expiration_time

# Create the first apple
apple = Food()

# Font to display score and level
font = pygame.font.SysFont("Verdana", 20)

# Set initial direction and game control variables
direction = 'RIGHT'
change_to = direction
clock = pygame.time.Clock()
score = 0
level = 1
speed = 10
Running = True

# Main game loop
while Running:
    # Handle events (key presses and closing the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Change direction if not opposite of current direction
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'

    direction = change_to  # Update direction

    # Move the snake's head based on direction
    if direction == 'UP':
        snake_pos[1] -= cell_size
    elif direction == 'DOWN':
        snake_pos[1] += cell_size
    elif direction == 'RIGHT':
        snake_pos[0] += cell_size
    elif direction == 'LEFT':
        snake_pos[0] -= cell_size

    # Wrap around the screen if snake goes out of bounds
    snake_pos[0] %= width
    snake_pos[1] %= height

    # Add new head to the snake body
    snake_body.insert(0, list(snake_pos))

    # Check if snake ate the apple
    if pygame.Rect(snake_pos[0], snake_pos[1], cell_size, cell_size).colliderect(apple.rect):
        score += apple.weight  # Increase score by apple's weight
        # If score reaches multiple of 4, increase level and speed
        if score // 4 + 1 > level:
            level += 1
            speed += 2
        apple = Food()  # Create a new apple
    else:
        snake_body.pop()  # If not eaten, remove last part to keep length same

    # If apple is expired (after 5 seconds), generate a new one
    if apple.is_expired():
        apple = Food()

    # Clear the screen
    screen.fill(black)

    # Draw the apple on the screen
    screen.blit(apple.image, apple.rect.topleft)

    # Draw each block of the snake
    for block in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(block[0], block[1], cell_size, cell_size))

    # Display score and level
    score_text = font.render(f"Score: {score}", True, white)
    level_text = font.render(f"Level: {level}", True, white)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (400, 10))

    # Update the screen
    pygame.display.flip()

    # Control the game's speed
    clock.tick(speed)
