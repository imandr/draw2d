from draw2d import Viewer, Rectangle, Frame, Circle, Line, FilledPolygon, Text
import draw2d

import math, time

viewer = Viewer(800,800, clear_color=(1.,1.,1.,1.))

frame = viewer.frame(-1.4, 1.4, -1.4, 1.4)

for i in range(12):
    a = math.pi/2 - i*2*math.pi/12.0
    if i % 3 == 0:
        m = Rectangle(-0.015, 0.015, -0.05, 0.06).color(0,0,0)
    else:
        m = Rectangle(-0.005, 0.005, -0.05, 0.05).color(0.3, 0.3, 0.3)
    f = Frame()
    f.add(m, at=(0.0, 1.0))
    f.rotate_by(a)
    frame.add(f)
    
    r = 1.2
    digits = str(i if i > 0 else 12)
    digits_frame = Frame().rotate_to(a)
    digits_text = Text(digits, anchor_x = "middle", anchor_y="middle", size=36, margin=5, color=(0.1, 0.1, 0.1)).rotate_to(-a)
    digits_frame.add(digits_text, at=(r, 0))
    frame.add(digits_frame)

hour_hand = Frame()
hour_hand.add(FilledPolygon([(-0.02, -0.03), (0.0, 0.5), (0.02, -0.03)], color=(0,0,0)))
hour_digital = Text(anchor_x = "middle", anchor_y="bottom", size=24, margin=5, color=(0.3, 0.3, 0.3)).rotate_to(90, "deg")
hour_hand.add(hour_digital, at=(0.0, 0.40))
frame.add(hour_hand)

minute_hand = Frame()
minute_hand.add(FilledPolygon([(-0.01, -0.03), (0.0, 0.75), (0.01, -0.03)], color=(0,0,0)))
minute_digital = Text(anchor_x = "middle", anchor_y="bottom", size=24, margin=5, color=(0.3, 0.3, 0.3)).rotate_to(90, "deg")
minute_hand.add(minute_digital, at=(-0.0, 0.70))
frame.add(minute_hand)

second_hand = Frame()
second_hand.add(Line((0.0, 0.8), (0.0, 0.9), color=(1.0,0,0), width = 2))
second_digital = Text(anchor_x = "middle", anchor_y="bottom", size=24, margin=5, color=(0.3, 0.3, 0.3)).rotate_to(90, "deg")
second_hand.add(second_digital, at=(-0.0, 0.85))
frame.add(second_hand)
    
while True:
    t = time.localtime()
    s = t.tm_sec
    m = t.tm_min
    h = t.tm_hour % 12
    if t.tm_hour == 12: h = 12
    
    ampm = "AM" if t.tm_hour < 12 else "PM"
    
    h_angle = -(float(h) + m/60.0 + s/3600.0)/12.0 * 2*math.pi
    hour_hand.rotate_to(h_angle)
    #h_position = (6 - abs(h - 6) + 6)/12.0 * 0.45
    hour_digital.text("%02d %s" % (h, ampm))
    hour_digital.rotate_to(90 if h < 6 or h == 12 else -90, "deg")

    m_angle = -(m/60.0 + s/3600) * 2*math.pi
    minute_hand.rotate_to(m_angle)
    minute_digital.text("%02d" % (m,))
    #m_position = (30 - abs(m - 30) + 30)/60.0 * 0.7
    minute_digital.rotate_to(90 if m < 30 else -90, "deg")

    s_angle = -s/60.0 * 2*math.pi
    second_hand.rotate_to(s_angle)
    second_digital.text("%02d" % (s,))
    #s_position = (30 - abs(s - 30) + 30)/60.0 * 0.9
    second_digital.rotate_to(90 if s < 30 else -90, "deg")

    viewer.locate()

    bitmap = viewer.render()
    time.sleep(1)
    