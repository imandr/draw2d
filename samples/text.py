from draw2d import Viewer, Text
import time

v = Viewer(500, 500, clear_color=(1., 1., 1.))
f = v.frame()
f.add(Text("Hello").move_to(200, 200))
v.render()
while True:
    time.sleep(1)