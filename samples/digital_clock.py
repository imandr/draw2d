from draw2d import Viewer, Rectangle, Frame, Circle, Line, Text

import math, time

viewer = Viewer(800,800, clear_color=(1,1,1,1))

frame = viewer.frame(-1.1, 1.1, -1.1, 1.1)

for i in range(12):
    a = math.pi/2 - i*2*math.pi/12.0
    if i % 3 == 0:
        m = Rectangle(-0.015, 0.015, -0.1, 0.05).color(0,0,0)
    else:
        m = Rectangle(-0.01, 0.01, -0.05, 0.05).color(0,0,0)
    f = Frame()
    f.add(m, at=(0.0,1.0))
    f.rotate_by(a)
    frame.add(f)

second_hand = Frame()
text = Text("00:00:00", 0.5, 0.0, anchor_x="center", anchor_y="center").color(1,1,1)
second_hand.add(text)
frame.add(second_hand)

    
while True:
    t = time.localtime()
    s = t.tm_sec
    m = t.tm_min
    h = t.tm_hour % 12

    s_angle = -s/60.0 * 2*math.pi
    second_hand.rotate_to(s_angle)
    viewer.render()
    time.sleep(1)
    