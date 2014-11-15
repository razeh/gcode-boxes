#!/usr/bin/env python

# A brief test that everything with mecode and rotations
# works.

import math
from mecode import GMatrix
import time


class box(object):
    def __init__(self, height, width):
        self.g = GMatrix()
        self.height = height
        self.width = width

    def box_level(self):
        g = self.g
        g.move(0, self.width)
        g.move(self.height, 0)
        g.move(0, -self.width)
        g.move(-self.height, 0)


    def boxes(self):
        g = self.g
        g.save_position()
        g.meander(self.width, self.height, self.width/15.0)
        g.restore_position()
        #self.box_level()
        g.rotate(math.pi/8)
        g.meander(self.width, self.height, self.width/15.0)
        #self.box_level()


if __name__ == "__main__":
    b = box(5, 10)
    b.boxes()
    b.g.view(backend="matplotlib")

