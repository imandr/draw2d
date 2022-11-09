from pygame import Color as PGColor

def Color(*args):
    if len(args) == 1 and isinstance(args[0], (tuple, list)):
        args = args[0]
    if len(args) == 1 and isinstance(args[0], (int, float)):
        x = args[0]
        args = (x,x,x)
    if len(args) in (3,4) and all(isinstance(x, (float, int)) and 0 <= x <= 255 for x in args):
        args = tuple(round(255*x) if isinstance(x, float) and x <= 1.0 else 
                    (round(x) if isinstance(x, float) else x)
                    for x in args
                )
        return PGColor(args)
    else:
        raise ValueError("Unrecognized arguments for Color: "+str(args))

class Attr(object):
    def enable(self):
        raise NotImplementedError
    def disable(self):
        pass

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

