from draw2d import Viewer, Point, PolyLine
import time

v = Viewer(500, 500)
f = v.frame(0, 500, 0, 500)
f.add(Point().color(255,100,100).move_to(300,350))
poly = PolyLine([(-15,-15), (-15,15), (15,15), (15,-15)]).move_to(10,10).color(100, 200, 100)
f.add(poly)

for _ in range(10):
    poly.move_by(10,10).rotate_by(10, "deg")
    v.render()
    time.sleep(1)
