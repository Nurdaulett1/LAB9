import pygame
import sys
import math

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simple Paint')

white = (255, 255, 255)
black = (0, 0 , 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)

class Button:
    def __init__(self, x, y, width, height, text, color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 30)
        text_surface = font.render(self.text, True, white)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def check_action(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.action()

drawing = False
shape_start = None
brush_color = black
tool = 'brush'

def set_black(): global brush_color; brush_color = black
def set_green(): global brush_color; brush_color = green
def set_red(): global brush_color; brush_color = red
def set_blue(): global brush_color; brush_color = blue
def clear_screen(): screen.fill(white)
def exit_app(): pygame.quit(); sys.exit()

def select_brush(): global tool; tool = 'brush'
def select_circle(): global tool; tool = 'circle'
def select_square(): global tool; tool = 'square'
def select_right_triangle(): global tool; tool = 'right_triangle'
def select_equilateral_triangle(): global tool; tool = 'equilateral_triangle'
def select_rhombus(): global tool; tool = 'rhombus'

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

clear_screen()

def draw_shape(shape_start, shape_end, tool):
    x1, y1 = shape_start
    x2, y2 = shape_end

    if tool == 'circle':
        radius = int(math.hypot(x2 - x1, y2 - y1))
        pygame.draw.circle(screen, brush_color, shape_start, radius, 2)

    elif tool == 'square':
        side = max(abs(x2 - x1), abs(y2 - y1))
        rect = pygame.Rect(x1, y1, side, side)
        pygame.draw.rect(screen, brush_color, rect, 2)

    elif tool == 'right_triangle':
        points = [shape_start, (x1, y2), (x2, y2)]
        pygame.draw.polygon(screen, brush_color, points, 2)

    elif tool == 'equilateral_triangle':
        side = abs(x2 - x1)
        height = side * (3 ** 0.5) / 2
        points = [(x1, y1), (x1 + side, y1), (x1 + side / 2, y1 - height)]
        pygame.draw.polygon(screen, brush_color, points, 2)

    elif tool == 'rhombus':
        dx = (x2 - x1) // 2
        dy = (y2 - y1) // 2
        cx = x1 + dx
        cy = y1 + dy
        points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
        pygame.draw.polygon(screen, brush_color, points, 2)

last_pos = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        for b in buttons:
            b.check_action(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                shape_start = pygame.mouse.get_pos()
                drawing = True
                if tool == 'brush':
                    last_pos = shape_start

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                shape_end = pygame.mouse.get_pos()
                if tool != 'brush':
                    draw_shape(shape_start, shape_end, tool)
                drawing = False
                last_pos = None

        elif event.type == pygame.MOUSEMOTION:
            if drawing and tool == 'brush':
                current_pos = pygame.mouse.get_pos()
                if last_pos:
                    pygame.draw.line(screen, brush_color, last_pos, current_pos, 4)
                last_pos = current_pos

    pygame.draw.rect(screen, gray, (0, 0, width, 90))
    for b in buttons:
        b.draw(screen)

    pygame.display.flip()
