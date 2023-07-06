import math
from .transformation import IsoTransform, Transform
from .attrs import Color
import pygame
import pygame.gfxdraw
import pygame.freetype

RAD2DEG = 180.0/math.pi
DEG2RAD = math.pi/180.0

class Geom(object):
    def __init__(self, hidden=False, transient=False, transform=None, 
            color=(0,0,0,1.0), bgcolor=(0,0,0,0.0), width=1):
        self.Color = Color(*color)
        self.BGColor = Color(*bgcolor)
        self.StrokeWidth = width
        self.Hidden = hidden
        self.Transient = transient
        self.Transform = transform or IsoTransform()
        self.X = self.Y = self.Angle = None
    
    @property
    def x(self):
        return self.Transform.Translation[0]
        
    @property
    def y(self):
        return self.Transform.Translation[1]
        
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
        
    def locate(self, context = None):
        t = self.Transform
        if context is not None:
            t = context * t
        self.X, self.Y = t * (0., 0.)
        self.Angle = t.Angle
        return self.Angle, (self.X, self.Y)

    def render(self, surface, context = None):
        if not self.Hidden:
            #for attr in reversed(self.attrs):
            #    #print("Geom.render: attr:", attr)
            #    attr.enable()
            t = self.Transform
            if context is not None:
                t = context * t
            self.render1(surface, t)
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
        self.StrokeWidth = w
        return self
        
    width = line_width

class Point(Geom):
    def __init__(self, **params):
        Geom.__init__(self, **params)
        
    def render1(self, surface, transform):
        x, y = transform * (0, 0)
        x = round(x)
        y = round(y)
        pygame.gfxdraw.pixel(surface, x, y, self.Color)
        
class FilledPolygon(Geom):
    def __init__(self, points, **params):
        Geom.__init__(self, **params)
        self.Points = points
        
    def render1(self, surface, transform):
        points = [transform*p for p in self.Points]
        #print("FilledPolygon: points:", points)
        pygame.draw.polygon(surface, self.Color, points)
        pygame.gfxdraw.aapolygon(surface, points, self.Color)
        
class PolyLine(Geom):
    def __init__(self, points, close=False, **params):
        Geom.__init__(self, **params)
        self.Points = points
        self.Close = close

    def render1(self, surface, transform):
        #print("PolyLine.render1: transform:", transform)
        points = [transform*p for p in self.Points]
        pygame.draw.lines(surface, self.Color, self.Close, points, width=self.StrokeWidth)

class Line(Geom):
    def __init__(self, start=(0.0, 0.0), end=(0.0, 0.0), **params):
        Geom.__init__(self, **params)
        self.start = start
        self.end = end

    def render1(self, surface, transforms):
        start = transforms*self.start
        end = transforms*self.end
        pygame.draw.line(surface, self.Color, start, end, width=self.StrokeWidth)

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
        self._Text = text
        self.AnchorX = anchor_x
        self.AnchorY = anchor_y
        self.Size = size
        self.Font = pygame.freetype.SysFont('arial', size)
        self.Color = Color(color)
        self.BGColor = Color(bgcolor)
        self.Margin = margin
        self.LastAngle = self.RenderedImage = self.RenderedRect = None

    def text(self, text):
        if self._Text != text:
            self._Text = text
            self.RenderedImage = None
        return self

    @property
    def Text(self):
        return self._Text
        
    @Text.setter
    def Text(self, text):
        self.text(text)

    def update(self, angle):
        self.TextRect = self.Font.get_rect(self._Text)
        self.TextRect.inflate_ip(self.Margin*2, self.Margin*2)
        self.TextRect.center = (0,0)
        self.RenderedImage, self.RenderedRect = self.Font.render(self._Text, 
            fgcolor = self.Color, bgcolor=self.BGColor,
            rotation=angle
        )
        self.RenderedRect.center = (0,0)
        self.LastAngle = angle
        return self.RenderedImage, self.RenderedRect

    def render1(self, surface, transform):
        #print("Text.rebder1: self.Transform:", self.Transform, "    combined angle:", transform.Angle)
        x, y = transform.translation
        angle = round(transform.Angle * RAD2DEG)
        if angle != self.LastAngle or self.RenderedImage is None or self.RenderedRect is None:
            self.update(angle)
        rotated_image = self.RenderedImage
        rotated_rect = self.RenderedRect
        #print("Text.render1: text:", self._Text, "  rotated_rect:", rotated_rect)
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
            angle = self.Transform.Angle
            self.Geom.render1(surface, IsoTransform(angle=angle, translate=(tx, ty)))

class Circle(Geom):
    def __init__(self, radius, filled=True, **params):
        Geom.__init__(self, **params)
        self.Radius = radius
        self.Filled = filled
        
    def render1(self, surface, transform):
        c = transform * (0., 0.)
        p = transform * (self.Radius, 0.)
        r = math.sqrt((p[0]-c[0])**2 + (p[1]-c[1])**2)
        c0 = int(round(c[0]))
        c1 = int(round(c[1]))
        r = int(round(r))
        if self.Filled:
            #print("Circle.render1:", surface, c0, c1, r, self.Color)
            pygame.gfxdraw.filled_circle(surface, c0, c1, r, self.Color)
        pygame.gfxdraw.aacircle(surface, c0, c1, r, self.Color)

    def render1(self, surface, transform):
        c = transform * (0., 0.)
        p = transform * (self.Radius, 0.)
        r = math.sqrt((p[0]-c[0])**2 + (p[1]-c[1])**2)
        c0 = int(round(c[0]))
        c1 = int(round(c[1]))
        r = int(round(r))
        pygame.gfxdraw.aacircle(surface, c0, c1, r, self.Color)
        if self.Filled:
            #print("Circle.render1:", surface, c0, c1, r, self.Color)
            pygame.gfxdraw.filled_circle(surface, c0, c1, r, self.Color)
        else:
            pygame.draw.circle(surface, self.Color, (c0, c1), r, width=self.StrokeWidth)
            
        
def Polygon(v, filled=True, **params):
    if filled: return FilledPolygon(v, **params)
    else: return PolyLine(v, True, **params)

def Rectangle(left, right, top, bottom, filled=True, **params):
    return Polygon([
        (left, bottom), (right, bottom), (right, top), (left, top)
    ], filled=filled, **params)
    

    