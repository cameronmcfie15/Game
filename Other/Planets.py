import pygame, math
from pygame.locals import *
from random import randint
pygame.init()
screen = pygame.display.set_mode([500,500])
clock = pygame.time.Clock()

class Planet():
    def __init__(self, vel = [1, 1], mass = 100000, pos = [100, 100], pathLength = 100000):
        self.v = vel
        self.m = mass
        self.size = mass/1000000
        self.pos = pos
        self.pL = pathLength
        self.path = [[pos[0], pos[1]]]

    def update(self):
        self.pos[0] += self.v[0]
        self.pos[1] += self.v[1]
        self.path.append([self.pos[0], self.pos[1]])
        if len(self.path) == self.pL:
            self.path.pop(0)

class World():
    def __init__(self, planetList, iterations, mass = 10000000, gravityConstant = (6 * 10 ** -9)):
        self.plnt = planetList
        self.iter = iterations
        self.mass = mass
        self.size = int(mass/1000000)
        self.gC = gravityConstant
    def draw(self):
        pygame.draw.circle(screen, [0, 0, 0], [250, 250], self.size)
        for p in self.plnt:
            pygame.draw.rect(screen, [0, 0, 0], [p.pos[0], p.pos[1], 20, 20])
            pygame.draw.lines(screen, [0, 0, 0], False, p.path)
    def update(self):
        for i in range(self.iter):
            for p in self.plnt:
                d = math.sqrt((p.pos[0] - 250) ** 2 + (p.pos[1] - 250) ** 2)
                f = (self.gC * self.mass * p.m)/(d ** 2)
                vect = [((250 - p.pos[0]) / d) * f, ((250 - p.pos[1]) / d) * f]
                print(d,f)
                p.v[0] += vect[0]
                p.v[1] += vect[1]
                p.update()
        self.draw()


a = Planet([4, 0])
b = Planet([4, 0])
w = World([b], 2)
while 1:
    screen.fill([255, 255, 255])

    w.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
    #print(b.v[0], b.v[1])
    pygame.display.update()
    clock.tick(60)