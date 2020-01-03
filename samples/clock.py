from draw2d import Viewer, Rectangle, Frame, Circle

import math, time

print (math)

viewer = Viewer(800,800)
print (math)

frame = viewer.frame(-1.1, 1.1, -1.1, 1.1)

for i in range(12):
    a = i*2*math.pi/12.0
    m = Rectangle(-0.01,0.01, -0.05, 0.05).color(0,0,0)
    f = Frame()
    f.move_to(0.0, 1.0).rotate_by(a)
    print(i, f)
    f.add(m)
    frame.add(f)

viewer.render()

while True:
    time.sleep(1)
    