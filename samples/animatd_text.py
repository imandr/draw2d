from draw2d import Viewer, Text, Line, Rectangle, Frame, Point, Circle

import math, time, random


viewer = Viewer(600,600)
W = 1.0
F = viewer.frame(0., W, 0., W)

F.add(Text("North", anchor_x="center", anchor_y="top", color=(0.2,0.2,1.0)).move_to(0.5,0.9))
F.add(Text("South", anchor_x="center", anchor_y="bottom", color=(1.0,1.0,0.1)).move_to(0.5,0.1))
F.add(Text("East", anchor_x="right", anchor_y="center", color=(0.2,1.0,1.0)).move_to(0.9,0.5))
F.add(Text("West", anchor_x="left", anchor_y="center", color=(1.0,0.2,0.1)).move_to(0.1,0.5))

fly = Frame()
fly.add(Circle(radius=0.01).color(1,1,1))
label = Text("").move_to(0.01, 0.01)
vlabel = Text("", anchor_x="left", anchor_y="center").move_to(0.02, 0.0)
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
        
    x = max(0.0, min(W, x))
    y = max(0.0, min(W, y))
    
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


