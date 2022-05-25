from draw2d import Viewer, Rectangle, Frame, Circle, Line, Point

import math, time

try:
    import pyglet
except ImportError as e:
    raise ImportError('''
    Cannot import pyglet.
    HINT: you can install pyglet directly via 'pip install pyglet'.
    But if you really just want to install all Gym dependencies and not have to think about it,
    'pip install -e .[all]' or 'pip install gym[all]' will do it.
    ''')

if True:
    try:
        from pyglet.gl import *
    except ImportError as e:
        raise ImportError('''
        Error occurred while running `from pyglet.gl import *`
        HINT: make sure you have OpenGL install. On Ubuntu, you can run 'apt-get install python-opengl'.
        If you're running on a server, you may need a virtual frame buffer; something like this should work:
        'xvfb-run -s \"-screen 0 1400x900x24\" python <your_script.py>'
        ''')





viewer = Viewer(800,800)

#frame = viewer.frame(-1.1, 1.1, -1.1, 1.1)

#r = Rectangle(100, 200, 300, 400).color(1,1,1)
#viewer.add_geom(r)
p = Point().color(1,1,1).move_to(30,30)
viewer.add_geom(p)

    
while True:
    #viewer.render()
    
    viewer.window.switch_to()
    viewer.window.dispatch_events()
    viewer.window.clear()
    glClearColor(*viewer.clear_color)
    
    glColor4f(1,1,1,1)
    glBegin(GL_POINTS) # draw point
    glVertex3f(30.0, 20.0, 0.0)
    glEnd()
    
    viewer.window.flip()
    
    
    time.sleep(1)
    