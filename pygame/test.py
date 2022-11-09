from draw2d import Viewer, Point
import time

v = Viewer(500, 500)
f = v.frame(0, 500, 0, 500)
f.add(Point().color(255,200,200).move_to(300,350))
v.render()

time.sleep(10)