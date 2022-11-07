import pygame, time
pygame.init()
scr = pygame.display.set_mode((600, 500))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    scr.fill((255, 255, 255))
    pygame.draw.circle(scr, (200, 0, 0), (250, 250), 80)
    pygame.display.flip()
    while True:
        time.sleep(1)
pygame.quit()