from .frame import Frame
from .scene import Scene

import os
import sys

import pygame

class Viewer(Scene):
    def __init__(self, width, height, display=None, clear_color=(0,0,0,255)):
        Scene.__init__(self)
        self.width = width
        self.height = height
        self.Surface = pygame.display.set_mode((width, height))
        self.ClearColor = pygame.Color(*clear_color)
        self.main_frame = Frame()
        
    def frame(self, left, right, bottom, top, add=True, transient=False):
        assert right > left and top > bottom
        scalex = self.width/(right-left)
        scaley = self.height/(top-bottom)
        f = Frame.linear(left, right, bottom, top, 0, self.width, 0, self.height)
        if add:
            self.main_frame.add(f)
        return f

    def render(self, return_rgb_array=False, remove_transient=True):
        self.Surface.fill(self.ClearColor)
        self.main_frame.render(self.Surface)
        pygame.display.flip()          
        if remove_transient:
            self.main_frame.remove_transient()



