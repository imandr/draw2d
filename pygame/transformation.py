import numpy as np
import math
DEG2RAD = math.pi/180.0

class Transform(object):

    def __inti__(self, matrix=None):
        self.Matrix = matrix or np.eye(3)

    @staticmethod
    def scale(sx, sy=None):
        if sy is None: sy = sx
        return Transform(
            np.array([
                [sx, 0., 0.],
                [0., sy, 0.],
                [0., 0., 1.]
            ])
        )

    @staticmethod
    def rotate(phi, unit="rad"):
        if unit == "deg":
            phi *= DEG2RAD
        s, c = math.sin(phi), math.cos(phi)
        return Transform(
            np.array([
                [c, -s,  0.],
                [s,  c,  0.],
                [0., 0., 1.]
            ])
        )

    @staticmethod
    def transfer(dx, dy):
        return Transform(
            np.array([
                [1., 0., dx],
                [0., 1., dy],
                [0., 0., 1.]
            ])
        )

    def __mult__(self, other, y=None):
        if isinstance(other, Transform):
            return Transform(np.dot(self.Transform, other.Transform))
        else:
            if y is None:
                # assume x in 2-vector or tuple or list
                v = np.array(other, dtype=np.float)
            else:
                v = np.array((other, y), dtype=np.float)
            return np.dot(self.Transform, v)

class Pipeline(object):
    
    def __init__(self, transforms=[]):
        self.Transforms = transforms
        
    def apply(self, x, y=None):
        if y is None:
            # assume x in 2-vector or tuple or list
            v = np.array(x, dtype=np.float)
        else:
            v = np.array((x, y), dtype=np.float)
