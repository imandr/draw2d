import math
from .transformation import Transform
import pygame
import pygame.gfxdraw

RAD2DEG = 180.0/math.pi
DEG2RAD = math.pi/180.0

class Sprite(object):
    
    def __init__(self, hidden=False, transient=False):
        self.Hidden = hidden
        self.Transient = transient

    def hide(self):
        self.Hidden = True
        return self
    
    def show(self):
        self.Hidden = False
        return self

class Geom(Sprite):
    def __init__(self, hidden=False):
        Sprite.__init__(self, hidden)
        self.Color = pygame.Color(0,0,0,1)
        #self.attrs = [self._color]
        self.Translation = (0.0, 0.0)
        self.Angle = 0.0
        self.Scale = (1.0, 1.0)

    def move_to(self, newx, newy):
        self.Translation = (float(newx), float(newy))
        return self

    def move_by(self, deltax, deltay):
        return self.move_to(self.Translation[0]+deltax, self.Translation[1]+deltay)

    def rotate_to(self, angle, unit="rad"):
        if unit == "deg":
            angle *= DEG2RAD
        self.Angle = float(angle)
        return self
        
    def rotate_by(self, angle, unit="rad"):
        if unit == "deg":
            angle *= DEG2RAD
        self.Angle += angle
        return self

    def scale_to(self, newx, newy):
        self.Scale = (float(newx), float(newy))
        return self

    def scale_by(self, deltax, deltay):
        return self.scale_to(self.scale[0]*deltax, self.scale[1]*deltay)
        
    def render(self, surface, context):
        if not self.Hidden:
            #for attr in reversed(self.attrs):
            #    #print("Geom.render: attr:", attr)
            #    attr.enable()
            print("Geom.render1: self:", self)
            self.render1(surface, context*Transform(scale=self.Scale, translate=self.Translation, angle=self.Angle))
            #for attr in self.attrs:
            #    attr.disable()
                
    def render1(self, transforms):
        raise NotImplementedError

    def add_attr(self, attr):
        self.attrs.append(attr)
        return self
        
    def set_color(self, r, g, b, a=None):
        self.Color = pygame.Color(r, g, b, a) if a is not None else  pygame.Color(r, g, b)
        return self

    color = set_color

    def line_width(self, w):
        return self.add_attr(LineWidth(w))
        
    def transform(self, **args):
        self.transform = Transform(**args)
        return self
        
class Point(Geom):
    def __init__(self):
        Geom.__init__(self)
        
    def render1(self, surface, transform):
        x, y = transform * (0, 0)
        x = round(x)
        y = round(y)
        pygame.gfxdraw.pixel(surface, x, y, self.Color)
        
class FilledPolygon(Geom):
    def __init__(self, points):
        Geom.__init__(self)
        self.Points = points
        
    def render1(self, surface, transform):
        points = [transform*p for p in self.Points]
        #print("FilledPolygon: points:", points)
        pygame.draw.polygon(surface, self.Color, points)
        #pygame.gfxdraw.aapolygon(surface, points, self.Color)
        
class PolyLine(Geom):
    def __init__(self, points, close=False):
        Geom.__init__(self)
        self.Points = points
        self.Close = close
        self.LineWidth = 1

    def render1(self, surface, transform):
        points = [transform*p for p in self.Points]
        pygame.draw.lines(surface, self.Color, self.Close, points, width=self.LineWidth)

    def line_width(self, x):
        self.LineWidth = x
        return self

class Line(Geom):
    def __init__(self, start=(0.0, 0.0), end=(0.0, 0.0)):
        Geom.__init__(self)
        self.start = start
        self.end = end
        self.LineWidth = 1

    def render1(self, transforms):
        start = transforms*self.start
        end = transforms*self.end
        pygame.draw.lines(surface, self.Color, start, end, width=self.LineWidth)

class Image(Geom):
    def __init__(self, fname, width, height):
        Geom.__init__(self)
        self.width = width
        self.height = height
        img = pyglet.image.load(fname)
        self.img = img
        self.flip = False
    def render1(self, transforms):
        self.img.blit(-self.width/2, -self.height/2, width=self.width, height=self.height)

def ___draw_text(surface, text, font, size, rotation, x, y, anchor_x, anchor_y):
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

class Text(Geom):
    def __init__(self, text="", anchor_x="right", anchor_y="bottom",
                    size=12, font="Arial", color=(0,0,0,255), bgcolor=(255,255,255,0)):
        Geom.__init__(self)
        self.Text = text
        self.AnchorX = anchor_x
        self.AnchorY = anchor_y
        self.Size = size
        self.Font = pygame.freetype.SysFont('arial', size)
        self.TextRect = self.Font.get_rect(text)
        self.TextRect.center = (0,0)
        self.Color = pygame.Color(color)
        self.BGColor = pygame.Color(bgcolor)

    def render1(self, surface, transform):
        rotated_image, rotated_rect = font.get_rect(text, rotation=transform.Angle * RAD2DEG)
        rotated_rect.center = (0,0)
        anchor_x = {
            "left": straight_rect.left,
            "middle": 0,
            "right": straight_rect.right
        }[self.AnchorX]
        anchor_y = {
            "top": straight_rect.top,
            "middle": 0,
            "bottom": straight_rect.bottom
        }[self.AnchorY]
        anchor_x, anchor_y = Transform.rotation(transform.Angle)*(anchor_x, anchor_y) # rotated anchor relative to the left-top corner of rotated rect
        anchor_x = rotated_rect.width//2 + anchor_x
        anchor_y = rotated_rect.height//2 - anchor_y
        surface.blit(rotated_image, (x - anchor_x, y - anchor_y))

class Marker(Geom):
    def __init__(self, geom, rotation="inherit"):
        Geom.__init__(self)
        self.Rotation = rotation
        self.Geom = geom
        
    def render1(self, transforms):
        # build transform from all stacked transforms, ignoring scale
        #print("Marker.render: calculating transforms...")
        #x, y, a = self.transform.apply(0.0, 0.0, 0.0)
        x, y, a = 0.0, 0.0, 0.0
        for t in reversed(transforms):
            #print("Marker.render: t:", t)
            x1, y1, a1 = t(x, y, a)
            #print("                 ", x, y, a, "->", x1, y1, a1)
            x, y, a = x1, y1, a1
        
        if self.Rotation != "inherit":  a = self.Rotation
        
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(x, y, 0) # translate to GL loc point
        glRotatef(RAD2DEG * a, 0, 0, 1.0)

        self.Geom.render(enable_transforms=False)
        
        glPopMatrix()

def Circle(radius=10, res=30, filled=True):
    points = []
    for i in range(res):
        ang = 2*math.pi*i / res
        points.append((math.cos(ang)*radius, math.sin(ang)*radius))
    if filled:
        return FilledPolygon(points)
    else:
        return PolyLine(points, True)
        
def Polygon(v, filled=True):
    if filled: return FilledPolygon(v)
    else: return PolyLine(v, True)

def Rectangle(left, right, top, bottom, filled=True):
    return Polygon([
        (left, bottom), (right, bottom), (right, top), (left, top)
    ], filled=filled)
    

    