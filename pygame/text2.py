import pygame
pygame.init()
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
X = 500
Y = 400
display_surface = pygame.display.set_mode((X, Y))
print(display_surface)
pygame.display.set_caption('Text Rectangle')
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Python Pygame Tutorial', True, red, black)
textRect = text.get_rect()
textRect.center = (X // 2, Y // 2)
while True:
    display_surface.fill(white)
    display_surface.blit(text, textRect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        pygame.display.update()
