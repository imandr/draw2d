from draw2d import Viewer, Text, Line, Rectangle, Frame, Point, Circle

import math, time, random


viewer = Viewer(600,600,clear_color=(1., 1., 1., 1.))
W = 1.0
F = viewer.frame(-W, W, -W, W)

F.add(Frame().move_to(0.0,0.8) \
        .add(Text("North", anchor_x="center", anchor_y="bottom", margin=5, color=(0.2,0.2,1.0))) \
        .add(Circle(0.002).color(1.0,0,0,1.0))
    ) \
.add(Frame().move_to(0.0,-0.8) \
        .add(Text("South", anchor_x="center", anchor_y="top", margin=5, color=(1.0,1.0,0.1))) \
        .add(Circle(0.002).color(1.0,0,0,1.0))
    ) \
.add(Frame().move_to(0.8,0.0) \
        .add(Text("East", anchor_x="left", anchor_y="center", margin=5, color=(0.2,1.0,1.0))) \
        .add(Circle(0.002).color(1.0,0,0,1.0))
    ) \
.add(Frame().move_to(-0.8, 0.0) \
        .add(Text("West", anchor_x="right", anchor_y="center", margin=5, color=(1.0,0.2,0.1)))
        .add(Circle(0.002).color(1.0,0,0,1.0))
    ) \

F.add(
    Frame().move_to(0.1, 0.2) \
        .add(Text(". . . . .", anchor_x="middle", anchor_y="bottom", margin=15).rotate_to(90, "deg")) \
        .add(Circle(0.002))
)
F.add(
    Frame().move_to(0.1, 0.1) \
        .add(Text(". . . . .", anchor_x="middle", anchor_y="bottom", margin=15).rotate_to(45, "deg")) \
        .add(Circle(0.002))
)
F.add(
    Frame().move_to(0.1, 0.0) \
        .add(Text(". . . . .", anchor_x="middle", anchor_y="bottom", margin=15).rotate_to(0, "deg")) \
        .add(Circle(0.002))
)
F.add(
    Frame().move_to(0.1, -0.1) \
        .add(Text(". . . . .", anchor_x="middle", anchor_y="bottom", margin=15).rotate_to(-25, "deg")) \
        .add(Circle(0.002))
)



fly = Frame()
fly.add(Circle(radius=0.01).color(0.2, 1.0, 0.1))
label = Text("", anchor_x="center", anchor_y="bottom", margin=5).move_to(0.0, 0.0)
vlabel = Text("", anchor_x="center", anchor_y="top", margin=5).move_to(0.0, 0.0)
fly.add(label)
fly.add(vlabel)
F.add(fly, "fly")

x, y = random.random(), random.random()
vx, vy = 0.0, 0.0
vmax = 0.5
r = random.random()
omega = 0.0
max_omega = 0.1
tau = 0.1

while True:
    x += vx * tau
    y += vy * tau
    r += omega * tau
    
    if x < 0.0 or x > W: vx = -vx*0.8
    if y < 0.0 or y > W: vy = -vy*0.8
        
    x = max(-W, min(W, x))
    y = max(-W, min(W, y))
    
    ax, ay = (2*random.random()-1)*vmax/10, (2*random.random()-1)*vmax/10
    vx += ay * tau
    vy += ay * tau
    
    vx = max(-vmax, min(vmax, vx))
    vy = max(-vmax, min(vmax, vy))
    
    omega += (2*random.random()-1)*max_omega/10
    omega = max(max_omega, min(-max_omega, omega))
    
    fly.move_to(x, y).rotate_to(r)
    label.Text = "[xy: %.3f:%.3f]" % (x,y)
    vlabel.Text = "[vxy: %.3f:%.3f]" % (vx,vy)
    viewer.render()
    time.sleep(tau)


