from draw2d import Viewer, Circle, Polygon, Rectangle, Text, Marker
import time

viewer = Viewer(800, 800)
frame = viewer.frame(-1.0, 1.0, -1.0, 1.0)

circle = Circle(0.2).color(1,1,1)
square = Rectangle(0, 0.1, 0, 0.1).color(0,1,0)
text = Text("Hello world", color=(0.5,0.5,1.0), anchor_x="center", anchor_y="center")
marker = Marker(Polygon([(-5,0), (5,0), (0,10)]).color(1,0.5,0.5))

frame.add(circle, at=(0,0))
frame.add(square, at=(0.4,0.1))
frame.add(text, at=(-0.5,-0.3))
frame.add(marker, at=(-0.5, 0.3))

viewer.render()

while True:
    time.sleep(1.0)