import os
import six
import sys, numpy as np

#if "Apple" in sys.version:
#    if 'DYLD_FALLBACK_LIBRARY_PATH' in os.environ:
#        os.environ['DYLD_FALLBACK_LIBRARY_PATH'] += ':/usr/lib'
#        # (JDS 2016/04/15): avoid bug on Anaconda 2.3.0 / Yosemite

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



def get_display(spec):
    """Convert a display specification (such as :0) into an actual Display
    object.

    Pyglet only supports multiple Displays on Linux.
    """
    if spec is None:
        return None
    elif isinstance(spec, six.string_types):
        return pyglet.canvas.Display(spec)
    else:
        raise error.Error('Invalid display specification: {}. (Must be a string like :0 or None.)'.format(spec))


class Screen(object):
    def __init__(self, width, height, display=None, clear_color=(0,0,0,1)):
        display = get_display(display)

        self.width = width
        self.height = height
        self.window = pyglet.window.Window(width=width, height=height, display=display)
        self.window.on_close = self.window_closed_by_user
        self.isopen = True
        self.onetime_geoms = []
        self.clear_color = clear_color

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_PROGRAM_POINT_SIZE)
        glPointSize(20.0)
        
        self.StrokeColor = (1,1,1,1)
        self.FillColor = (0.5, 0.5, 0.5, 1.0)
        self.StrokeWeight = 1.0

    def start_frame(self):
        self.window.switch_to()
        self.window.dispatch_events()
        glClearColor(*self.clear_color)
        self.window.clear()
        
    def fill(self, v1, v2, v3, a=1.0):
        self.FillColor = (v1, v2, v3, a)
    
    def stroke(self, v1, v2, v3, a=1.0):
        self.StrokeColor = (v1, v2, v3, a)
    
    def strokeWeight(self, x):
        self.StrokeWeight = x
        glPointSize(x)
        
    def point(self, x, y=None):
        if isinstance(x, np.ndarray):
            x, y = x
        glColor4f(*self.StrokeColor)
        glBegin(GL_POINTS) # draw point
        glVertex3f(x, y, 0)
        glEnd()

    def line(self, a0, a1, x1=None, y1=None):
        if isinstance(a0, np.ndarray):
            x0, y0 = a0
            x1, y1 = a1
        else:
            x0, y0 = a0, a1
        glBegin(GL_LINES)
        glColor4f(*self.StrokeColor)
        glVertex3f(x0, y0, 0)
        glVertex3f(x1, y1, 0)
        glEnd()
        
    def end_frame(self):
        self.window.flip()
        
    def window_closed_by_user(self):
        print("clsoed")        
        

if __name__ == "__main__":
    import time
    D = 500
    s = Screen(D,D)

    points = [
        np.random.random((2,))*D for _ in range(100)
    ]

    def draw(s):
        s.start_frame()
        s.stroke(1.,1.,1.,1.)
        s.strokeWeight(5.0)
        for p in points:
            x, y = p
            s.stroke(x/D, y/D, 0.5, 1.0)
            s.point(p)
        s.end_frame()
        
    while True:
        draw(s)
        time.sleep(1)
