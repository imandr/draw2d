from .transform import Transform
from .geoms import Sprite
from .scene import Scene

class Frame(Sprite, Scene):
    def __init__(self, hidden=False, **scene_args):
        Sprite.__init__(self, hidden)
        Scene.__init__(self, **scene_args)
        
    @staticmethod
    def linear(x0, x1, y0, y1, X0, X1, Y0, Y1, **args):
        return Frame(transform = Transform.linear(x0, x1, y0, y1, X0, X1, Y0, Y1), **args)
        
    def __str__(self):
        return "<Frame: %s>" % (repr(self.transform),)
        
    __repr__ = __str__
    
    def __getattr__(self, name):
        return getattr(self.transform, name)
        
