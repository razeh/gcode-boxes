#!/usr/bin/env python

from __future__ import print_function
from mecode import GMatrix
from bit_info import DOVETAIL_BIT_1
from bit_info import DOVETAIL_BIT_2


class boatbox(object):
    def __init__(self,
                 x_length,
                 y_length,
                 z_length,
                 z_length_increment,
                 bit_info):
        self.x_length = x_length
        self.y_length = y_length
        self.z_length = z_length
        self.bit_info = bit_info
        self.g = GMatrix()
        self.g.linewidth = self.bit_diameter
        self.z_length_increment = z_length_increment
        print('; x_length =', self.x_length)
        print('; y_length =', self.y_length)
        print('; z_length =', self.z_length)
        print('; z_length_increment =', self.z_length_increment)

    @property
    def bit_diameter(self):
        return self.bit_info.largest_bit_diameter

    @property
    def bit_radius(self):
        return self.bit_diameter/2.0

    def clear_box(self):
        x_length = self.x_length - self.bit_radius
        y_length = self.y_length - self.bit_radius
        g = self.g
        z = 0

        def box():
            g.abs_move(x=0, y=0)
            g.meander(x_length, y_length, self.bit_diameter, 'LL', 'y')

        while z > -self.z_length:
            box()
            z -= self.z_length_increment
            g.move(z=self.z_length_increment)
            g.abs_move(z=z)
            
        if (z != -self.z_length):
            g.abs_move(z=-self.z_length)
            box()

    def bottom_wedge(self):
        g = self.g        
        g.abs_move(x=0, y=0)
        wedge_depth = self.bit_info.largest_bit_diameter - self.bit_info.smallest_bit_diameter
        g.move(y=-wedge_depth)
        g.move(x=self.x_length)
        g.move(x=-self.bit_diameter-1)
        g.abs_move(y=self.y_length+wedge_depth, x=self.x_length)
        g.move(x=-self.x_length)
        g.abs_move(x=self.x_length/2.0, y=self.y_length/2.0)
        g.abs_move(z=0.0)

    def box(self):
        self.clear_box()
        self.bottom_wedge()
        

if __name__ == "__main__":
    bb = boatbox(45.0, 20.00, 25.0, 1, DOVETAIL_BIT_2)
    bb.box()
    
