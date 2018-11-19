# Made By Cameron McFie

import pygame, sys, random, math, time, threading, trace,sched
import numpy as np
import itertools
# Setup
#  For trace    python -m trace --trace Orbit_Sim.py
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()
width, height = 1000, 950
screen = pygame.display.set_mode((width, height))
font = pygame.font.SysFont('Verdana', 18)
planetList, satList, missileList = [], [], []
center = 500
randColour = list(np.random.choice(range(256), size=3))
colourDict = {'white': (255, 255, 255), 'brown': (160, 82, 45), 'black': (0, 0, 0)}
bg = pygame.image.load('background1.png')
posMovement = 0.00001
text = ' '
numberOfPlanets = 0
frames, actualFps, count, degrees = 0, 0, 0, 0
sol = pygame.image.load('sol.png')
# Constants
Mass = 4*10**13  # Mass of Centre   5.972*10**24
G = 6.67*10**-11  # Gravity Constant    6.67*10**-11


# def keyPressed(inputKey):
#     keysPressed = pygame.key.get_pressed()
#     if keysPressed[inputKey]:
#         return True
#     else:
#         return False
#         print('wow')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.xPos, self.yPos, self.xVel, self.yVel, self.xAcceleration, self.yAcceleration = 500, 500, 0, 0, 0, 0
        self.sprite = pygame.draw.circle(screen, colourDict['brown'], (int(self.xPos), int(self.yPos)), 15)
        self.force = 0
        self.decay = 0.98
        self.angle = 0

    def update(self):
        #self.sprite = pygame.draw.circle(screen, colourDict['black'], (int(self.xPos), int(self.yPos)), 15)
        if self.force > 0:
            self.ship = pygame.image.load('missile1.png')
        else:
            self.ship = pygame.image.load('missile3.png')
        # self.triList = [(0+center,-10+center),(10+center,10+center),(-10+center,10+center)]
        self.x, self.y = [0, 10, -10], [-10, 10, 10]

        self.triList = [(self.x[0] + self.xPos, self.y[0] + self.yPos), (self.x[1] + self.xPos, self.y[1] + self.yPos), (self.x[2] + self.xPos, self.y[2] + self.yPos)]
        # self.triList = [(0 + self.x, -10 + self.y), (10 + self.x, 10 + self.y), (-10 + self.x, 10 + self.y)]
        self.tri = pygame.draw.polygon(screen, colourDict['white'], self.triList,2)
        self.ship = pygame.transform.rotate(self.ship, math.degrees(self.angle-math.pi))
        self.posistionUpdate()
        screen.blit(self.ship, (self.xPos, self.yPos))
        #print(self.xPos, self.yPos, self.xVel, self.yVel, self.xAcceleration, self.yAcceleration)
        self.force = 0
        # self.force
        # self.xAcceleration = self.force * self.xPos
        # self.yAcceleration = self.force * self.yPos
        # self.yAcceleration = self.force * self.yPos
        # self.yAcceleration = self.force * self.yPos
        # self.yAcceleration = self.force * self.yPos
        # if keyPressed(pygame.K_UP):
        #     self.force = 0.3
        # else:
        #     self.force = 0

    def moveUp(self):
        # if pygame.key.get_focused():
        # # self.yAcceleration += -self.force
        #     self.force = 1
        # else:
        #     self.force = 0
        pass



    def moveDown(self):
        # self.yAcceleration += +self.force
        self.force = 0

    def posistionUpdate(self):
        self.angle = list(pygame.mouse.get_pos())
        self.angle = [self.angle[0]-self.xPos,self.angle[1]-self.yPos]
        self.angle = (math.atan2(self.angle[0],self.angle[1]))
        self.xAcceleration = math.sin(self.angle) * self.force
        self.yAcceleration = math.cos(self.angle) * self.force
        # self.xAcceleration = self.force
        # self.yAcceleration = self.force
        self.xVel += self.xAcceleration
        self.yVel += self.yAcceleration
        self.xVel *= self.decay
        self.yVel *= self.decay
        self.xPos += self.xVel
        self.yPos += self.yVel
        # if d < 1:
        #     pass


class Planet:
    def __init__(self, mass, xPos, yPos, xVel, yVel):
        self.mass, self.xPos, self.yPos, self.xVel, self.yVel = mass, xPos, yPos, xVel, yVel
        self.xAcceleration, self.yAcceleration, self.force = 0, 0, 0  # Force of gravity at the distance calculated
        self.distance = 1000  # Distance from the center of the gravity well
        self.xReset, self.yReset = xPos, yPos
        self.planet = pygame.draw.circle(screen, colourDict['brown'], (int(self.xPos), int(self.yPos)), 15)
        planetList.append(self)

    def update(self):  # Is called every tick, from here a method is decided
        global center, v, posMovement
        self.planet = pygame.draw.circle(screen, colourDict['brown'], (int(self.xPos), int(self.yPos)), 15)
        if self.xPos > 1000 or self.xPos < 0 or self.yPos > 1000 or self.yPos < 0:
            self.kill()
        elif self.distance > 9:
            self.positionUpdate()
            posMovement = 0.1
        #elif 1 in pressed:
        #   self.positionUpdate()
        elif self.distance < 9:
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
        if self.distance < 2:
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


class Sat:  # Dunno what calls this but it works
    def __init__(self, radius, planet, xPos, yPos, velocity, w):
        self.planet, self.radius, self.xPos, self.yPos, self.velocity, self.w = planet, radius, xPos, yPos, velocity, w
        satList.append(self)

    def update(self):
        self.velocity = math.sqrt(G * self.planet.mass*10**15 / self.radius)
        self.w = self.velocity / self.radius
        self.xPos = self.radius * math.cos(self.w * timeSec) + self.planet.xPos
        self.yPos = self.radius * math.cos((self.w * timeSec) - (math.pi / 2)) + self.planet.yPos
        self.sat = pygame.draw.circle(screen, randColour, (int(self.xPos), int(self.yPos)), 2)


class Missile:
    def __init__(self, xPos, yPos, target):
        self.xPos, self.yPos, self.target = xPos, yPos, target
        self.xAcceleration, self.yAcceleration, self.force, self.xVel, self.yVel = 0, 0, 0, 0, 0
        self.adjacent, self.opposite, self.count = 0, 0, 0
        self.distance = 100
        self.rocket = pygame.image.load('missile1.png')
        self.rect = self.rocket.get_rect()
        missileList.append(self)

    def update(self):
        if frames % 2 == 0:
            self.rocket = pygame.image.load('missile1.png')
        else:
            self.rocket = pygame.image.load('missile2.png')
        self.positionUpdate()
        #if timeSec > 15:
        #    self.kill()
        if self.distance < 30:
            #planetList[0].kill()
            self.kill()
            pass


    def kill(self):
        self.xPos, self.yPos = 500, 500
        global count
        count += 1
        #missileList.remove(self)
        planetList.pop(0)
        print('died', count)
        rocketSpeed = 0

    def positionUpdate(self):
        self.distance = math.sqrt(((planetList[self.target].xPos - self.xPos) ** 2) + ((planetList[self.target].yPos - self.yPos) ** 2))
        #self.line = pygame.draw.line(screen, colourDict['white'], (self.xPos, self.yPos), (earth.xPos, earth.yPos), 1)
        self.opposite = (planetList[self.target].yPos - self.yPos)  # Works out distance between the y axis
        self.adjacent = (planetList[self.target].xPos - self.xPos)  # Works out distance between the x axis
        #self.angle = math.atan2(self.opposite, self.adjacent)
        #self.xVel = math.cos(self.angle)*self.distance*0.05
        #self.yVel = math.sin(self.angle)*self.distance*0.05
        self.xVel = (self.adjacent/self.distance)
        self.yVel = (self.opposite/self.distance)
        self.xPos += self.xVel * timeSec  # Time sec works well for 1 target but needs to reset for multiply tartgets
        self.yPos += self.yVel * timeSec
        self.rotater()
        '''
        self.opposite = (planetList[0].yPos - self.yPos)  # Works out distance between the y axis
        self.adjacent = (planetList[0].xPos - self.xPos)  # Works out distance between the x axis
        self.distance = abs(math.sqrt(((self.xPos - earth.xPos) ** 2) + ((self.yPos - earth.yPos) ** 2)))
        self.force = (G * Mass * 1) / self.distance ** 2  # V = GM/r
        self.xAcceleration = self.force * (earth.xPos - self.xPos) / self.distance
        self.yAcceleration = self.force * (earth.yPos - self.yPos) / self.distance
        self.xVel += self.xAcceleration
        self.yVel += self.yAcceleration
        self.xPos += self.xVel
        self.yPos += self.yVel
        print(self.xPos, self.yPos)
        #self.missile = screen.blit(self.rocket, (self.xPos, self.yPos))
        self.rotater()'''

    def rotater(self):
        self.direction = math.atan2(self.opposite, self.adjacent) * -1
        self.rotated = pygame.transform.rotate(self.rocket, math.degrees(self.direction)-90)
        self.missile = screen.blit(self.rotated, (self.xPos, self.yPos))

class shot:
    def __init__(self, angle, xPos, yPos):
        self.angle, self.xPos, self.yPos = angle, xPos, yPos

    def update(self):
        self.shot = pygame.draw.circle(screen, colourDict['black'], (int(self.xPos), int(self.yPos)), 2)





def keyboard():
    global pressed
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_RIGHT]:
        player.moveRight()
        #planetList[0].xVel += posMovement

    if pressed[pygame.K_LEFT]:
        player.moveLeft()
        #planetList[0].xVel -= posMovement

    if pressed[pygame.K_UP]:
        shot()
        player.moveUp()
        #planetList[0].yVel -= posMovement

    if pressed[pygame.K_DOWN]:
        player.moveDown()
        #planetList[0].yVel += posMovement

    if pressed[pygame.K_SPACE]:
        player.force = 0.4
        #planetList[0].yVel = planetList[0].yVel*1.01
        #planetList[0].xVel = planetList[0].xVel*1.01

    if pressed[pygame.K_LSHIFT]:
        pass
        #planetList[0].yVel = planetList[0].yVel*0.99
        #planetList[0].xVel = planetList[0].xVel*0.99


def hud():
    global text
    try:
        planet = missileList[0]
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
    except:
        pass
        #print('hud gone')


def updater():  # print(len(planetList))
    for planet in planetList:
        planet.update()
    for sat in satList:
        sat.update()
    for missile in missileList:
        missile.update()
    player.update()
    hud()


def eventHandler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def randPlanets():
    count = 0
    for i in range(0, numberOfPlanets):
        count += 1
        x = random.randint(1, 1000)
        y = random.randint(1, 1000)
        xv = random.uniform(-5, 5)
        yv = random.uniform(-5, 5)
        #yv = math.sqrt((G * Mass) / (500-x))
        #print(xv)
        #Planet(1, x, 500, 0, yv)
        Planet(1,x,y,xv,yv)
        #Missile(500, 500, count)
        print(count)


v = math.sqrt((G * Mass) / 400)
# Mass, X Position, Y Position, X Velocity, Y Velocity
player = Player()
# earth = Planet(1, 100, 500, 0, v)
#kerbin = Planet(1, 350, 500, 0, 4.21742417439)
# moon = Sat(20, earth, 0, 0, 0, 0)
# thaad = Missile(500, 500, 0)

startFrames = 0
startTime = 0
s = sched.scheduler(time.time, time.sleep)

randPlanets()
#threading.Thread(target=fpsCounter).start()
#fpsCounter()

def change():
    myfunc = next(itertools.cycle([0, 1]))
    return myfunc


def main():
    global center
    degrees = 0
    frames = 0

    centerList=[400,700]
    x=1
    global timeSec
    while True:  # main game loop
        #screen.fill(colourDict['black'])

        #d = abs(math.sqrt(((earth.xPos - centerList[x]) ** 2) + ((earth.yPos - centerList[x]) ** 2)))
        # if d < 100:
        #     if x == 1:
        #         center = 700
        #         x=0
        #         print('here')
        #     # if x== 0:
        #     #     center = 400
        #     #     x=1
        #d = abs(math.sqrt(((earth.xPos - centerList[x]) ** 2) + ((earth.yPos - centerList[x]) ** 2)))
        screen.blit(bg,(0,0))
        randColour = list(np.random.choice(range(256), size=3))
        timeSec = (pygame.time.get_ticks() - start_ticks) / 1000  # Time in Seconds
        rocketSpeed = (pygame.time.get_ticks() - start_ticks) / 1000
        #sol = pygame.draw.circle(screen, colourDict['brown'], (500, 500), 80)
        scaled = pygame.transform.scale(sol, (20, 20))
        rotated = pygame.transform.rotate(scaled, degrees)
        rect = rotated.get_rect()
        #sun = screen.blit(rotated, (500 - rect.center[0], 500 - rect.center[1]))
        if degrees < 359:
            degrees += (1/4)
        else:
            degrees = 0
        #sun = screen.blit(rotated, (500 - rect.center[0], 500 - rect.center[1]))
        sun = screen.blit(rotated, (400, 400))
        sun = screen.blit(rotated, (700, 700))
        #sol = pygame.image.load('sol.png')
        updater()
        eventHandler()
        pygame.display.update()
        fpsClock.tick(fps)  # Same as time.sleep(1/fps) I think
        frames += 1
        pressed = pygame.key.get_pressed()
        if 1 in pressed:
            keyboard()


def other():
    while True:
        time.sleep(1)
        print('seconds')


if __name__ == '__main__':
    main()

'''
def fpsCounter():
    global startTime
    #print("yall")
    timy = int(((pygame.time.get_ticks() - start_ticks) / 1000)/timeSec)
    print(timy)
    print(timeSec)
    time.sleep(1)
    if timeSec-timy > 1:
        print('sec')
        startTime = timeSec
        startFrames = frames
        #print(startTime)'''


'''def scale():# Takes arguements that need changing
    change value by factor
    return avlue'''
'''
def scale(input):
    input-500
    return input()'''








