from draw2d import Viewer, Text, Line, Rectangle, Frame, Point, Circle

import math, time, random

viewer = Viewer(600,600)
W = 1.0
f = viewer.frame(0., W, 0., W)
text_frame = Frame()
f.add(text_frame)

x, y = W/2, W/2
a = 0.0

while True:
    x = min(W, max(0.0, x + random.random()*0.1 - 0.05))
    y = min(W, max(0.0, y + random.random()*0.1 - 0.05))
    a = a + (random.random()*2-1)*math.pi/30.0

    text_frame.add(Text("[%.3f:%.3f]" % (x,y), 0.0, 0.0, anchor_x = "center", anchor_y="center").color(1,1,1))
    text_frame.move_to(x,y)
    text_frame.rotate_to(a)
    viewer.render()
    text_frame.remove_all()
    
    time.sleep(1.0)


