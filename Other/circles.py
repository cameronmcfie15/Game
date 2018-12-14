import pygame
import sys

SCREEN_SIZE = WIDTH, HEIGHT = (640, 480)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
CIRCLE_RADIUS = 30

# Initialization
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Circles')
fps = pygame.time.Clock()
paused = False

# Ball setup
ball_pos1 = [50, 50]
ball_pos2 = [50, 240]
ball_pos3 = [50, 430]

def update():
    ball_pos1[0] += 5
    ball_pos2[0] += 3
    ball_pos3[0] += 1


def render():
    screen.fill(BLACK)
    pygame.draw.circle(screen, RED, ball_pos1, CIRCLE_RADIUS, 0)
    pygame.draw.circle(screen, WHITE, ball_pos2, CIRCLE_RADIUS, 0)
    pygame.draw.circle(screen, GREEN, ball_pos3, CIRCLE_RADIUS, 0)
    pygame.display.update()
    fps.tick(60)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                paused = not paused
    if not paused:
        update()
        render()