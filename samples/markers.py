import time
from draw2d import Viewer, Marker, Circle, Text

v = Viewer(600,600)
f = v.frame(-200, 200, -200, 200)
m1 = Marker(Circle(3, filled=False).color(1,1,0.5))
#f.add(m1, at=(0,0))
m1 = Marker(Circle(4).color(0.2,1,0.5))
m2 = Marker(Circle(4).color(0.2,1,0.5))
m3 = Marker(Circle(4).color(0.2,1,0.5))
f.add(m1, at=(1,3))
f.add(m2, at=(101,103))
f.add(m3, at=(197,198))

t = Text("hello")
#f.add(t, at=(-50,50))
v.render()
time.sleep(100)