import pygame, sys, time

pygame.init()
screen = pygame.display.set_mode((500, 400))
font = pygame.freetype.SysFont('arial', 18)
new_font = pygame.freetype.SysFont('Timesnewroman', 25)
new_font2 = pygame.freetype.SysFont('impact', 70)
text, text_rect = font.render("Welcome to Pygame Example!",(0,255,0))
fun, fun_rect = new_font.render("Enjoy with games", (0,255,255))
game_end, game_end_rect = new_font2.render("Game Ends", (255,0,0), rotation=5)
screen.fill((255, 255, 255)) 
screen.blit(text, (40,60))
screen.blit(fun, (40,90))
screen.blit(game_end, (40,140))
pygame.display.flip()

while True:
    time.sleep(1)