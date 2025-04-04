# Import necessary libraries
import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Set the dimensions of the drawing area (window size)
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simple Paint')  # Window title

# Define color constants
white = (255, 255, 255)
black = (0, 0 , 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)

# Define Button class to handle button creation and interaction
class Button:
    def __init__(self, x, y, width, height, text, color, action):
        self.rect = pygame.Rect(x, y, width, height)  # Button's position and size
        self.text = text  # Button label text
        self.color = color  # Button color
        self.action = action  # Action to perform when button is clicked

    # Draw the button on the screen
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)  # Draw button rectangle
        font = pygame.font.Font(None, 30)  # Set font size
        text_surface = font.render(self.text, True, white)  # Render text
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))  # Draw text on button

    # Check if the button is clicked
    def check_action(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.action()  # Execute button's action when clicked

# Global variables for drawing
drawing = False  # Track whether drawing is in progress
shape_start = None  # Start position for shapes
brush_color = black  # Default brush color
tool = 'brush'  # Default drawing tool (brush)

# Functions to select colors and tools
def set_black(): global brush_color; brush_color = black
def set_green(): global brush_color; brush_color = green
def set_red(): global brush_color; brush_color = red
def set_blue(): global brush_color; brush_color = blue
def clear_screen(): screen.fill(white)  # Clear the screen to white
def exit_app(): pygame.quit(); sys.exit()  # Exit the application

# Tool selection functions
def select_brush(): global tool; tool = 'brush'
def select_circle(): global tool; tool = 'circle'
def select_square(): global tool; tool = 'square'
def select_right_triangle(): global tool; tool = 'right_triangle'
def select_equilateral_triangle(): global tool; tool = 'equilateral_triangle'
def select_rhombus(): global tool; tool = 'rhombus'

# Create buttons for color and tool selection
buttons = [
    Button(10, 10, 60, 30, 'Black', black, set_black),
    Button(80, 10, 60, 30, 'Green', green, set_green),
    Button(150, 10, 60, 30, 'Red', red, set_red),
    Button(220, 10, 60, 30, 'Blue', blue, set_blue),
    Button(290, 10, 60, 30, 'Clear', gray, clear_screen),
    Button(360, 10, 60, 30, 'Exit', gray, exit_app),
    Button(430, 10, 80, 30, 'Brush', gray, select_brush),
    Button(520, 10, 80, 30, 'Circle', gray, select_circle),
    Button(610, 10, 80, 30, 'Square', gray, select_square),
    Button(700, 10, 80, 30, 'R-Tri', gray, select_right_triangle),
    Button(10, 50, 80, 30, 'E-Tri', gray, select_equilateral_triangle),
    Button(100, 50, 80, 30, 'Rhombus', gray, select_rhombus),
]

clear_screen()  # Initial screen is cleared to white

# Function to draw shapes based on the selected tool
def draw_shape(shape_start, shape_end, tool):
    x1, y1 = shape_start
    x2, y2 = shape_end

    if tool == 'circle':
        radius = int(math.hypot(x2 - x1, y2 - y1))  # Calculate distance for circle radius
        pygame.draw.circle(screen, brush_color, shape_start, radius, 2)  # Draw circle

    elif tool == 'square':
        side = max(abs(x2 - x1), abs(y2 - y1))  # Ensure square's sides are equal
        rect = pygame.Rect(x1, y1, side, side)  # Create a rectangle with square dimensions
        pygame.draw.rect(screen, brush_color, rect, 2)  # Draw square

    elif tool == 'right_triangle':
        points = [shape_start, (x1, y2), (x2, y2)]  # Right triangle points
        pygame.draw.polygon(screen, brush_color, points, 2)  # Draw right triangle

    elif tool == 'equilateral_triangle':
        side = abs(x2 - x1)
        height = side * (3 ** 0.5) / 2  # Calculate height for equilateral triangle
        points = [(x1, y1), (x1 + side, y1), (x1 + side / 2, y1 - height)]  # Triangle points
        pygame.draw.polygon(screen, brush_color, points, 2)  # Draw equilateral triangle

    elif tool == 'rhombus':
        dx = (x2 - x1) // 2  # Horizontal distance for rhombus
        dy = (y2 - y1) // 2  # Vertical distance for rhombus
        cx = x1 + dx  # Center X
        cy = y1 + dy  # Center Y
        points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]  # Rhombus points
        pygame.draw.polygon(screen, brush_color, points, 2)  # Draw rhombus

# Variable to track the last drawing position for brush tool
last_pos = None

# Main loop for handling events and drawing
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Exit the game if window is closed
            pygame.quit()
            sys.exit()

        # Check for button actions (color and tool selection)
        for b in buttons:
            b.check_action(event)

        # Mouse button pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left-click to start drawing
                shape_start = pygame.mouse.get_pos()  # Get starting position
                drawing = True  # Start drawing
                if tool == 'brush':
                    last_pos = shape_start  # Track last position for brush

        # Mouse button released
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:  # Finish drawing when mouse is released
                shape_end = pygame.mouse.get_pos()  # Get ending position
                if tool != 'brush':  # If not brush, draw the shape
                    draw_shape(shape_start, shape_end, tool)
                drawing = False  # Stop drawing
                last_pos = None  # Reset last position

        # Mouse motion while drawing
        elif event.type == pygame.MOUSEMOTION:
            if drawing and tool == 'brush':  # Draw continuous lines with brush
                current_pos = pygame.mouse.get_pos()
                if last_pos:
                    pygame.draw.line(screen, brush_color, last_pos, current_pos, 4)  # Draw line
                last_pos = current_pos  # Update last position

    # Draw the button area (top part of the screen)
    pygame.draw.rect(screen, gray, (0, 0, width, 90))
    for b in buttons:  # Draw all buttons
        b.draw(screen)

    # Update the display
    pygame.display.flip()
