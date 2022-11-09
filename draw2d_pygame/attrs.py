class Attr(object):
    def enable(self):
        raise NotImplementedError
    def disable(self):
        pass

class Color(Attr):
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

