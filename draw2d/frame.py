from .transformation import IsoTransform, BoxTransform
from .geoms import Geom

class Frame(Geom):
    def __init__(self, scale=1.0, angle=0.0, unit="rad", translate=(0.0, 0.0), transform=None, **geom_args):
        transform = transform or IsoTransform(scale=scale, angle=angle, unit=unit, translate=translate)
        Geom.__init__(self, transform=transform, **geom_args)
        self.Named = {}
        self.Unnamed = []

    @staticmethod
    def box(x0, x1, y0, y1, X0, X1, Y0, Y1, **args):
        transform = BoxTransform(x0, x1, y0, y1, X0, X1, Y0, Y1)
        return Frame(transform=transform)

    def __str__(self):
        return f"Frame(scale={self.Transform.Scale}, angle={self.Transform.Angle}, translation={self.Transform.Translation})"
        
    __repr__ = __str__

    def add(self, g, label=None, at=None, rotation=None, scale=None):
        if label is None:
            self.Unnamed.append(g)
        else:
            self.Named[label] = g
        if at is not None:  g.move_to(*at)
        if rotation is not None:    g.rotate_to(rotation)
        if scale is not None:   g.scale_to(*scale)
        return self
            
    def __getitem__(self, label):
        return self.Named[label]
        
    def render(self, surface, transform=None):
        if transform is None:
            c = self.Transform
        else:
            c = transform * self.Transform
        for g in self.Unnamed + list(self.Named.values()):
            if not g.Hidden:
                #print("rendering:", g)
                g.render(surface, c)

    def locate(self, context=None):
        t = self.Transform
        if context is not None:
            t = context * t
        for g in self.Unnamed + list(self.Named.values()):
            g.locate(t)
        return Geom.locate(self, context)

    def remove_all(self):
        self.Named = {}
        self.Unnamed = []
    
    clear = remove_all

    def remove(self, label):
        return self.Named.pop(label, None)

    def remove_transient(self):
        self.Unnamed = [s for s in self.Unnamed if not s.Transient]
        self.Named = {label:s for label, s in self.Named.items() if not s.Transient}
        for s in self.Unnamed + list(self.Named.values()):
            if isinstance(s, Frame):
                s.remove_transient()

