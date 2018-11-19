import pygame, sys, random, math, time, threading
import numpy as np
# Setup
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()
width, height = 1000, 950
screen = pygame.display.set_mode((width, height))
WHITE = (255, 255, 255)
black = (0, 0, 0)
font = pygame.font.SysFont('Verdana', 18)
planetList = []
center = 500
colour = list(np.random.choice(range(256), size=3))
colourDict = {'white': (255, 255, 255), 'brown': (160, 82, 45)}
posMovement = 0.00001
text = ' '
numberOfPlanets = 100
frames, actualFps = 0, 0
#sol = pygame.transform.scale()
# Constants
Mass = 4*10**13  # Mass of Centre   5.972*10**24
G = 6.67*10**-11  # Gravity Constant    6.67*10**-11



class Planet():
    def __init__(self, mass, xPos, yPos, xVel, yVel):
        self.mass, self.xPos, self.yPos, self.xVel, self.yVel = mass, xPos, yPos, xVel, yVel
        self.xAcceleration, self.yAcceleration, self.force = 0, 0, 0  # Force of gravity at the distance calculated
        self.distance = 1000  # Distance from the center of the gravity well
        self.xReset, self.yReset = xPos, yPos
        self.planet = pygame.draw.circle(screen, colour, (int(self.xPos), int(self.yPos)), 5)
        planetList.append(self)

    def update(self):  # Is called every tick, from here a method is decided
        global center, v, posMovement
        self.planet = pygame.draw.circle(screen, colour, (int(self.xPos), int(self.yPos)), 5)
        if self.xPos > 1000 or self.xPos < 0 or self.yPos > 1000 or self.yPos < 0:
            self.kill()

        elif self.distance > 90:
            self.positionUpdate()
            posMovement = 0.1
        elif 1 in pressed:
            self.positionUpdate()
        elif self.distance < 90:
            self.collided()
    def kill(self):
        global count
        count += 1
        planetList.remove(self)
        print('died', count)

    def collided(self):
        self.kill()
        self.xVel, self.yVel, self.xAcceleration, self.yAcceleration = 0, 0, 0, 0
        self.friction = -self.force
        self.force = self.force + self.friction
        self.xReset = self.xPos
        self.yReset = self.yPos
        self.distance = math.sqrt(((self.xPos - center) ** 2) + ((self.yPos - center) ** 2))
        posMovement = 1
        if self.distance < 82:
            # print(self.xReset, self.yReset)
            self.xPos, self.yPos = self.xReset, self.yReset


    def positionUpdate(self):
        self.distance = abs(math.sqrt(((self.xPos - center) ** 2) + ((self.yPos - center) ** 2)))
        self.force = (G * Mass * self.mass) / self.distance ** 2  # V = GM/r
        self.xAcceleration = self.force * (center - self.xPos) / self.distance
        self.yAcceleration = self.force * (center - self.yPos) / self.distance
        self.xVel += self.xAcceleration
        self.yVel += self.yAcceleration
        self.xPos += self.xVel
        self.yPos += self.yVel

v = math.sqrt((G * Mass) / 400)
# Mass, X Position, Y Position, X Velocity, Y Velocity
count = 0
'''while count < 100:
    globals()['variable{}'.format(i)] = count
    Planet()
    count += 1'''
for i in range(0, numberOfPlanets):
    x = random.randint(1, 1000)
    y = random.randint(1, 1000)
    xv = random.uniform(-5, 5)
    yv = random.uniform(-5, 5)
    #yv = math.sqrt((G * Mass) / (500-x))
    #print(xv)
    #Planet(1, x, 500, 0, yv)
    Planet(1,x,y,xv,yv)



earth = Planet(1, 100, 500, 0, v)
kerbin = Planet(1, 350, 500, 0, 4.21742417439)


class Sat():
    def __init__(self, radius, planet, xPos, yPos, velocity, w):
        self.planet, self.radius, self.xPos, self.yPos, self.velocity, self.w = planet, radius, xPos, yPos, velocity, w
        planetList.append(self)

    def update(self):
        self.velocity = math.sqrt(G * self.planet.mass*10**15 / self.radius)
        self.w = self.velocity / self.radius
        self.xPos = self.radius * math.cos(self.w * timeSec) + self.planet.xPos
        self.yPos = self.radius * math.cos((self.w * timeSec) - (math.pi / 2)) + self.planet.yPos
        self.sat = pygame.draw.circle(screen, colour, (int(self.xPos), int(self.yPos)), 2)

moon = Sat(20, earth, 0, 0, 0, 0)


def keyboard():
    if pressed[pygame.K_RIGHT]:
        planetList[0].xVel += posMovement

    if pressed[pygame.K_LEFT]:
        planetList[0].xVel -= posMovement

    if pressed[pygame.K_UP]:
        planetList[0].yVel -= posMovement

    if pressed[pygame.K_DOWN]:
        planetList[0].yVel += posMovement

    if pressed[pygame.K_SPACE]:
        planetList[0].yVel = planetList[0].yVel*1.01
        planetList[0].xVel = planetList[0].xVel*1.01

    if pressed[pygame.K_LSHIFT]:
        planetList[0].yVel = planetList[0].yVel*0.99
        planetList[0].xVel = planetList[0].xVel*0.99

def hud():
    global text
    planet = planetList[0]
    aStr = str(round(planet.yPos))
    bStr = str(round(planet.xPos))
    cStr = str(round(timeSec))
    dStr = str(round(planet.distance))
    eStr = str(round(planet.force,2))
    fStr = str(round(planet.xAcceleration,2))
    gStr = str(round(planet.yAcceleration,2))
    hStr = str(round(planet.xVel, 1))
    iStr = str(round(planet.yVel*-1, 1))
    #fpsStr = str(round(frames,2))
    text = (bStr+' XPos  '+cStr+' secs   '+aStr+' YPos   '+eStr+' ms-2   '+dStr+' m   '+fStr+'m xVect  '+gStr+'m yVect  '+hStr+'ms xVel  '+iStr+'ms yVel  ')
    screen.blit(font.render(text, True, (colourDict['white'])), (32, 48))


while True:  # main game loop
    screen.fill(black)
    colour = list(np.random.choice(range(256), size=3))
    timeSec = (pygame.time.get_ticks() - start_ticks) / 1000  # Time in Seconds
    pressed = pygame.key.get_pressed()
    for planet in planetList:
        planet.update()
    sol = pygame.draw.circle(screen, colourDict['brown'], (500, 500), 80)
    hud()
    clock = pygame.time.Clock()
    #print(clock.get_fps())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.update()
    fpsClock.tick(fps)  # Same as time.sleep(1/fps) I think
    #print(len(planetList))
    if 1 in pressed:
        keyboard()
        print(planetList)











'''
self.dDraw = pygame.draw.circle(screen, colour, (150, int(self.distance)+500), 3)
self.aDraw = pygame.draw.circle(screen, colour, (130, int(self.force)+500), 3)
self.xVectDraw = pygame.draw.circle(screen, colour, (110, int(self.xA*500)+500), 3)
self.yVectDraw = pygame.draw.circle(screen, colour, (90, int(self.yAcceleration*500)+500), 3)
self.xVelDraw = pygame.draw.circle(screen, colour, (70, int(self.xVel*20)+500), 3)
self.yVelDraw = pygame.draw.circle(screen, colour, (50, int(self.yVel*20)+500), 3)
self.xPosDraw = pygame.draw.circle(screen, colour, (30, int(self.xPos)), 3)
self.yPosDraw = pygame.draw.circle(screen, colour, (10, int(self.yPos)), 3)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([5, 5])
        self.rect = self.image.get_rect()
'''



