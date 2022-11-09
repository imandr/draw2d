import numpy as np
import math
DEG2RAD = math.pi/180.0

class Transform(object):

    def __init__(self, matrix=None, scale=(1.0, 1.0), angle=0.0, unit="rad", translate=(0.0, 0.0)):
        if matrix is not None:
            self.Matrix = matrix
        else:
            sx, sy = scale
            tx, ty = translate
            if unit == "deg":
                angle *= DEG2RAD
            s, c = math.sin(angle), math.cos(angle)
            self.Matrix = np.array([
                    [c*sx, -s*sy, tx],
                    [s*sx, c*sy, ty],
                    [0.0, 0.0, 1.0]
                ]).T
        self.Angle = angle
        
    @staticmethod
    def linear(x0, x1, y0, y1, X0, X1, Y0, Y1):
        #
        # linear transpomation from rectangle ((x0, y0), (x1, y1)) to ((X0, Y0), (X1, Y1))
        #
        assert x0 != x1 and y0 != y1
        scale = ((X1-X0)/(x1-x0), (Y1-Y0)/(y1-y0))
        tx = X0 - scale[0]*x0
        ty = Y0 - scale[1]*y0
        return Transform(scale=scale, translate=(tx, ty))

    @staticmethod
    def scale(sx, sy=None):
        if sy is None: sy = sx
        return Transform(np.array([
                [sx, 0., 0.],
                [0., sy, 0.],
                [0., 0., 1.]
            ]).T)

    @staticmethod
    def rotation(phi, unit="rad"):
        if unit == "deg":
            phi *= DEG2RAD
        s, c = math.sin(phi), math.cos(phi)
        return Transform(
            np.array([
                [c, -s,  0.],
                [s,  c,  0.],
                [0., 0., 1.]
            ]).T,
            angle = phi
        )

    @staticmethod
    def translate(dx, dy):
        return Transform(
            np.array([
                [1., 0., dx],
                [0., 1., dy],
                [0., 0., 1.]
            ]).T
        )

    def __mul__(self, other):
        print("__mul__", other, type(other))
        if isinstance(other, Transform):
            return Transform(np.dot(other.Matrix, self.Matrix), angle = self.Angle + other.Angle)
        else:
            # assume x in 2-vector or tuple or list
            v = np.empty((3,), dtype=float)
            v[:2] = other
            v[2] = 1.0
            return np.dot(v, self.Matrix)[:2]

class ______GContext(object):
    
    U = Transform(np.array([
                [1., 0., 0.],
                [0., 1., 0.],
                [0., 0., 1.]
            ]).T)
    
    def __init__(self):
        self.TStack = []               # [(tmatrix, product of all matrices including this one)]
        self.T = self.U

    def __mul__(self, x):
        v = np.array(v, dtype=float)
        return self.T*v

    def push(self, t):
        if isinstance(t, np.ndarray):
            assert t.shape == (3,3)
            t = Transform(t)
        self.TStack.append((t, self.T))
        self.T = self.T*t
        return self

    def pop(self):
        try:
            t, tp = self.TStack.pop(-1)
            self.T = tp
            return t
        except KeyError:
            self.T = self.U
            return None

    @property
    def angle(self):
        return self.T.Angle
        
    def __enter__(self, t):
        return self.push(t)
        
    def __exit__(self):
        self.pop()