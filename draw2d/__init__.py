import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
pygame.init()

from .attrs import Color
from .geoms import Geom, Point, PolyLine, Line, Image, Circle, Polygon, Rectangle, Text, Marker, FilledPolygon
from .frame import Frame
from .viewer import Viewer
from .transformation import Transform


