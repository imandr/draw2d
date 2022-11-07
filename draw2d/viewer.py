from .frame import Frame
from .scene import Scene

import os
import six
import sys

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


class Viewer(Scene):
    def __init__(self, width, height, display=None, clear_color=(0,0,0,1)):
        Scene.__init__(self)
        display = get_display(display)

        self.width = width
        self.height = height
        self.window = pyglet.window.Window(width=width, height=height, display=display)
        self.window.on_close = self.window_closed_by_user
        self.isopen = True
        self.clear_color = clear_color
        self.main_frame = Frame()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_PROGRAM_POINT_SIZE)
        glPointSize(2.0)
        
    def frame(self, left, right, bottom, top, add=True, transient=False):
        assert right > left and top > bottom
        scalex = self.width/(right-left)
        scaley = self.height/(top-bottom)
        
        f = Frame.linear(left, right, bottom, top, 0, self.width, 0, self.height)
        if add:
            self.main_frame.add(f)
        return f

    def render(self, return_rgb_array=False, remove_transient=True):
        self.window.switch_to()
        self.window.dispatch_events()
        glClearColor(*self.clear_color)
        self.window.clear()
        self.main_frame.render()
        arr = None
        if return_rgb_array:
            import numpy as np
            buffer = pyglet.image.get_buffer_manager().get_color_buffer()
            image_data = buffer.get_image_data()
            print(type(image_data), dir(image_data))
            arr = np.frombuffer(image_data.data, dtype=np.uint8)
            # In https://github.com/openai/gym-http-api/issues/2, we
            # discovered that someone using Xmonad on Arch was having
            # a window of size 598 x 398, though a 600 x 400 window
            # was requested. (Guess Xmonad was preserving a pixel for
            # the boundary.) So we use the buffer height/width rather
            # than the requested one.
            arr = arr.reshape(buffer.height, buffer.width, 4)
            arr = arr[::-1,:,0:3]
        self.window.flip()
        if remove_transient:
            self.main_frame.remove_transient()
        return arr if return_rgb_array else self.isopen

    def window_closed_by_user(self):
        self.isopen = False

