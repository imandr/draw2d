import time, math
from draw2d import Viewer, Marker, Circle, Text, Frame, Polygon, Rectangle

v = Viewer(600,600)
f = v.frame(-200, 200, -200, 200)

circle = Marker(Circle(10, filled=False).color(1.,1.,0.5))
triangle = Marker(Polygon([(-5, -5), (0, 5), (5, -5)]).color(1.0, 0.2, 0.0))
block = Marker(Rectangle(-5, 5, -2, 2).color(0.1, 1.0, 0.1))

frame = Frame()
frame.add(circle, at=(100, 0))
frame.add(triangle, at=(-50, 60))
frame.add(block, at=(-50, -67))

f.add(frame)

turn = 1
t = 0
while True:
    scale = 0.1 + math.sin(t/10*0.2)
    frame.rotate_by(turn, "deg").scale_to(scale)
    v.render()
    time.sleep(0.1)
    t += 1
