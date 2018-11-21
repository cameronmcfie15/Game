import pygame, sys

white, black = (255, 255, 255), (0, 0, 0)
screen_width, screen_height = 640, 480

pygame.init()
pygame.display.set_caption('Perfect Collision Detection Example')
screen = pygame.display.set_mode([screen_width, screen_height])
clock = pygame.time.Clock()

myImage = pygame.image.load('coll.png').convert()
myImage.set_colorkey(white)
myOtherImage = pygame.image.load('missile3.png').convert()
myOtherImage.set_colorkey(white)

# creating masks for the images
myImage_mask = pygame.mask.from_surface(myImage)
myOtherImage_mask = pygame.mask.from_surface(myOtherImage)

# this is where the images are
myImage_rect = myImage.get_rect()
myOtherImage_rect = myOtherImage.get_rect()

myImage_rect.topleft = (0, 115)
myOtherImage_rect.topleft = (0, 0)

pygame.mouse.set_visible(False)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    myOtherImage_rect.topleft = pygame.mouse.get_pos()

    screen.fill(white)
    screen.blit(myImage, myImage_rect.topleft)
    screen.blit(myOtherImage, myOtherImage_rect.topleft)

    # this is where we check for pixel perfect collision
    # observe the order mask variables are used in calculating offset and in overlap method
    offset_x, offset_y = (myOtherImage_rect.left - myImage_rect.left), (myOtherImage_rect.top - myImage_rect.top)
    if (myImage_mask.overlap(myOtherImage_mask, (offset_x, offset_y)) != None):
        print('Collision Detected!')
    else:
        print ('None')

    pygame.display.update()
    clock.tick(144)