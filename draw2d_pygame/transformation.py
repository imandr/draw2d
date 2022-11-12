import numpy as np
import math
DEG2RAD = math.pi/180.0

class Transform(object):
    
    def __init__(self, matrix=None, angle=0.0):
        self.Matrix = matrix if matrix is not None else np.eye(3)
        self.Angle = angle
    
    def __mul__(self, other):
        if isinstance(other, Transform):
            matrix = np.dot(other.matrix(), self.matrix())
            angle = other.Angle + self.Angle
            return Transform(matrix, angle)
        else:
            # assume x in 2-vector or tuple or list
            v = np.empty((3,), dtype=float)
            v[:2] = other
            v[2] = 1.0
            return np.dot(v, self.matrix())[:2]
    
    def matrix(self):
        return self.Matrix

    @property
    def translation(self):
        matrix = self.matrix()
        return matrix[2,0:2]

    @staticmethod
    def rotation(angle, unit="rad"):
        return IsoTransform(angle=angle, unit=unit)
        s, c = math.sin(angle), math.cos(angle)
        matrix = np.array([
                [c, -s, 0],
                [s, c, 0],
                [0.0, 0.0, 1.0]
            ]).T
        return Transform(matrix)

class IsoTransform(Transform):

    def __init__(self, scale=1.0, angle=0.0, unit="rad", translate=(0.0, 0.0)):
        self.Translation = translate
        if unit == "deg":
            angle *= DEG2RAD
        self.Angle = angle
        self.Scale = scale
        self.Matrix = None
    
    def __str__(self):
        return f"IsoTransform(scale={self.Scale}, angle={self.Angle}, translate={self.Translation})"

    def matrix(self):
        if self.Matrix is None:
            # cache
            scale = self.Scale
            tx, ty = self.Translation
            angle = self.Angle
            s, c = math.sin(angle), math.cos(angle)
            self.Matrix = np.array([
                    [c*scale, -s*scale, tx],
                    [s*scale, c*scale, ty],
                    [0.0, 0.0, 1.0]
                ]).T
        return self.Matrix

    def move_to(self, newx, newy):
        self.Translation = (float(newx), float(newy))
        self.Matrix = None      # force recalculation
        return self

    def move_by(self, deltax, deltay):
        return self.move_to(self.Translation[0]+deltax, self.Translation[1]+deltay)

    def rotate_to(self, angle, unit="rad"):
        if unit == "deg":
            angle *= DEG2RAD
        self.Angle = float(angle)
        self.Matrix = None      # force recalculation
        return self
        
    def rotate_by(self, angle, unit="rad"):
        if unit == "deg":
            angle *= DEG2RAD
        self.Angle += angle
        self.Matrix = None      # force recalculation
        return self

    def scale_to(self, new_s):
        self.Scale = new_s
        self.Matrix = None      # force recalculation
        return self

    def scale_by(self, delta):
        return self.scale_to(self.Scale*delta)

class BoxTransform(Transform):
    def __init__(self, x0, x1, y0, y1, X0, X1, Y0, Y1):
        Transform.__init__(self)
        assert x0 != x1 and y0 != y1
        sx, sy = self.Scale = ((X1-X0)/(x1-x0), (Y1-Y0)/(y1-y0))
        self.Translation = (X0 - sx*x0, Y0 - sy*y0)
        self.Matrix = None
            
    def matrix(self):
        if self.Matrix is None:
            # cache
            sx, sy = self.Scale
            tx, ty = self.Translation
            self.Matrix = np.array([
                    [sx, 0.0, tx],
                    [0.0, sy, ty],
                    [0.0, 0.0, 1.0]
                ]).T
        return self.Matrix

    def move_to(self, newx, newy):
        self.Translation = (float(newx), float(newy))
        self.Matrix = None      # force recalculation
        return self

    def move_by(self, deltax, deltay):
        return self.move_to(self.Translation[0]+deltax, self.Translation[1]+deltay)

    def scale_to(self, newx, newy):
        self.Scale = (float(newx), float(newy))
        self.Matrix = None      # force recalculation
        return self

    def scale_by(self, deltax, deltay):
        return self.scale_to(self.scale[0]*deltax, self.scale[1]*deltay)
