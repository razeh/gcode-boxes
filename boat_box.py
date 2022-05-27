#!/usr/bin/env python

from __future__ import print_function
from mecode import GMatrix
from bit_info import DOVETAIL_BIT_1
from bit_info import DOVETAIL_BIT_2
from bit_info import DOVETAIL_BIT_3
import math

def extra_width_for_depth(z, bit):
    return -math.tan(bit.bit_angle) * z

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
        print('; bit_diameter=', self.bit_diameter)

    @property
    def bit_diameter(self):
        return self.bit_info.largest_bit_diameter

    @property
    def bit_radius(self):
        return self.bit_diameter/2.0

    def x_length_at_z(self, z):
        return self.x_length - self.bit_radius + 2*extra_width_for_depth(z, self.bit_info)

    def y_length_at_z(self, z):
        return self.y_length - self.bit_radius + 2*extra_width_for_depth(z, self.bit_info)

    def offset_for_z(self, z):
        return extra_width_for_depth(z, self.bit_info)

    def clear_box(self):
        g = self.g
        z = 0

        def move_to_start_position():
            g.abs_move(x=-self.offset_for_z(z), y=-self.offset_for_z(z))

        def spiral_box():
            move_to_start_position()
            self.spiral_box(-self.offset_for_z(z), -self.offset_for_z(z),
                            self.x_length_at_z(z), self.y_length_at_z(z))

        while True:
            print('; starting spiral box z=', z)
            spiral_box()
            print('; finished spiral box z=', z)
            last_z = z
            z -= self.z_length_increment
            if z < -self.z_length:
                break
            g.abs_move(z=z)
            move_to_start_position()
            
        if (last_z != -self.z_length):
            g.abs_move(z=-self.z_length)
            move_to_start_position()
            spiral_box()

    def spiral_box(self, start_x, start_y, x_length, y_length):
        print('; spiral box ', x_length, y_length)
        g = self.g
        bit_radius = self.bit_diameter/2.0

        y_delta = y_length - bit_radius
        x_delta = x_length - bit_radius
        
        overlap = 1.0

        def y_move():
            return min(self.bit_diameter*overlap, y_delta - y_amount_moved['value'])

        y_amount_moved = { 'value': 0.0 }
        def move_y():
            if y_amount_moved['value'] < y_delta:
                y = y_move()
                g.move(y=y)
                y_amount_moved['value'] += y

        g.abs_move(start_x, start_y)
        while y_amount_moved['value'] < y_delta:
            g.move(x=x_delta)
            move_y()
            g.move(x=-x_delta)
            move_y()

        print('; cleanup at {}'.format(y_amount_moved['value']))
        g.abs_move(start_x, start_y)
        g.abs_move(start_x+x_delta, y=start_y)
        g.abs_move(start_x+x_delta, y=start_y+y_delta)
        g.abs_move(start_x, y=start_y+y_delta)
        g.abs_move(start_x, start_y)

    def withdraw(self):
        print('; withdraw ')
        g = self.g
        g.abs_move(x=self.x_length/2.0, y=self.y_length/2.0)
        g.abs_move(z=5)

    def box(self):
        self.g.feed(250)
        self.clear_box()
        self.withdraw()

if __name__ == "__main__":
    width = 3.25 * 25.4
    height = 5.75 * 25.4
    depth = (5/8.0) * 25.4
    bit = DOVETAIL_BIT_1
    bb = boatbox(width, height, 10.0, 1, bit)
    bb.box()
    
