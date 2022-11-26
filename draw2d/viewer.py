from .frame import Frame
from .attrs import Color

import os
import sys

import pygame
pygame.init()


class Viewer(object):
    def __init__(self, width, height, display=None, clear_color=(0,0,0,255)):
        self.width = width
        self.height = height
        self.Surface = pygame.display.set_mode((width, height))
        self.ClearColor = Color(*clear_color)
        self.RootFrame = self.set_frame(0, width, 0, height)

    def frame(self, *params, **args):
        if not params and not args:
            return self.RootFrame
        else:
            return self.set_frame(*params, **args)

    def set_frame(self, left, right, bottom, top):
        scalex = self.width/(right-left)
        scaley = self.height/(top-bottom)
        self.RootFrame = Frame.box(left, right, bottom, top, 0, self.width, self.height, 0)
        return self.RootFrame

    def render(self, return_rgb_array=False, remove_transient=True):
        self.Surface.fill(self.ClearColor)
        self.RootFrame.render(self.Surface)
        pygame.display.flip()          
        if remove_transient:
            self.RootFrame.remove_transient()
        return self.Surface.get_buffer().raw

    def locate(self):
        self.RootFrame.locate()



