import math
from .attrs import Color, LineWidth
from .transform import Transform

try:
    import pyglet
except ImportError as e:
    raise ImportError('''
    Cannot import pyglet.
    HINT: you can install pyglet directly via 'pip install pyglet'.
    But if you really just want to install all Gym dependencies and not have to think about it,
    'pip install -e .[all]' or 'pip install gym[all]' will do it.
    ''')

try:
    from pyglet.gl import *
except ImportError as e:
    raise ImportError('''
    Error occurred while running `from pyglet.gl import *`
    HINT: make sure you have OpenGL install. On Ubuntu, you can run 'apt-get install python-opengl'.
    If you're running on a server, you may need a virtual frame buffer; something like this should work:
    'xvfb-run -s \"-screen 0 1400x900x24\" python <your_script.py>'
    ''')

class Geom(object):
    def __init__(self, transform=None, hidden=False):
        self._color=Color((0, 0, 0, 1.0))
        self.attrs = [self._color]
        self.transform = transform
        self.hidden = hidden
        
    def hide(self):
        self.hidden = True
        return self
    
    def show(self):
        self.hidden = False
        return self
    
    def render(self):
        if not self.hidden:
            for attr in reversed(self.attrs):
                attr.enable()
            if self.transform is not None:
                with self.transform:
                    self.render1()
            else:
                self.render1()
            for attr in self.attrs:
                attr.disable()
    def render1(self):
        raise NotImplementedError
    def add_attr(self, attr):
        self.attrs.append(attr)
        return self
    def set_color(self, r, g, b):
        self._color.vec4 = (r, g, b, 1)
        return self
    color = set_color
        
    def transform(self, **args):
        self.transform = Transform(**args)
        return self
        
    def move_to(self, *params):
        if self.transform is None:  self.transform = Transform()
        self.transform.move_to(*params)
        return self

    def move_by(self, *params):
        if self.transform is None:  self.transform = Transform()
        self.transform.move_by(*params)
        return self

    def rotate_by(self, *params):
        if self.transform is None:  self.transform = Transform()
        self.transform.rotate_by(*params)
        return self

    def rotate_to(self, *params):
        if self.transform is None:  self.transform = Transform()
        self.transform.rotate_to(*params)
        return self
        
    def scale_to(self, *params):
        if self.transform is None:  self.transform = Transform()
        self.transform.scale_to(*params)
        return self

    def scale_by(self, *params):
        if self.transform is None:  self.transform = Transform()
        self.transform.scale_by(*params)
        return self

class Point(Geom):
    def __init__(self):
        Geom.__init__(self)
    def render1(self):
        glBegin(GL_POINTS) # draw point
        glVertex3f(0.0, 0.0, 0.0)
        glEnd()

class FilledPolygon(Geom):
    def __init__(self, v):
        Geom.__init__(self)
        self.v = v
    def render1(self):
        if   len(self.v) == 4 : glBegin(GL_QUADS)
        elif len(self.v)  > 4 : glBegin(GL_POLYGON)
        else: glBegin(GL_TRIANGLES)
        for p in self.v:
            glVertex3f(p[0], p[1],0)  # draw each vertex
        glEnd()

class PolyLine(Geom):
    def __init__(self, v, close):
        Geom.__init__(self)
        self.v = v
        self.close = close
        self.linewidth = LineWidth(1)
        self.add_attr(self.linewidth)
    def render1(self):
        glBegin(GL_LINE_LOOP if self.close else GL_LINE_STRIP)
        for p in self.v:
            glVertex3f(p[0], p[1],0)  # draw each vertex
        glEnd()
    def set_linewidth(self, x):
        self.linewidth.stroke = x

class Line(Geom):
    def __init__(self, start=(0.0, 0.0), end=(0.0, 0.0)):
        Geom.__init__(self)
        self.start = start
        self.end = end
        self.linewidth = LineWidth(1)
        self.add_attr(self.linewidth)

    def render1(self):
        glBegin(GL_LINES)
        glVertex2f(*self.start)
        glVertex2f(*self.end)
        glEnd()

class Image(Geom):
    def __init__(self, fname, width, height):
        Geom.__init__(self)
        self.width = width
        self.height = height
        img = pyglet.image.load(fname)
        self.img = img
        self.flip = False
    def render1(self):
        self.img.blit(-self.width/2, -self.height/2, width=self.width, height=self.height)

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
    