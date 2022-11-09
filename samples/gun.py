from draw2d import Viewer, Rectangle, Frame, Circle, Line
from pythreader import Gate, PyThread, Primitive, synchronized, RWLock
import math, random, time



class Field(Primitive):
    
    G = 2.0
    V = 20.0
    U = 2.0
    DT = 0.05
    F = 0.01
    Center = (0.0, 0.0)
    DIMS = (-100,100,0,100)

    def __init__(self, viewer):
        Primitive.__init__(self)
        self.Viewer = viewer
        self.Frame = viewer.frame(*self.DIMS)
        self.Lock = RWLock()
    
    @synchronized
    def add(self, geom):
        self.Frame.add(geom)
        
    def render(self):
        with self.Lock.exclusive:
            self.Viewer.render()
        
    def start_speed(self):
        phi = random.random()*math.pi
        v = self.V*(1+random.random())/2
        return v*math.cos(phi), v*math.sin(phi)
        
    def update(self):
        return self.Lock.shared
                
class Ball(PyThread):

    SIZE = 0.5

    def __init__(self, gate, field, x=0.0, y=0.0):
        PyThread.__init__(self)
        self.X = x
        self.Y = y
        self.VX = 0.0
        self.VY = 0.0
        self.Gate = gate
        self.Field = field
        self.Rect = Rectangle(0.0, self.SIZE, 0.0, self.SIZE).color(*self.Color)
        self.Field.add(self.Rect)
        
    def update(self):
        with self.Field.update():
            self.Rect.move_to(self.X, self.Y)

    def run(self):
        cx, cy = self.Field.Center
        while True:
            self.Gate.wait()
            self.VX, self.VY = self.Field.start_speed()
            print(self.VX, self.VY)
            dt = self.Field.DT
            self.X += dt * self.VX
            self.Y += dt * self.VY
            self.update()
            while self.VY > 0.0 or self.Y > 0.0:
                time.sleep(dt)
                self.VY -= dt * self.Field.G + self.VY * self.Field.F
                self.VX -=                     self.VX * self.Field.F
                self.X += dt * self.VX
                self.Y += dt * self.VY
                self.update()

            self.landed()

            self.Y = self.VY = 0
            d = self.X - cx
            self.VX = self.Field.U if d < 0 else -self.Field.U
            self.update()
            while d * (self.X-cx) > 0.0:
                time.sleep(dt)
                self.X += dt * self.VX
                self.update()
            self.VX = self.VY = 0.0
            self.X, self.Y = cx, cy
            self.update()
            self.at_center()

    def at_center(self):
        pass
        
    def landed(self):
        pass
        
class WhiteBall(Ball):
    
    Color = (0.8,0.8, 0.1)
    
class BlueBall(Ball):
    
    Color = (0.1,1.0,0.1)
    
    def at_center(self):
        self.Gate.pulse()
    
class RedBall(Ball):
    
     Color = (1,0.2,0.2)
    
     def landed(self):
         self.Gate.pulse()
    
    
viewer = Viewer(800,400, clear_color=(0,0,0,0))

gate = Gate()
field = Field(viewer)
white_balls = [WhiteBall(gate, field) for _ in range(100)]
blue_balls = [BlueBall(gate, field) for _ in range(5)]
red_balls = [RedBall(gate, field) for _ in range(8)]
balls = red_balls + blue_balls + white_balls

[b.start() for b in balls]

gate.pulse()

while True:
    time.sleep(field.DT/3)
    field.render()
    


