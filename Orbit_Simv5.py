# Made By Cameron McFie
"""
TO DO:
Rotate using surface for sprites 
Use better collisions
need to define radius attribute somehow
"""

import pygame, sys, random, math, time, threading, trace, itertools, profile
import numpy as np

# --Setup--
# Declaring / Assigning Variable
pygame.init()  # Inizialises all of pygame
pygame.mixer.init()  # Inizialises sound in pygame
fps = 60  # Framerate, controls physics
fpsClock = pygame.time.Clock()  # Sets up the pygame clock
start_ticks = pygame.time.get_ticks()
width, height = 1200, 900  # Window dimensions
screen = pygame.display.set_mode((width, height))  # Sets up the screen
font = pygame.font.SysFont('Verdana', 18)  # Sets up the Font
center = height/2
randColour = list(np.random.choice(range(256), size=3))  # Returns a random colour
colourDict = {'white': (255, 255, 255), 'brown': (160, 82, 45), 'black': (0, 0, 0)}  # Predefined dictionary of colours
bg = pygame.image.load('background1.png')  # Loads in the background image
pygame.Surface.convert(bg)  # Don't have to do this. but meant to
posMovement = 0.00001
shotSpeed = 5
planetList, satList, missileList, shotList, asteroidList = [], [], [], [], []
text = ''
numberOfPlanets = 0
numberOfAsteroids = 10
SIZE = 100, 100
fired = 0  # Turns to 1 if shots have been fired
lives = 0
frames, actualFps, count, degrees = 0, 0, 0, 0
# Constants
Mass = 4*10**13  # Mass of Centre   5.972*10**24
G = 6.67*10**-11  # Gravity Constant    6.67*10**-11

# --All the functions --


def timeTaken():  # Function that calculates framerate of the application and wrights it to text file
    global totFrames
    endTime = time.time()
    file = open("times.txt","a")
    timeTaken = float(endTime-startTime)
    info = "This script took "+str(timeTaken)+" seconds"+" and had an average framerate of "+str(totFrames/timeTaken)
    print(totFrames, (totFrames/timeTaken))
    file.write(info+"\n")
    file.close()


def distance(v1, v2):  # Vectors 1 and 2
    return math.sqrt((v1[0]-v2[0])**2 + (v1[1]-v2[1])**2)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.xPos, self.yPos = 500, 500
        self.xVel, self.yVel, self.xAcceleration, self.yAcceleration, self.force, self.angle = 0, 0, 0, 0, 0, 0
        self.decay = 0.98
        self.radius = 20
        self.triangle, self.x, self.y, self.velVector = [], [], [], []
        # self.rect = pygame.Rect(self.xPos, self.yPos, self.radius, self.radius)

    def update(self):  # Is called every tick
        self.updatePoly()
        self.posistionUpdate()
        self.velVector = [math.atan2(self.xVel, self.yVel), math.sqrt(self.xVel**2+self.yVel**2)]  # Theta ,absolute
        self.force = 0  # Resets force when button is not pushed down
        # self.rect = pygame.Rect(self.xPos, self.yPos, self.radius, self.radius)
        # Above line and same for init  not needed at the moment but may be needed for other collisions

    def updatePoly(self):
        self.x, self.y = [], []  # Resets list of points so the previous points are not drawn again
        self.triangle = [0, (3 * math.pi / 4), (5 * math.pi / 4)]  # Points around a circle describing a triangle
        self.triangle = map(lambda x: x+(2*math.pi/4), self.triangle)  # Adding 90 degrees to angles
        for t in self.triangle:  # Makes these angles to x, y pos
            self.x.append(self.xPos + self.radius * math.cos(t + -self.angle))   # Adds these coordinates to list
            self.y.append(self.yPos + self.radius * math.sin(t + -self.angle))   # Where the magic happens
        self.triangle = [(self.x[0], self.y[0]), (self.x[1], self.y[1]), (self.x[2], self.y[2])]  # X, Y Pos List
        self.triangle = pygame.draw.polygon(screen, colourDict['white'], self.triangle, 2)  # Draws the ship

    def posistionUpdate(self):
        self.angle = list(pygame.mouse.get_pos())  # Calculating angle in rads of mouse from the player
        self.angle = [self.angle[0]-self.xPos,self.angle[1]-self.yPos]
        self.angle = (math.atan2(self.angle[0],self.angle[1]))
        self.xAcceleration = math.sin(self.angle) * self.force  # Calculating forces and directions to update posistions
        self.yAcceleration = math.cos(self.angle) * self.force
        self.xVel += self.xAcceleration
        self.yVel += self.yAcceleration
        self.xVel *= self.decay
        self.yVel *= self.decay
        self.xPos += self.xVel
        self.yPos += self.yVel

    def death(self):
        print("You died!")
        #sys.exit()

class Asteroids(pygame.sprite.Sprite):
    def __init__(self, xVel, yVel ,mass, spin):
        pygame.sprite.Sprite.__init__(self)
        asteroidList.append(self)  # Put into list so it can be easily destroyed and checked for stuff like collisions
        self.polyList, self.xy, self.poly, self.velVector, self.pos = [], [], [], [], []
        self.x, self.y, self.angle, self.force = 0, 0, 0, 0
        self.density = 100
        self.distance = 0
        self.radiiSum = 0
        # Making things random unless preassigned a value
        if xVel == 0:  # Making the velocities random
            self.xVel = random.uniform(-2, 2)
            self.yVel = random.uniform(-2, 2)
        else:  # Else already predefined
            self.xVel = xVel
            self.yVel = yVel
        if -0.2 <= self.xVel <= 0.2 or -0.2 <= self.yVel <= 0.2:  # Checking to see if it's to slow, if so, destroys it
            self.death()
        if spin == 0:  # Same of spin
            self.rotationSpeed = random.uniform(-0.05, 0.05)
        else:
            self.rotationSpeed = spin
        self.radius = random.randint(10, 100)
        if mass == 0:
            self.mass = self.radius * self.density
        else:
            self.mass = mass
        self.momentum = int(self.mass * math.sqrt(self.xVel ** 2 + self.yVel ** 2))
        self.spawnPos()
        self.makeShape()
        self.rect = pygame.Rect(self.xPos, self.yPos, self.radius, self.radius)

    def death(self):
        asteroidList.remove(self)

    def hit(self):
        if self.mass <= 2500:
            self.death()
        if self.mass > 2500:
            for i in range (0,2):
                Asteroids(0, 0, self.mass/2, 0)
                # new direction max 90 degrees maybe definitely random
        elif self.mass >= 5000:
            for i in range (0,3):
                Asteroids(0, 0, self.mass/3, 0)
        elif self.mass >= 7500:
            for i in range (0,4):
                Asteroids(0, 0, self.mass/4, 0)

    def makeShape(self):
        self.vertices = random.randint(12, 20)
        for i in range(0, self.vertices):
            self.point = random.uniform(0, math.tau)
            self.polyList.append(self.point)
        self.polyList.sort()

    def spawnPos(self):
        self.axisStart = random.choice([0, 1])
        if self.axisStart == 1:
            self.xPos = random.randint(-100, width + 100)
            self.yPos = random.choice([-100, height + 100])
        else:
            self.xPos = random.choice([-100, width + 100])
            self.yPos = random.randint(-100, height + 100)

    def update(self):
        self.pos = [self.xPos, self.yPos]
        self.velVector = [math.atan2(self.xVel, self.yVel), math.sqrt(self.xVel ** 2 + self.yVel ** 2)]
        self.drawPoly()
        self.posistionUpdate()
        self.boundCheck()
        self.collisions()
        self.force = 0  # Resets force when button is not pushed down
        self.poly = []
        self.rect = pygame.Rect(self.xPos, self.yPos, self.radius, self.radius)

    def drawPoly(self):
        self.angle += self.rotationSpeed
        for pt in self.polyList:  # Makes these angles to x, y pos
            self.x = self.xPos + self.radius * math.cos(pt+self.angle)
            self.y = self.yPos + self.radius * math.sin(pt+self.angle)
            self.xy = [self.x, self.y]  # Adds these coordinates to list
            self.poly.append(self.xy)  # Adds all coordinates to master list
        #self.asteroid = pygame.draw.circle(screen, colourDict['white'], (int(self.xPos), int(self.yPos)), self.radius, 2)
        self.asteroid = pygame.draw.polygon(screen, colourDict['white'], self.poly, 2)  # Draws the ship

    def collisions(self):
        #self.radiiSum = player.radius + self.radius
        self.distance = math.sqrt(abs((self.xPos - player.xPos)**2+(self.yPos-player.yPos)**2))
        #print(self.radiiSum, self.distance)
        if self.distance + 2 < player.radius + self.radius:  # the plus 2 gives a bit or breathing room
            self.death()
        for shot in shotList:
            if distance(shot.pos, self.pos) < shot.radius + self.radius:
                shot.death()
                self.death()
        # if pygame.sprite.collide_circle(self, player):
        #     self.death()
        #     player.death()
        # for shot in shotList:
        #     if pygame.sprite.collide_circle(self, shot):
        #         self.death()
        #         shot.death()


    def posistionUpdate(self):
        self.xPos += self.xVel
        self.yPos += self.yVel

    def boundCheck(self):
        if self.xPos < -300 or self.xPos > (width+300) or self.yPos < -300 or self.yPos > (width+300):
            self.death()


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

    def rotater(self):
        self.direction = math.atan2(self.opposite, self.adjacent) * -1
        self.rotated = pygame.transform.rotate(self.rocket, math.degrees(self.direction)-90)
        self.missile = screen.blit(self.rotated, (self.xPos, self.yPos))

class Shot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        shotList.append(self)
        global shotSpeed
        global fired
        self.angle, self.xPos, self.yPos = player.angle, player.xPos, player.yPos
        fired = 1
        self.xVel = math.sin(self.angle) * shotSpeed
        self.yVel = math.cos(self.angle) * shotSpeed
        self.distance = 0
        self.radius = 4
        self.pos = [self.xPos, self.yPos]
        self.rect = pygame.Rect(self.xPos, self.yPos, self.radius, self.radius)
        fireSound = pygame.mixer.Sound('fire.wav')
        fireSound.play()

    def update(self):
        self.pos = [self.xPos, self.yPos]
        self.xPos += self.xVel
        self.yPos += self.yVel
        self.shot = pygame.draw.circle(screen, colourDict['white'], (int(self.xPos), int(self.yPos)), self.radius)
        self.distance = abs(math.sqrt(((self.xPos - center) ** 2) + ((self.yPos - center) ** 2)))
        self.rect = pygame.Rect(self.xPos, self.yPos, self.radius, self.radius)
        if self.distance > 1000:
            self.death()
        #self.collisions()

    # def collisions(self):
    #     for aster in asteroidList:
    #         if pygame.sprite.collide_circle(self, aster):
    #             self.death()
    #             aster.death()

    def death(self):
        shotList.remove(self)

def keyboard():
    global pressed
    global shotSpeed
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_RIGHT]:
        player.moveRight()
        #planetList[0].xVel += posMovement

    if pressed[pygame.K_4]:
        shotSpeed = 20

    if pressed[pygame.K_3]:
        shotSpeed = 15

    if pressed[pygame.K_2]:
        shotSpeed = 10
        #planetList[0].yVel += posMovement

    if pressed[pygame.K_1]:
        shotSpeed = 5

    if pressed[pygame.K_SPACE]:
        player.force = 0.4

def hud():
    global text
    try:
        text = str(shotSpeed)
        screen.blit(font.render(text, True, (colourDict['white'])), (32, 48))
    except Exception as e:
        print(e)

def updater():  # print(len(planetList))
    for planet in planetList:
        planet.update()
    for sat in satList:
        sat.update()
    for missile in missileList:
        missile.update()
    for asteroid in asteroidList:
        asteroid.update()
    player.update()
    if fired == 1:
        for shot in shotList:
            shot.update()

def eventHandler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            timeTaken()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            Shot()

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

def randAsteroids():
    for i in range(0, numberOfAsteroids):  # Rotation , xPos, yPos
        Asteroids(0, 0, 0, 0)

def change():
    myfunc = next(itertools.cycle([0, 1]))
    return myfunc

def menu():
    pass

def main():
    global center  # A bit messy try clean up
    global totFrames
    totFrames = 0
    frames = 0
    text = ""
    sTime = time.time()
    global timeSec
    global startTime
    startTime = time.time()
    while True:  # main game loop
        screen.blit(bg,(0,0))  # Resets the screen
        hud()
        randColour = list(np.random.choice(range(256), size=3))
        timeSec = (pygame.time.get_ticks() - start_ticks) / 1000  # Time in Seconds
        updater()
        eventHandler()
        pygame.display.update()
        fpsClock.tick(fps)  # Same as time.sleep(1/fps) I think
        pressed = pygame.key.get_pressed()
        if 1 in pressed:
            keyboard()
        eTime = time.time()
        if eTime-sTime > 1:  # Is true when one seconds has passed
            print(text)
            sTime = time.time()
            text = str(frames)
            frames = 0
            randAsteroids()

        screen.blit(font.render(text, True, (colourDict['white'])), (32, 48))
        frames += 1
        totFrames += 1


if __name__ == '__main__':
    player = Player()
    randAsteroids()
    main()
    #profile.run('main()')

# scaled = pygame.transform.scale(sol, (20, 20))
# rotated = pygame.transform.rotate(scaled, degrees)
# screen.blit(rotated, (400, 400))
'''def scale(input):# Takes arguement that need changing
    change input by factor
    return value'''
'''    def tile_texture(self, texture, size):
        result = pygame.Surface(size, depth=32)
        for x in range(0, size[0], texture.get_width()):
            for y in range(0, size[1], texture.get_height()):
                result.blit(texture, (x, y))
        return result
'''