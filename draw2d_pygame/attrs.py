from pygame import Color as PGColor

def Color(*args):
    if len(args) == 1:
        if args[0] is None:
            return None
        elif isinstance(args[0], (tuple, list)):
            args = args[0]
    converted = []
    for c in args:
        if isinstance(c, float) and c <= 1.0:
            c = round(c*255)
        elif isinstance(c, float):
            c = round(c)
        converted.append(c)
    return PGColor(*converted)

class Attr(object):
    def enable(self):
        raise NotImplementedError
    def disable(self):
        pass

class ____Color(Attr):
    def __init__(self, vec4):
        self.vec4 = vec4
    def __str__(self):
        return f"<Color {self.vec4}>"
    def enable(self):
        glColor4f(*self.vec4)

class LineStyle(Attr):
    def __init__(self, style):
        self.style = style
    def enable(self):
        glEnable(GL_LINE_STIPPLE)
        glLineStipple(1, self.style)
    def disable(self):
        glDisable(GL_LINE_STIPPLE)

class LineWidth(Attr):
    def __init__(self, stroke):
        self.stroke = stroke
    def enable(self):
        glLineWidth(self.stroke)

