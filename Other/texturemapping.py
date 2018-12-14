# coding: utf-8

import random

import pygame, sys

SIZE = 800,600

def tile_texture(texture, size):
    result = pygame.Surface(size, depth=32)
    for x in range(0, size[0], texture.get_width()):
        for y in range(0, size[1], texture.get_height()):
            result.blit(texture,(x,y))
    return result


def apply_alpha(texture, mask):
    """
    Image should be  a 24 or 32bit image,
    mask should be an 8 bit image with the alpha
    channel to be applied
    """
    texture = texture.convert_alpha()
    target = pygame.surfarray.pixels_alpha(texture)
    target[:] = pygame.surfarray.array2d(mask)
    # surfarray objets usually lock the Surface.
    # it is a good idea to dispose of them explicitly
    # as soon as the work is done.
    del target
    return texture

def stamp(image, texture, mask):
    image.blit(apply_alpha(texture, mask), (0,0))


def main():
    screen = pygame.display.set_mode(SIZE)
    screen.fill((255,255,255))
    texture = tile_texture(pygame.image.load("texture.png"), SIZE)  # Turns image in to texture
    mask = pygame.Surface(SIZE, depth=8)
    # Create sample mask:
    pygame.draw.polygon(mask, 255,
                        [(random.randrange(SIZE[0]), random.randrange(SIZE[1]) )
                         for _ in range(5)] , 0)

    stamp(screen, texture, mask)
    pygame.display.flip()
    while not any(pygame.key.get_pressed()):
        pygame.event.pump()
        pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



if __name__ == "__main__":
    pygame.init()
    try:
        main()
    finally:
        pygame.quit()