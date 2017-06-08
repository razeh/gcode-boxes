#!/usr/bin/env python
""" Drill out a space for a set of dovetail joints. """

from mecode import GMatrix
from bit_info import STRAIGHT_BIT_1
import dovetails

class spacer(object):
    def __init__(self, length, depth, bit_info, dovetail):
        self.g = GMatrix()
        self.length = length
        self.depth = depth
        self.bit_info = bit_info
        self.dovetail = dovetail
        self.width = dovetail.period / 2.0
        print('; width = {}'.format(self.width))

    def __call__(self):
        g = self.g
        g.feed(250)
        
        def cutting_pass():
            y_delta = self.width + self.bit_info.largest_bit_diameter
            g.move(x=self.length)
            g.move(y=y_delta)
            g.move(x=-self.length)
            g.move(y=-y_delta)

        z = 0.0
        z_delta = self.bit_info.largest_bit_diameter / 3.0
        cutting_pass()
        while z > -self.depth:
            z -= z_delta
            g.move(z=-z_delta)
            cutting_pass()
            
if __name__ == "__main__":
    length = 100
    depth = 25.4*(3.0/8.0) #6.35
    
    s = spacer(length, depth, bit_info=STRAIGHT_BIT_1, dovetail=dovetails.get_dovetail())
    s()
