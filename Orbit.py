# Made By Cameron McFie
"""
TO DO:
Need to randomise gravity well,
THATS IT
Tidy up remove unnecessary things
"""

# Ctrl+Shift+NumPad -      To fold all
import pygame, sys, random, math, time, os
import numpy as np
from settings import *
from win32api import GetSystemMetrics
import tkinter


# --Setup--
# Declaring / Assigning Variable
pygame.init()  # Inizialises all of pygame
monitorWidth = (GetSystemMetrics(0))
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((monitorWidth-WINDOWWIDTH)/2, 50)  # Location of Window
fps = FRAMERATE  # Framerate, controls physics
fpsClock = pygame.time.Clock()  # Sets up the pygame clock
start_ticks = pygame.time.get_ticks()
width, height = WINDOWWIDTH, WINDOWHEIGHT  # Window dimensions
screen = pygame.display.set_mode((width, height))  # Sets up the screen
font = pygame.font.SysFont('Verdana', 18)  # Sets up the Font
center = height/2
randColour = list(np.random.choice(range(256), size=3))  # Returns a random colour
colourDict = {'white': (255, 255, 255), 'brown': (160, 82, 45), 'black': (0, 0, 0)}  # Predefined dictionary of colours
heart = pygame.image.load('Images\Heart.png')
alien = pygame.image.load('Images\Alien.png')
asteroidRate = ASTEROIDRATE  # bigger = slower
gravity = False
# Constants
Mass = 4*10**13  # Mass of Centre   5.972*10**24
G = 6.67*10**-11  # Gravity Constant    6.67*10**-11
# Other Setup
heart = pygame.transform.scale(heart, (12, 12))
# --All the functions --


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
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, colourDict['white'], (self.xPos, self.yPos, self.width, self.height), 5)
                    menu(self.text)


buttonList = []
missileButton = Button("Buy Missile", width / 2, (height / 5), 250, 50)
livesButton = Button("Buy Lives", width / 2, (height / 5) + 50, 250, 50)
shieldButton = Button("Buy Shields", width / 2, (height / 5) + 100, 250, 50)
shotSpeedButton = Button("Buy Faster Shot Speed", width / 2, (height / 5) + 150, 250, 50)
exitButton = Button("Exit", width / 2, (height / 5) + 200, 250, 50)


def start():
    if __name__ == '__main__':
        root.destroy()
        main()
        # try:
        #     main()
        # except Exception as e:
        #     print(e)
        #

def distance(v1, v2):  # Vectors 1 and 2
    return math.sqrt((v1[0]-v2[0])**2 + (v1[1]-v2[1])**2)


class Player:
    def __init__(self):
        self.grav = pygame.math.Vector2(width / 2, height / 2)
        self.pos = pygame.math.Vector2(width / 2, height / 2)
        self.xVel, self.yVel, self.xAcceleration, self.yAcceleration, self.force, self.angle = 0, 0, 0, 0, 0, 0
        self.planetList, self.missileList, self.shotList, self.asteroidList, self.alienList = [], [], [], [], []
        self.decay = DECAY
        self.radius = 20
        self.triangle, self.x, self.y, self.velVector, self.triThrust, self.alienShotList = [], [], [], [], [], []
        self.deathTime = 0
        self.cash = CASH
        self.shotSpeed = SHOTSPEED
        self.shield = SHIELD
        self.lives = LIVES
        self.score = 0
        self.died = False
        self.distance = 0
        self.xA, self.yA, self.gForce = 0, 0, 0
        self.force = 0
        self.missiles = 0
        self.cost = 5
        self.vector = pygame.math.Vector2()
        self.vel, self.acc, self.thrustPos = self.vector, self.vector, self.vector
        self.front, self.left, self.right = self.vector, self.vector, self.vector

    def update(self):  # Is called every tick
        player.cost = int(4 + math.e**(timeCount*0.01))
        list(map(int, self.pos))
        if self.shield >= 1:
            pygame.draw.circle(screen, colourDict['white'], (int(self.pos.x), int(self.pos.y)), self.radius+5, 2)
        self.updatePoly()
        self.posistionUpdate()
        self.force = 0  # Resets force when button is not pushed down

    def sound(self):
        pass

    def updatePoly(self):
        self.x, self.y = [], []  # Resets list of points so the previous points are not drawn again
        self.triangle = [0, (3 * math.pi / 4), (5 * math.pi / 4)]  # Points around a circle describing a triangle
        self.triangle = map(lambda x: x+(2*math.pi/4), self.triangle)  # Adding 90 degrees to angles
        for t in self.triangle:  # Makes these angles to x, y pos
            self.x.append(self.pos.x + self.radius * math.cos(t + -self.angle))   # Adds these coordinates to list
            self.y.append(self.pos.y + self.radius * math.sin(t + -self.angle))   # Where the magic happens
        self.triangle = [(self.x[0], self.y[0]), (self.x[1], self.y[1]), (self.x[2], self.y[2])]  # X, Y Pos List
        self.triangle = pygame.draw.polygon(screen, colourDict['white'], self.triangle, 2)  # Draws the ship
        if self.force != 0:  # Thrust Animation
            self.thrustPos = pygame.math.Vector2(int(self.pos.x-15 * math.sin(self.angle)), int(self.pos.y-15 * math.cos(self.angle)))
            self.front = pygame.math.Vector2(0, -self.radius/2)
            self.front.rotate_ip(math.degrees(-self.angle))
            self.left = self.front.rotate(-90)
            self.right = self.front.rotate(90)
            pygame.draw.line(screen, (255, 255, 255), (self.thrustPos + self.front), (self.thrustPos + self.left), 2)
            pygame.draw.line(screen, (255, 255, 255), (self.thrustPos + self.front), (self.thrustPos + self.right), 2)

    def posistionUpdate(self):
        self.angle = list(pygame.mouse.get_pos())  # Calculating angle in rads of mouse from the player
        self.angle = [self.angle[0]-self.pos.x, self.angle[1]-self.pos.y]
        self.angle = (math.atan2(self.angle[0], self.angle[1]))
        if gravity:
            pygame.draw.circle(screen, colourDict['white'], (int(self.grav.x), int(self.grav.y)), 5)
            self.distance = abs(math.sqrt(((self.pos.x - self.grav.x) ** 2) + ((self.pos.y - self.grav.y) ** 2)))
            self.gForce = 50 / self.distance ** 1.05  # V = GM/r
        else:
            self.gForce = 0
        if self.distance < 200:
            self.gForce = 0.3
        if gravity:
            self.xA = self.gForce * (self.grav.x - self.pos.x) / self.distance
            self.yA = self.gForce * (self.grav.y - self.pos.y) / self.distance
        else:
            self.xA = 0
            self.yA = 0
        self.acc = (math.sin(self.angle) * self.force + self.xA, math.cos(self.angle) * self.force + self.yA)
        self.vel *= self.decay
        self.vel += self.acc
        self.pos += self.vel

    def hit(self):
        if self.shield >= 1:
            self.shield -= 1
        else:
            player.lives -= 1
            if player.lives == 0:
                self.deathTime = timeCount
                player.died = True
                self.reset()

    def reset(self):
        self.shotSpeed = 0
        self.cash = 0


class Asteroids:
    def __init__(self, xPos, yPos, xVel, yVel ,mass, radius):
        player.asteroidList.append(self)  # Put into list so it can be easily destroyed and checked for stuff like collisions
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
        if self in player.asteroidList:
            player.asteroidList.remove(self)


    def hit(self):
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
        self.asteroid = pygame.draw.polygon(screen, colourDict['white'], self.poly, 2)  # Draws the ship

    def collisions(self):
        self.distance = math.sqrt(abs((self.xPos - player.pos.x)**2+(self.yPos-player.pos.y)**2))
        if self.distance + 2 < player.radius + self.radius:  # the plus 2 gives a bit or breathing room
            self.death()
            player.hit()
        for shot in player.shotList:
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


class Alien:
    def __init__(self):
        self.w = 0.04  # Rotational Velocity
        self.radius = 40
        self.alien = pygame.transform.scale(alien, (50, 30))
        self.pos = pygame.math.Vector2()
        self.vel = pygame.math.Vector2()
        self.count, self.angle = 0, 0
        player.alienList.append(self)
        self.axisStart = random.choice([0, 1])
        self.axisStart = 0
        if self.axisStart == 1:
            self.pos.x = random.randint(-50, width + 50)
            self.pos.y = random.choice([-50, height + 50])
            if self.pos.y == -50:
                self.vel.y = random.uniform(0.5, 2)
                self.vel.x = random.uniform(-1, 1)
            else:
                self.vel.y = random.uniform(-2, -0.5)
                self.vel.x = random.uniform(-1, 1)
        else:
            self.pos.x = random.choice([-50, width + 50])
            self.pos.y = random.randint(-50, height + 50)
            if self.pos.x == -50:
                self.vel.y = random.uniform(-1, 1)
                self.vel.x = random.uniform(0.5, 2)
            else:
                self.vel.y = random.uniform(-1, 1)
                self.vel.x = random.uniform(-0.5, -2)

    def update(self):
        global alien, gravity
        alien = pygame.transform.scale(alien, (50, 30))
        self.count += 1
        self.bound_check()
        self.update_pos()
        self.star(0)
        self.star(2*math.pi/3)
        self.star(4*math.pi/3)
        self.shotChance = random.randint(0, 100)
        if self.shotChance <= 2:
            self.shoot()

    def shoot(self):
        self.angle = random.uniform(-2*math.pi, 2*math.pi)
        AlienShot(self.angle, self.pos.x+25, self.pos.y+15)

    def update_pos(self):
        self.alien = pygame.transform.scale(self.alien, (50, 30))
        self.pos += self.vel
        screen.blit(alien, (self.pos[0], self.pos[1]))

    def star(self, start_pos):
        self.count += 1
        pos = list()
        pos.append(self.radius * math.cos(self.w*self.count+start_pos) + self.pos[0] + 25)
        pos.append(self.radius * math.sin((self.w*self.count+start_pos)) + self.pos[1] + 15)
        pygame.draw.circle(screen, colourDict['white'], (int(pos[0]), int(pos[1])), 2)

    def bound_check(self):
        if self.pos.x < -100 or self.pos.x > (width+100) or self.pos.y < -100 or self.pos.y > (width+100):
            if self in player.alienList:
                player.alienList.remove(self)


class Missile:
    def __init__(self, pos, target):
        player.missileList.append(self)
        self.pos = pygame.math.Vector2(player.pos.x, player.pos.y)
        self.startPos = pygame.math.Vector2(player.pos.x, player.pos.y)
        self.xVel, self.yVel, self.angle = 0, 0, 0
        self.radius = 7
        self.triangle, self.x, self.y, self.velVector, self.triThrust = [], [], [], [], []
        self.score = 0
        self.distance = 0
        self.xA, self.yA, self.gForce = 0, 0, 0
        self.force = 0
        self.vel = pygame.math.Vector2()
        self.asterList = {}
        self.seeking = True
        self.lowest = 0
        self.target = pygame.mouse.get_pos()
        self.speed = 5
        self.startTime = time.time()
        player.missiles -= 1


    def update(self):  # Is called every tick
        list(map(int, self.pos))
        self.updatePoly()
        self.posistionUpdate()
        if self.seeking:
            if time.time() - self.startTime > 0.5:
                for asteroid in player.asteroidList:
                    self.asterList.update({asteroid: distance(self.pos, [asteroid.xPos, asteroid.yPos])})
                    self.lowest = (min(self.asterList, key=self.asterList.get))
                    self.target = [self.lowest.xPos, self.lowest.yPos]
                self.seeking = False
        elif distance(self.pos, [self.lowest.pos[0], self.lowest.pos[1]]) < self.lowest.radius:
            self.lowest.hit()
            self.lowest.death()
            self.destroy()
        else:
            self.target = [self.lowest.xPos, self.lowest.yPos]

    def sound(self):
        pass

    def updatePoly(self):
        self.x, self.y = [], []  # Resets list of points so the previous points are not drawn again
        self.triangle = [0, (3 * math.pi / 4), (5 * math.pi / 4)]  # Points around a circle describing a triangle
        self.triangle = map(lambda x: x+(2*math.pi/4), self.triangle)  # Adding 90 degrees to angles
        for t in self.triangle:  # Makes these angles to x, y pos
            self.x.append(self.pos.x + self.radius * math.cos(t + -self.angle))   # Adds these coordinates to list
            self.y.append(self.pos.y + self.radius * math.sin(t + -self.angle))   # Where the magic happens
        self.triangle = [(self.x[0], self.y[0]), (self.x[1], self.y[1]), (self.x[2], self.y[2])]  # X, Y Pos List
        self.triangle = pygame.draw.polygon(screen, colourDict['white'], self.triangle, 2)  # Draws the ship

    def posistionUpdate(self):
        self.angle = (math.atan2(self.target[0] - self.pos.x, self.target[1] - self.pos.y))
        self.vel = pygame.math.Vector2(math.sin(self.angle), math.cos(self.angle))
        self.pos += self.vel * self.speed

    def destroy(self):
        player.missileList.remove(self)


    def reset(self):
        self.shotSpeed = 0
        self.cash = 0


class Shot:
    def __init__(self, angle, xPos, yPos):
        player.shotList.append(self)
        self.angle, self.xPos, self.yPos = angle, xPos, yPos
        self.xVel = math.sin(self.angle) * player.shotSpeed
        self.yVel = math.cos(self.angle) * player.shotSpeed
        self.distance = 0
        self.radius = 4
        self.pos = [xPos, yPos]
        self.rect = pygame.Rect(self.xPos, self.yPos, self.radius, self.radius)


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
        player.shotList.remove(self)


class AlienShot(Shot):
    def __init__(self, angle, xPos, yPos):
        super().__init__(angle, xPos, yPos)
        player.alienShotList.append(self)

    def updateShot(self):
        if distance([self.xPos, self.yPos],[player.pos.x, player.pos.y]) < player.radius+self.radius:
            try:
                player.shotList.remove(self)
                player.alienShotList.remove(self)
                player.hit()
            except:
                pass


def keyboard(pressed):
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
        textList.update({"missile": "Missiles: " + str(player.missiles)})
        textList.update({"lives": "Lives: "})
        textList.update({"shield": "Shield: " + str(player.shield)})
        textList.update({"cash": "Credits: " + str(player.cash)})
        textList.update({"time": "Time: " + str(timeCount) + "  " + str(default.get())})
        textList.update({"cost": "Cost: " + str(player.cost)})
        screen.blit(font.render(textList["missile"], True, (colourDict['white'])), (width-172, 16 + 2 * 18))
        screen.blit(font.render(textList["score"], True, (colourDict['white'])), (width/2-48, 16))
        screen.blit(font.render(textList["lives"], True, (colourDict['white'])), (32, 16 + 0 * 18))
        screen.blit(font.render(textList["missile"], True, (colourDict['white'])), (32, 16 + 1 * 18))
        screen.blit(font.render(textList["shield"], True, (colourDict['white'])), (32, 16 + 2 * 18))
        screen.blit(font.render(textList["cash"], True, (colourDict['white'])), (width-172, 16 + 1 * 18))
        screen.blit(font.render(textList["time"], True, (colourDict['white'])), (width - 172, 16 + 0 * 18))
        screen.blit(font.render(textList["cost"], True, (colourDict['white'])), (width / 2 - 48, 16 + 1 * 18))
        screen.blit(font.render("Frame Rate:"+frameRate, True, (colourDict['white'])), (width/2-48, 16 + 2 * 18))
    except Exception as e:
        print(e)


def updater():
    if exitButton.pressed:
        for button in buttonList:
            button.update()
    for planet in player.planetList:
        planet.update()
    for missile in player.missileList:
        missile.update()
    for asteroid in player.asteroidList:
        asteroid.update()
    for alien in player.alienList:
        alien.update()
    player.update()
    try:
        for shot in player.alienShotList:
            shot.updateShot()
        for shot in player.shotList:
            shot.update()
    finally:
        pass


def event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pressed()
            if mouse[0] == 1:
                Shot(player.angle, player.pos.x, player.pos.y)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                exitButton.pressed = True
            if event.key == pygame.K_m and player.missiles > 0:
                Missile(player.pos, player)
            if event.key == pygame.K_2 and player.cash > player.cost:
                if player.lives < 5:
                    player.lives += 1
                    player.cash -= player.cost
            if event.key == pygame.K_3 and player.cash > player.cost:
                if player.shield < 10:
                    player.shield += 1
                    player.cash -= player.cost
            if event.key == pygame.K_1 and player.cash > player.cost:
                if player.missiles < 10:
                    player.missiles += 1
                    player.cash -= player.cost
            if event.key == pygame.K_4 and player.cash > player.cost:
                if player.shotSpeed < 30:
                    player.shotSpeed += 5
                    player.cash -= player.cost


def rand_spawns():
    global timeCount
    global numberOfAsteroids
    global asteroidRate
    global gravity
    global counted
    startTime = 0
    if timeCount % 5 == 0:
        if random.randint(0, player.cost) > 4:
            Alien()
    if timeCount % asteroidRate == 0:
        numberOfAsteroids += 1
    for i in range(0, numberOfAsteroids):  # Rotation , xPos, yPos
        Asteroids(0, 0, 0, 0, 0, 0)
    if timeCount % 30 == 0:
        gravity = True
        player.grav = pygame.math.Vector2(random.randint(100, width-100), random.randint(100, height-100))
    if gravity:
        counted += 1
    if counted > 10:
        gravity = False


def menu(button):
    mouse = pygame.mouse.get_pressed()
    if mouse[0] == 1:
        if button == exitButton:
            button.pressed = False
        if button == livesButton and player.cash > player.cost:
            if player.lives < 5:
                player.lives += 1
                player.cash -= player.cost
        if button == shieldButton and player.cash > player.cost:
            if player.shield < 10:
                player.shield += 1
                player.cash -= player.cost
        if button == missileButton and player.cash > player.cost:
            if player.missiles < 10:
                player.missiles += 1
                player.cash -= player.cost
        if button == shotSpeedButton and player.cash > player.cost:
            if player.shotSpeed < 30:
                player.shotSpeed += 5
                player.cash -= player.cost


def main():  # A bit messy try clean up  ["Easy", "Normal", "Hard", "Extreme"]
    global totFrames, timeCount, frameRate, textList, numberOfAsteroids, player
    global frames, actualFps, startTime, gravity, asteroidRate, counted
    frames, actualFps, count, degrees, score, timeCount, totFrames, frames, cash, counted = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    textList = {}
    text, frameRate = '', ''
    numberOfAsteroids = ASTEROIDSPAWN
    if default.get() == 'Easy':
        asteroidRate *= 2
    elif default.get() == 'Hard':
        asteroidRate *= 0.5
    elif default.get() == 'Extreme':
        asteroidRate *= 0.2
      # Number of asteroids per second
    s_time = time.time()
    startTime = time.time()
    player = Player()
    player.planetList, satList, player.missileList, player.shotList, player.asteroidList = [], [], [], [], []
    rand_spawns()
    gravity = False
    while True:  # main game loop
        screen.fill(colourDict['black'])
        hud()
        updater()
        event_handler()
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
            rand_spawns()
        frames += 1
        if player.deathTime != 0:
            if timeCount - player.deathTime > 5:
                player.deathTime = 0
                main()


root = tkinter.Tk()

optionList = ["Easy", "Normal", "Hard", "Extreme"]
default = tkinter.StringVar()
default.set("Normal")

menu = tkinter.OptionMenu(root, default, *optionList).pack()
text = tkinter.Text(root, height=20, width=60)
text.pack()
text.insert(tkinter.END, "Orbit\n"
                         "A Game similar to the arcade game Asteroids\n"
                         "\n"
                         "Aim: Get the highest score possible by shooting"
                         " asteroids;\n"
                         "At random points during the game Aliens and Gravity Wells may appear\n"
                         "Missiles have an arming time of 0.5 seconds\n"
                         "Aliens are very powerful and cannot be destroyed\n"
                         "Be careful!\n"
                         "\n"
                         "Controls:\n"
                         "Space = Forward\n"
                         "Mouse = Direction of ship\n"
                         "M = Fire Missile\n"
                         "B = Buy Menu\n"
                         "1 = Buy Missiles\n"
                         "2 = Buy Lives\n"
                         "3 = Buy Shields\n"
                         "4 = Buy Faster Shot")
startButton = tkinter.Button(root, text="Start", command=start)
startButton.pack()

root.mainloop()



# scaled = pygame.transform.scale(sol, (20, 20))
# rotated = pygame.transform.rotate(scaled, degrees)
# screen.blit(rotated, (400, 400))