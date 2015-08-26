#!/usr/bin/env python

import math
from mecode import GMatrix
from mecode import G

class dovetail(object):
    def __init__(self, side_thickness, side_height, bit_width_bottom):
        self.g                = GMatrix()
        self.side_thickness   = side_thickness
        self.side_height      = side_height
        self.bit_width_bottom = bit_width_bottom
        self.depth_increment  = 2
        self.depth_to_carve   = side_thickness
        # how far to move past the side.
        self.x_margin         = 10

    def one_dovetail(self):
        g = self.g
        cut_length = self.side_thickness * 2
        g.move(x=-cut_length)
        g.move(x=cut_length+self.x_margin)
        g.move(y=self.bit_width_bottom * 2)
        g.move(x=-self.x_margin)

    def dovetail_layer(self):
        g = self.g
        y = g.current_position['y']
        while y < self.side_height:
            self.one_dovetail()
            y = g.current_position['y']
        g.abs_move(x=0,y=0)

    def dovetails(self):
        g = self.g

        while g.current_position['z'] >= -self.depth_to_carve:
            self.dovetail_layer()
            g.move(z=-self.depth_increment)

        self.dovetail_layer()

if __name__ == "__main__":
    d = dovetail(side_thickness=19.05, side_height=63.5, bit_width_bottom=12.7)
    d.g.rotate(math.pi)
    d.dovetails()
    d.g.view(backend="matplotlib")

