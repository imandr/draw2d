from draw2d import Viewer, Rectangle, Frame, Circle, Line

import math, time

viewer = Viewer(800,800)

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
    #print(i, f)
    frame.add(f)

hour_hand = Rectangle(-0.02, 0.02, -0.02, 0.5).color(0,0,0)
frame.add(hour_hand)
minute_hand = Rectangle(-0.01, 0.01, -0.02, 0.75).color(0,0,0)
frame.add(minute_hand)
second_hand = Rectangle(-0.003, 0.003, -0.1, 0.95).color(0,0,0)
frame.add(second_hand)

    
while True:
    t = time.localtime()
    s = t.tm_sec
    m = t.tm_min
    h = t.tm_hour % 12

    h_angle = -(float(h) + m/60.0 + s/3600.0)/12.0 * 2*math.pi
    m_angle = -(m/60.0 + s/3600) * 2*math.pi
    s_angle = -s/60.0 * 2*math.pi
    hour_hand.rotate_to(h_angle)
    minute_hand.rotate_to(m_angle)
    second_hand.rotate_to(s_angle)
    viewer.render()
    time.sleep(1)
    