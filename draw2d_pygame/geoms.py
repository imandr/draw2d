import math, os
from .transformation import IsoTransform, Transform
from .attrs import Color
import pygame
import pygame.gfxdraw
import pygame.freetype

RAD2DEG = 180.0/math.pi
DEG2RAD = math.pi/180.0

class Geom(object):
    def __init__(self, hidden=False, transient=False, transform=None):
        self.Color = Color(0,0,0,1.0)
        self.Hidden = hidden
        self.Transient = transient
        self.Transform = transform or IsoTransform()
        
    def move_to(self, *args):
        self.Transform.move_to(*args)
        return self

    def move_by(self, *args):
        self.Transform.move_by(*args)
        #print("Geom.move_by: transform:", self.Transform)
        return self

    def rotate_to(self, *args):
        self.Transform.rotate_to(*args)
        return self

    def rotate_by(self, *args):
        self.Transform.rotate_by(*args)
        return self

    def scale_to(self, *args):
        self.Transform.scale_to(*args)
        return self

    def scale_by(self, *args):
        self.Transform.scale_by(*args)
        return self

    def hide(self):
        self.Hidden = True
        return self
    
    def show(self):
        self.Hidden = False
        return self

    def render(self, surface, context):
        if not self.Hidden:
            #for attr in reversed(self.attrs):
            #    #print("Geom.render: attr:", attr)
            #    attr.enable()
            self.render1(surface, context*self.Transform)
            #for attr in self.attrs:
            #    attr.disable()
                
    def render1(self, transforms):
        raise NotImplementedError

    def add_attr(self, attr):
        self.attrs.append(attr)
        return self
        
    def set_color(self, *tup):
        self.Color = Color(*tup)
        return self

    color = set_color

    def line_width(self, w):
        return self.add_attr(LineWidth(w))

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
        pygame.gfxdraw.aapolygon(surface, points, self.Color)
        
class PolyLine(Geom):
    def __init__(self, points, close=False):
        Geom.__init__(self)
        self.Points = points
        self.Close = close
        self.LineWidth = 1

    def render1(self, surface, transform):
        #print("PolyLine.render1: transform:", transform)
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

    def render1(self, surface, transforms):
        start = transforms*self.start
        end = transforms*self.end
        pygame.draw.line(surface, self.Color, start, end, width=self.LineWidth)

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

class Text(Geom):
    def __init__(self, text="", anchor_x="right", anchor_y="bottom",
                    margin = 0,
                    size=12, font="Arial", color=(0,0,0,255), bgcolor=None):
        Geom.__init__(self)
        self.Text = text
        self.AnchorX = anchor_x
        self.AnchorY = anchor_y
        self.Size = size
        self.Font = pygame.freetype.SysFont('arial', size)
        self.Color = Color(color)
        self.BGColor = Color(bgcolor)
        self.Margin = margin
        self.text(text)
        
    def text(self, text):
        self.Text = text
        self.TextRect = self.Font.get_rect(text)
        self.TextRect.inflate_ip(self.Margin*2, self.Margin*2)
        self.TextRect.center = (0,0)

    def render1(self, surface, transform):
        #print("Text.rebder1: self.Transform:", self.Transform, "    combined angle:", transform.Angle)
        x, y = transform.translation
        rotated_image, rotated_rect = self.Font.render(self.Text, 
            fgcolor = self.Color, bgcolor=self.BGColor,
            rotation=round(transform.Angle * RAD2DEG)
        )
        rotated_rect.center = (0,0)
        #print("Text.render1: text:", self.Text, "  rotated_rect:", rotated_rect)
        anchor_x = {
            "left": self.TextRect.left,
            "middle": 0,
            "center": 0,
            "right": self.TextRect.right
        }[self.AnchorX]
        anchor_y = {
            "top": self.TextRect.top,
            "middle": 0,
            "center": 0,
            "bottom": self.TextRect.bottom
        }[self.AnchorY]
        anchor_x, anchor_y = Transform.rotation(-transform.Angle)*(anchor_x, anchor_y) 
        anchor_x = rotated_rect.width//2 + anchor_x
        anchor_y = rotated_rect.height//2 + anchor_y
        # rotated anchor relative to the left-top corner of rotated rect
        surface.blit(rotated_image, (x - anchor_x, y - anchor_y))

class Marker(Geom):
    def __init__(self, geom, rotation="inherit"):
        Geom.__init__(self)
        self.Rotation = rotation
        self.Geom = geom

    def render(self, surface, context):
        if not self.Hidden:
            t = context * self.Transform
            tx, ty = t.translation
            angle = t.Angle
            self.Geom.render1(surface, Transform(angle=anlge, translation=(tx, ty)))

def ___Circle(radius=10, res=30, filled=True):
    points = []
    for i in range(res):
        ang = 2*math.pi*i / res
        points.append((math.cos(ang)*radius, math.sin(ang)*radius))
    if filled:
        return FilledPolygon(points)
    else:
        return PolyLine(points, True)
        
class Circle(Geom):
    def __init__(self, radius, filled=True, **compat):
        Geom.__init__(self)
        self.Radius = radius
        self.Filled = filled
        
    def render1(self, surface, transform):
        c = transform * (0., 0.)
        p = transform * (self.Radius, 0.)
        r = math.sqrt((p[0]-c[0])**2 + (p[1]-c[1])**2)
        if self.Filled:
            pygame.gfxdraw.filled_circle(surface, round(c[0]), round(c[1]), round(r), self.Color)
        pygame.gfxdraw.aacircle(surface, round(c[0]), round(c[1]), round(r), self.Color)
            
        
def Polygon(v, filled=True):
    if filled: return FilledPolygon(v)
    else: return PolyLine(v, True)

def Rectangle(left, right, top, bottom, filled=True):
    return Polygon([
        (left, bottom), (right, bottom), (right, top), (left, top)
    ], filled=filled)
    

    