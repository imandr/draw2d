import pygame, sys, time

pygame.init()
screen = pygame.display.set_mode((500, 400))
font = pygame.font.SysFont('arial', 18)
new_font = pygame.font.SysFont('Timesnewroman', 25)
new_font2 = pygame.font.SysFont('impact', 70)
text = font.render("Welcome to Pygame Example!",True, (0,255,0))
fun = new_font.render("Enjoy with games", True, (0,255,255))
game_end = new_font2.render("Game Ends", True, (255,0,0))
screen.fill((255, 255, 255)) 
screen.blit(text, (40,60))
screen.blit(fun, (40,90))
screen.blit(game_end, (40,140))
pygame.display.flip()

while True:
    time.sleep(1)