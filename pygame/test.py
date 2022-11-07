import pygame, time
from pygame import gfxdraw

VIEWPORT_W, VIEWPORT_H = 500, 500

pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((VIEWPORT_W, VIEWPORT_H))
surf = pygame.Surface((VIEWPORT_W, VIEWPORT_H))
surf.fill((255, 255, 255))
#print("rect:", pygame.draw.rect(surf, (255, 255, 255), surf.get_rect()))

polygon = [
    (10, 30),
    (100, 350),
    (30, 400)
]

print("polygon:", pygame.draw.polygon(surf, 100, polygon, 10))

pygame.event.pump()
pygame.display.flip()

while True:
    time.sleep(1)