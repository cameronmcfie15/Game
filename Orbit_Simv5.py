# Made By Cameron McFie
"""
TO DO:
Rotate using surface for sprites 
Use better collisions
need to define radius attribute somehow
Use google sheets for high scores
Add shields, gravity well, difficulty (rate of aster spawns, lives)
"""

import pygame, sys, random, math, time, threading, trace, itertools, profile, os
import numpy as np
from win32api import GetSystemMetrics

print(sys.platform)
# --Setup--
# Declaring / Assigning Variable
pygame.init()  # Inizialises all of pygame
monitorWidth = (GetSystemMetrics(0))
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((monitorWidth-1280)/2, 50)  # Location of Window
#pygame.mixer.init()  # Inizialises sound in pygame
fps = 60  # Framerate, controls physics
fpsClock = pygame.time.Clock()  # Sets up the pygame clock
start_ticks = pygame.time.get_ticks()
width, height = 1280, 960  # Window dimensions
screen = pygame.display.set_mode((width, height))  # Sets up the screen
font = pygame.font.SysFont('Verdana', 18)  # Sets up the Font
center = height/2
randColour = list(np.random.choice(range(256), size=3))  # Returns a random colour
colourDict = {'white': (255, 255, 255), 'brown': (160, 82, 45), 'black': (0, 0, 0)}  # Predefined dictionary of colours
bg = pygame.image.load('Images/background1.png')  # Loads in the background image
heart = pygame.image.load('Images/Heart.png')
pygame.Surface.convert(bg)  # Don't have to do this. but meant to
asteroidRate = 50  # bigger = slower
# Constants
Mass = 4*10**13  # Mass of Centre   5.972*10**24
G = 6.67*10**-11  # Gravity Constant    6.67*10**-11
# Other Setup
pygame.Surface.convert(bg)
heart = pygame.transform.scale(heart, (12, 12))
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


def volume(sound):
    return sound.set_volume(0.0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.xPos, self.yPos = width/2, height/2
        self.xVel, self.yVel, self.xAcceleration, self.yAcceleration, self.force, self.angle = 0, 0, 0, 0, 0, 0
        self.decay = 0.98
        self.radius = 20
        self.triangle, self.x, self.y, self.velVector = [], [], [], []
        self.deathTime = 0
        self.cash = 0
        self.shotSpeed = 5
        self.shield = 0
        self.lives = 3
        self.score = 0
        self.died = False
        # self.rect = pygame.Rect(self.xPos, self.yPos, self.radius, self.radius)

    def update(self):  # Is called every tick
        if self.shield >= 1:
            pygame.draw.circle(screen, colourDict['white'], (int(self.xPos), int(self.yPos)), self.radius+5, 2)

        self.updatePoly()
        self.posistionUpdate()
        self.velVector = [math.atan2(self.xVel, self.yVel), math.sqrt(self.xVel**2+self.yVel**2)]  # Theta ,absolute
        self.force = 0  # Resets force when button is not pushed down
        # self.rect = pygame.Rect(self.xPos, self.yPos, self.radius, self.radius)
        # Above line and same for init  not needed at the moment but may be needed for other collisions

    def sound(self):
        pass

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

    def hit(self):
        if self.shield >= 1:
            self.shield -= 1
        else:
            player.lives -= 1
            if player.lives == 0:
                print("You died!")
                self.deathTime = timeCount
                player.died = True
                self.reset()

    def reset(self):
        self.shotSpeed = 0
        self.cash = 0
        #sys.exit()

    def buyMenu(self, pressed):
        if self.cash >= 5:
            self.shield += 1
            self.cash -= 5



class Asteroids(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, xVel, yVel ,mass, radius):
        pygame.sprite.Sprite.__init__(self)
        asteroidList.append(self)  # Put into list so it can be easily destroyed and checked for stuff like collisions
        self.polyList, self.xy, self.poly, self.velVector, self.pos = [], [], [], [], []
        self.x, self.y, self.angle, self.force = 0, 0, 0, 0
        self.density = 100
        self.distance = 0
        self.radiiSum = 0
        # Making things random unless preassigned a value
        if xPos == 0 and yPos == 0:
            self.spawnPos()
        else:
            self.xPos = xPos
            self.yPos = yPos
        if xVel == 0 and yVel == 0:  # Making the velocities random
            self.xVel = random.uniform(-2, 2)
            self.yVel = random.uniform(-2, 2)
        else:  # Else already predefined
            self.xVel = xVel
            self.yVel = yVel
        if -0.2 <= self.xVel <= 0.2 or -0.2 <= self.yVel <= 0.2:  # Checking to see if it's to slow, if so, destroys it
            self.death()
        if radius == 0:  # Same of spin
            self.radius = random.randint(10, 100)
        else:
            self.radius = radius
        if mass == 0:
            self.mass = self.radius * self.density
        else:
            self.mass = mass
        self.rotationSpeed = random.uniform(-0.05, 0.05)
        self.momentum = int(self.mass * math.sqrt(self.xVel ** 2 + self.yVel ** 2))
        self.makeShape()
        self.rect = pygame.Rect(self.xPos, self.yPos, self.radius, self.radius)

    def death(self):
        if self in asteroidList:
            asteroidList.remove(self)

    def explodeSound(self):
        thrustSound = pygame.mixer.Sound('Sounds/bangMedium.wav')
        thrustSound.play()
        volume(thrustSound)

    def hit(self):
        self.explodeSound()
        if self.mass >= 7500:
            player.score += 100
            player.cash += 1
            for i in range(0, 4):
                self.newXVel = random.uniform(self.xVel - math.pi / 2, self.xVel + math.pi / 2)
                self.newYVel = random.uniform(self.yVel - math.pi / 2, self.yVel + math.pi / 2)
                Asteroids(self.xPos, self.yPos, self.newXVel, self.newYVel, self.mass/2, self.radius/4)
                # new direction max 90 degrees maybe definitely random
        elif self.mass >= 5000:
            player.score += 75
            player.cash += 0.75
            for i in range(0, 3):
                self.newXVel = random.uniform(self.xVel - math.pi / 2, self.xVel + math.pi / 2)
                self.newYVel = random.uniform(self.yVel - math.pi / 2, self.yVel + math.pi / 2)
                Asteroids(self.xPos, self.yPos, self.newXVel, self.newYVel, self.mass/3, self.radius/3)
        elif self.mass >= 2500:
            player.score += 50
            player.cash += 0.50
            for i in range(0, 2):
                self.newXVel = random.uniform(self.xVel - math.pi / 2, self.xVel + math.pi / 2)
                self.newYVel = random.uniform(self.yVel - math.pi / 2, self.yVel + math.pi / 2)
                Asteroids(self.xPos, self.yPos, self.newXVel, self.newYVel, self.mass/4, self.radius/2)
        else:
            player.score += 25
            player.cash += 0.25
            self.death()

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
            player.hit()
        for shot in shotList:
            if distance(shot.pos, self.pos) < shot.radius + self.radius:
                self.hit()
                shot.death()
                self.death()


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
        self.rocket = pygame.image.load('Images/missile1.png')
        self.rect = self.rocket.get_rect()
        missileList.append(self)

    def update(self):
        if frames % 2 == 0:
            self.rocket = pygame.image.load('Images/missile1.png')
        else:
            self.rocket = pygame.image.load('Images/missile2.png')
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
        print('died', count)
        rocketSpeed = 0

    def positionUpdate(self):
        self.distance = math.sqrt(((self.target.xPos - self.xPos) ** 2) + ((self.target.yPos - self.yPos) ** 2))
        #self.line = pygame.draw.line(screen, colourDict['white'], (self.xPos, self.yPos), (earth.xPos, earth.yPos), 1)
        self.opposite = (self.target.yPos - self.yPos)  # Works out distance between the y axis
        self.adjacent = (self.target.xPos - self.xPos)  # Works out distance between the x axis
        #self.angle = math.atan2(self.opposite, self.adjacent)
        #self.xVel = math.cos(self.angle)*self.distance*0.05
        #self.yVel = math.sin(self.angle)*self.distance*0.05
        self.xVel = (self.adjacent/self.distance)
        self.yVel = (self.opposite/self.distance)
        self.xPos += self.xVel # * timeSec  # Time sec works well for 1 target but needs to reset for multiply tartgets
        self.yPos += self.yVel # * timeSec
        self.rotater()

    def rotater(self):
        self.direction = math.atan2(self.opposite, self.adjacent) * -1
        self.rotated = pygame.transform.rotate(self.rocket, math.degrees(self.direction)-90)
        self.missile = screen.blit(self.rotated, (self.xPos, self.yPos))


class Shot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        shotList.append(self)
        self.sound()
        self.angle, self.xPos, self.yPos = player.angle, player.xPos, player.yPos
        self.xVel = math.sin(self.angle) * player.shotSpeed
        self.yVel = math.cos(self.angle) * player.shotSpeed
        self.distance = 0
        self.radius = 4
        self.pos = [self.xPos, self.yPos]
        self.rect = pygame.Rect(self.xPos, self.yPos, self.radius, self.radius)

    def sound(self):
        fireSound = pygame.mixer.Sound('Sounds/fire.wav')
        fireSound.play()
        volume(fireSound)

    def update(self):
        self.pos = [self.xPos, self.yPos]
        self.xPos += self.xVel
        self.yPos += self.yVel
        self.shot = pygame.draw.circle(screen, colourDict['white'], (int(self.xPos), int(self.yPos)), self.radius)
        self.distance = abs(math.sqrt(((self.xPos - center) ** 2) + ((self.yPos - center) ** 2)))
        self.rect = pygame.Rect(self.xPos, self.yPos, self.radius, self.radius)
        if self.distance > 1000:
            self.death()

    def death(self):
        shotList.remove(self)


class Alien:
    def __init__(self):
        pass


class Menu:
    def __init__(self):
        pass


class Button:
    def __init__(self, text, x_pos, y_pos, button_width, button_height):
        self.xPos = x_pos - (button_width/2)  # Top left corner of x, y posistions for rect
        self.yPos = y_pos - (button_height/2)
        self.width = button_width
        self.height = button_height
        self.font = pygame.font.SysFont('Verdana', 18)
        self.mouse = pygame.mouse.get_pos()
        self.text = text
        self.pressed = False
        buttonList.append(self)  # x, y, width, height
        self.text_width, self.text_height = self.font.size(self.text)
        self.w = self.xPos+(self.width-self.text_width)/2  # x, y  coordinates for text
        self.h = self.yPos+(self.height - self.text_height) / 2

    def update(self):
        pygame.draw.rect(screen, colourDict['white'], (self.xPos, self.yPos, self.width, self.height), 1)
        screen.blit(font.render(self.text, False, (colourDict['white'])), (self.w, self.h))
        self.mouse = pygame.mouse.get_pos()
        self.check()

    def check(self):
        if self.xPos < self.mouse[0] < int(self.xPos+self.width) and self.yPos < self.mouse[1] < int(self.yPos+self.height):
            menu(self)
    # Also got check if mouse is clicked and only LMB


def keyboard(pressed):
    global bPressed
    if pressed[pygame.K_5]:
        pass

    if pressed[pygame.K_3]:
        pass

    if pressed[pygame.K_2]:
        pass

    if pressed[pygame.K_1]:
        pass

    if pressed[pygame.K_SPACE]:
        player.force = 0.4


def hud():
    try:  # Last 2 digits are x,y     add plus 18 for new line
        for x in range(player.lives):
            screen.blit(heart, (18 * (5+x), 22))
        if player.died:
            screen.blit(font.render("YOU DIED!", True, (colourDict['white'])), (width / 2 - 48, height / 2))
        textList.update({"shot speed": "Shot Speed: "+str(player.shotSpeed)})
        textList.update({"score": "Score: "+str(player.score)})
        textList.update({"spawn rate": "Asteroid Spawn Rate: " + str(numberOfAsteroids)})
        textList.update({"lives": "Lives: "})
        textList.update({"shield": "Shield: " + str(player.shield)})
        textList.update({"cash": "Credits: " + str(player.cash)})
        screen.blit(font.render(textList["shot speed"], True, (colourDict['white'])), (width-172, 16 + 1 * 18))
        screen.blit(font.render(textList["score"], True, (colourDict['white'])), (width/2-48, 16))
        screen.blit(font.render(textList["lives"], True, (colourDict['white'])), (32, 16 + 0 * 18))
        screen.blit(font.render(textList["spawn rate"], True, (colourDict['white'])), (32, 16 + 1 * 18))
        screen.blit(font.render(textList["shield"], True, (colourDict['white'])), (32, 16 + 2 * 18))
        screen.blit(font.render(textList["cash"], True, (colourDict['white'])), (width-172, 16 + 0 * 18))
        screen.blit(font.render("Frame Rate:"+frameRate, True, (colourDict['white'])), (width/2-48, 16 + 1 * 18))
    except Exception as e:
        print(e)


def updater():  # print(len(planetList))
    if exitButton.pressed == True:
        for button in buttonList:
            button.update()
    for planet in planetList:
        planet.update()
    for sat in satList:
        sat.update()
    for missile in missileList:
        missile.update()
    for asteroid in asteroidList:
        asteroid.update()
    player.update()
    try:
        for shot in shotList:
            shot.update()
    except:
        pass


def eventHandler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            timeTaken()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pressed()
            if mouse[0] == 1:
                Shot()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                exitButton.pressed = True



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
    global timeCount
    global numberOfAsteroids
    global asteroidRate
    if timeCount % asteroidRate == 0:
        numberOfAsteroids += 1
    for i in range(0, numberOfAsteroids):  # Rotation , xPos, yPos
        Asteroids(0, 0, 0, 0, 0, 0)


def change():
    myfunc = next(itertools.cycle([0, 1]))
    return myfunc
    # PLus 1
    # When divisible by 2


def menu(button):
    if button == exitButton:
        mouse = pygame.mouse.get_pressed()
        if mouse[0] == 1:
            button.pressed = False



def main():  # A bit messy try clean up
    global center, totFrames, timeCount, frameRate, textList, numberOfAsteroids, player
    global planetList, satList, missileList, shotList, asteroidList, frameRate
    global frames, actualFps, count, startTime
    frames, actualFps, count, degrees, score, timeCount, totFrames, frames, cash = 0, 0, 0, 0, 0, 0, 0, 0, 0
    planetList, satList, missileList, shotList, asteroidList = [], [], [], [], []
    textList = {}
    text, frameRate = '', ''
    numberOfAsteroids = 1  # Number of asteroids per second
    s_time = time.time()
    startTime = time.time()
    player = Player()
    randAsteroids()





    while True:  # main game loop
        screen.fill(colourDict['black'])
        hud()
        # randColour = list(np.random.choice(range(256), size=3))
        updater()
        eventHandler()
        pygame.display.update()
        fpsClock.tick(fps)  # Same as time.sleep(1/fps) I think
        pressed = pygame.key.get_pressed()
        if 1 in pressed:
            keyboard(pressed)
        e_time = time.time()
        if e_time-s_time > 1:  # Is true when one seconds has passed
            timeCount += 1
            s_time = time.time()
            frameRate = str(frames)
            frames = 0
            randAsteroids()

        screen.blit(font.render(text, True, (colourDict['white'])), (32, 48))
        frames += 1
        if player.deathTime != 0:
            if timeCount - player.deathTime > 5:
                died = False
                player.deathTime = 0
                main()


buttonList = []
menuButton = Button("Menu", width/2, height/5, 250, 50)
livesButton = Button("Buy Lives", width / 2, height / 5 + 50, 250, 50)
shieldButton = Button("Buy Shields", width / 2, height / 5 + 100, 250, 50)
shotSpeedButton = Button("Buy Faster Shot Speed", width / 2, height / 5 + 150, 250, 50)
exitButton = Button("Exit", width / 2, height / 5 + 200, 250, 50)

if __name__ == '__main__':
    # Missile(0, 0, player)
    main()
    #profile.run('main()')    #or main()

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