import pygame, sys, time
from transformation import Transform

def draw_text(surface, text, font, size, rotation, x, y, anchor_x, anchor_y):
    font = pygame.freetype.SysFont(font, size)
    straight_rect = font.get_rect(text)
    print("rect:", straight_rect)
    straight_rect.center = (0,0)
    rotated_rect = font.get_rect(text, rotation=rotation)
    print("rotated rect:", rotated_rect)
    rotated_rect.center = (0,0)
    anchor_x = {
        "left": straight_rect.left,
        "middle": 0,
        "right": straight_rect.right
    }[anchor_x]
    anchor_y = {
        "top": straight_rect.top,
        "middle": 0,
        "bottom": straight_rect.bottom
    }[anchor_y]
    print("anchor:", anchor_x, anchor_y)
    anchor_x, anchor_y = Transform.rotation(rotation, "deg")*(anchor_x, anchor_y) # rotated anchor relative to the left-top corner of rotated rect
    print("rotated anchor:", anchor_x, anchor_y)

    # anchor coordinates relative to the left-top corner of the rotated rect
    anchor_x = rotated_rect.width//2 + anchor_x
    anchor_y = rotated_rect.height//2 - anchor_y
    print("anchor relative to corner:", anchor_x, anchor_y)
    surf_w, surf_h = surface.get_size()
    font.render_to(surface, (x - anchor_x, y - anchor_y), text, (0,0,0), rotation=rotation)



pygame.init()
screen = pygame.display.set_mode((400, 400))
screen.fill((250, 250, 250))
for y in range(0, 400, 50):
    draw_text(screen, str(y), "Helvetica", 12, 0, 0, y, "left", "middle")
draw_text(screen, "hello there", "Helvetica", 24, 10, 200, 300, "right", "top")
pygame.draw.line(screen, (200, 50, 50), (200,0), (200,400))
pygame.draw.line(screen, (200, 50, 50), (0,300), (400,300))
pygame.display.flip()

while True:
    time.sleep(1)