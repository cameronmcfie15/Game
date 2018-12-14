import pygame, sys, math
from pygame.locals import *


#converte in base ai gradi le cordinate x,y
#maxXY= surface MaxXY
#gradoRot = grado di rotazione
#distXY = spostamento in x,y lungo il vettore di cordinate locali dalle cordinate x,y

#movement from one point to another
def Move(t0,t1,psx,psy,speed):
    global mx
    global my

    speed = speed

    distance = [t0 - psx, t1 - psy]
    norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
    direction = [distance[0] / norm, distance[1 ] / norm]

    bullet_vector = [direction[0] * speed, direction[1] * speed]
    return bullet_vector
# Main Function
if __name__ == '__main__':
    pygame.init()
    FPS = 30 # frames per second setting
    fpsClock = pygame.time.Clock()
    # set up the window
    DISPLAYSURF = pygame.display.set_mode((800, 600), 0, 32)
    alfhaSurface = DISPLAYSURF.convert_alpha()
    pygame.display.set_caption('test')
    shipImg = pygame.image.load('ship.png')
    shipImgcpy=shipImg.copy()
    vetShip=pygame.math.Vector2(400,300)
    gradi = 0
    gradiRot=0
    mouseX=0
    mouseY=0
    SHIP_W=40
    SHIP_H=40
    vetMouse=pygame.math.Vector2(mouseX,mouseY)
    #main loop
    while True:
        DISPLAYSURF.fill((0,0,0))
        alfhaSurface.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                vetMouse=pygame.math.Vector2(mouseX,mouseY)

                gradiRot=math.atan2(vetShip.x-vetMouse.x, vetShip.y-vetMouse.y)
                gradiRot=math.degrees(gradiRot)
                pygame.display.set_caption(""+str(gradi) +"="+ str(gradiRot)+" "+ str(vetMouse.angle_to(vetShip)) )
        pygame.draw.line(alfhaSurface, (255,255,255), (vetShip.x+SHIP_W,vetShip.y+SHIP_H),(vetMouse.x,vetMouse.y),1)
        if gradi != int(gradiRot) :
            if gradiRot > gradi and gradi != gradiRot :
                gradi=gradi+1

            if gradiRot < gradi and gradi != gradiRot :
                gradi=gradi-1

            shipImgcpy=pygame.transform.rotate(shipImg.copy(),gradi)

        elif int(vetMouse.distance_to(vetShip)) >0:
            posNext=Move(mouseX,mouseY,vetShip.x+SHIP_W,vetShip.y+SHIP_H,1)
            vetShip=pygame.math.Vector2(vetShip.x+posNext[0],vetShip.y+posNext[1])


        alfhaSurface.blit(shipImgcpy, tuple(vetShip))
        DISPLAYSURF.blit(alfhaSurface,(0,0))
        pygame.display.update()
        fpsClock.tick(FPS)