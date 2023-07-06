from draw2d import Viewer, Circle
import time

v = Viewer(500, 500)
f = v.frame(-1, 1, -1, 1)
f.add(Circle(0.2, filled=False, width=3).color(1.0, 1.0, 1.0))

for _ in range(10):
    v.render()
    time.sleep(1)
