from draw2d import Viewer, Rectangle, Frame, Circle, Line, FilledPolygon, Text
import draw2d

import math, time

viewer = Viewer(800,800, clear_color=(1.,1.,1.,1.))

frame = viewer.frame(-1.1, 1.1, -1.1, 1.1)

for i in range(12):
    a = math.pi/2 - i*2*math.pi/12.0
    if i % 3 == 0:
        m = Rectangle(-0.015, 0.015, -0.1, 0.05).color(0,0,0)
    else:
        m = Rectangle(-0.005, 0.005, -0.05, 0.05).color(0.3, 0.3, 0.3)
    f = Frame()
    f.add(m, at=(0.0, 1.0))
    f.rotate_by(a)
    frame.add(f)

hour_hand = Frame()
hour_hand.add(FilledPolygon([(-0.02, -0.02), (0.0, 0.5), (0.02, -0.02)]).color(0,0,0))
hour_digital = Text(anchor_x = "middle", anchor_y="bottom", size=36, margin=5, color=(0.3, 0.3, 0.3)).rotate_to(90, "deg")
hour_hand.add(hour_digital, at=(-0.0, 0.45))
frame.add(hour_hand)


minute_hand = Frame()
minute_hand.add(FilledPolygon([(-0.01, -0.02), (0.0, 0.75), (0.01, -0.02)]).color(0,0,0))
minute_digital = Text(anchor_x = "middle", anchor_y="bottom", size=36, margin=5, color=(0.3, 0.3, 0.3)).rotate_to(90, "deg").color(0.3, 0.3, 0.3)
minute_hand.add(minute_digital, at=(-0.0, 0.70))
frame.add(minute_hand)


second_hand = Frame()
second_hand.add(Line((0.0, -0.1), (0.0, 0.95)).color(0,0,0))
second_digital = Text(anchor_x = "middle", anchor_y="bottom", size=36, margin=5, color=(0.3, 0.3, 0.3)).rotate_to(90, "deg").color(0.3, 0.3, 0.3)
second_hand.add(second_digital, at=(-0.0, 0.9))
frame.add(second_hand)
    
while True:
    t = time.localtime()
    s = t.tm_sec
    m = t.tm_min
    h = t.tm_hour % 12
    
    ampm = "AM" if t.tm_hour < 12 else "PM"
    
    hour_digital.text("%02d %s" % (h, ampm))
    minute_digital.text("%02d" % (m,))
    second_digital.text("%02d" % (s,))

    hour_digital.rotate_to(90 if h < 6 else -90, "deg")
    second_digital.rotate_to(90 if s < 30 else -90, "deg")
    minute_digital.rotate_to(90 if m < 30 else -90, "deg")
        

    h_angle = -(float(h) + m/60.0 + s/3600.0)/12.0 * 2*math.pi
    m_angle = -(m/60.0 + s/3600) * 2*math.pi
    s_angle = -s/60.0 * 2*math.pi
    hour_hand.rotate_to(h_angle)
    minute_hand.rotate_to(m_angle)
    second_hand.rotate_to(s_angle)
    viewer.render()
    time.sleep(1)
    