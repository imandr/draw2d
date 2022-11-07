from draw2d import Viewer, Rectangle, Circle
import time, random, math

v = Viewer(600, 600)

f = v.frame(-0.1, 1.1, -0.1, 1.1)
r = Rectangle(-0.07, 0.07, -0.09, 0.09).color(0.2, 1.0, 0.3, 0.5)
c = Circle(0.06).color(1.0, 0.3, 0.2, 0.5)

rx = random.random()
ry = random.random()
ra = random.random()*math.pi
rw = random.random()*math.pi/100
rvx = (random.random()*2-1)*0.003
rvy = (random.random()*2-1)*0.003

cx = random.random()
cy = random.random()
cvx = (random.random()*2-1)*0.003
cvy = (random.random()*2-1)*0.003

r.rotate_by(ra)

f.add(r, at=(rx, ry))
f.add(c, at=(cx, cy))

while True:

    # bounce from walls
    if rx <= 0 or rx >= 1:
        rvx = -rvx
        rw = (random.random()-0.2)*math.pi/100
    if ry <= 0 or ry >= 1:
        rvy = -rvy
        rw = (random.random()-0.8)*math.pi/100
    if cy <= 0 or cy >= 1:
        cvy = -cvy
    if cx <= 0 or cx >= 1:
        cvx = -cvx

    # collide
    if abs(rx-cx) < 0.1 and abs(ry-cy) < 0.1:
        cvx, cvy, rvx, rvy = rvx, rvy, cvx, cvy
        rw = (random.random()-0.5)*math.pi/100
        
        
    
    rx += rvx
    ry += rvy
    ra += rw
    cx += cvx
    cy += cvy
    
    r.move_to(rx, ry).rotate_to(ra)
    c.move_to(cx, cy)
    
    v.render()
    time.sleep(0.01)
