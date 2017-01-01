#!/usr/bin/env python

# Current problems:
# the y move to get to the start of the arcs is at feed rate, not rapid move rate
# there are a bunch of redundant moves while doing the arcs
# when cutting the slots we go backwards for a bit.
# we cut the slots too far.

import math
import sys
from mecode import GMatrix
from mecode import G
from bit_info import DOVETAIL_BIT_1
from bit_info import DOVETAIL_BIT_2


EPSILON = .01

class Constraints(object):
    """ The relationship between height or depth of cut (h), bit angle(e), 
    the bit's widest diameter (d) and the distance between tails is:

    h * tan(e) = d - (p/2)
    
    """
    def __init__(self, largest_bit_diameter, bit_angle, wood_width):
        self.largest_bit_diameter = largest_bit_diameter
        self.bit_angle = bit_angle
        self.wood_width = wood_width

    def solve_for_period(self, height):
        " Distance from pin-to-pin for a given height."
        return 2 * (self.largest_bit_diameter - (height * math.tan(self.bit_angle)))

    def solve_for_periods(self, height):
        period = self.solve_for_period(height)
        return int(math.floor(self.wood_width / period))

    def solve_for_slop(self, height):
        " Left over space after we've gone pin-to-pin for a height. "
        period = self.solve_for_period(height)
        return self.wood_width - (self.solve_for_periods(height) * period)

class CarvingSpeed(object):
    def __init__(self, dovetail):
        self.dovetail = dovetail

    def __enter__(self):
        self.dovetail.g.feed(self.dovetail.carving_speed)

    def __exit__(self, *args):
        self.dovetail.g.feed(self.dovetail.rapid_speed)

class dovetail(object):
    def __init__(self, wood_thickness, wood_width, height, bit_info):
        self.g = GMatrix()
        self.constraints = Constraints(bit_info.largest_bit_diameter, bit_info.bit_angle, wood_width)
        self.bit_info = bit_info
        self.wood_width = wood_width
        self.period = self.constraints.solve_for_period(height)
        self.slop = self.constraints.solve_for_slop(height)
        self.height = height
        self.wood_thickness = wood_thickness
        print '; Period = ', self.period
        print '; Periods = ', self.periods
        print '; Slop = ', self.slop
        print '; Bit diameter = ', self.bit_diameter
        print '; Wood thickness = ', self.wood_thickness
        print '; Height = ', self.height
        self.x_margin = 10
        assert self.x_margin > self.bit_diameter
        self.rapid_speed = 600
        self.carving_speed = 100

    @property
    def bit_diameter(self):
        return self.bit_info.largest_bit_diameter

    @property
    def bit_radius(self):
        return self.bit_diameter/2.0

    @property
    def periods(self):
        return self.constraints.solve_for_periods(self.height) + 2 # one extra for the start and end.

    def dovetail(self):
        g = self.g
        # Get us out of the 0,0 position; we expect to start 
        # right at the corner of the vertical piece.
        x_start = self.x_margin + self.bit_diameter
        print '; x_start = ', x_start
        print '; x_margin = ', self.x_margin

        # How much shorter the bit is at the top than the bottom
        # because it is an angled bit.
        width_delta = self.height*math.tan(self.bit_info.bit_angle)
        print '; width delta = ', width_delta, ' ', self.height, ' * ', math.tan(self.bit_info.bit_angle)

        g.feed(self.rapid_speed)
        g.abs_move(x=x_start)
        g.move(z=-self.height)

        # Figure out where we want our cuts to start
        start_points = [(i * self.period) + (self.slop/2.0) - self.period for i in range(self.periods)]
        print '; start_points = ', start_points

        x_delta = self.x_margin + (2.0* self.wood_thickness)
        print '; x_delta = ', x_delta

        def carve_period(width):
            """ This will carve out a section, starting at our current y and going for width.
            You can use this to simulate a larger bit size by setting width to be larger than the
            bit size. """
            print '; start of width'.format(width)
            y_offset = 0.0
            print '; y at start', g.current_position['y']
            start_y = g.current_position['y']
            g.move(y=self.bit_radius)

            with CarvingSpeed(self):
                g.move(x=-x_delta)
            g.move(x=x_delta)

            y_offset += self.bit_radius
            while y_offset < width - self.bit_radius:
                distance_to_end_of_width = width - (y_offset + self.bit_radius)
                if distance_to_end_of_width == 0:
                    break
                y_move_amount = min(distance_to_end_of_width, self.bit_diameter/3.0)
                g.move(y=y_move_amount)
                y_offset += y_move_amount
                with CarvingSpeed(self):
                    g.move(x=-x_delta)
                g.move(x=+x_delta)

            print '; y at end', g.current_position['y']
            print ';end of width {}'.format(width)
            width_travelled = g.current_position['y'] - start_y
            width_cut = width_travelled + self.bit_radius # Take into account the initial move
            assert abs(width - width_cut) < EPSILON, 'Incorrect width cut {} != {}'.format(width, width_cut)

        # Set parameters for the arcs that will fit into the curved
        # portions we cut. The arcs need to match the bit we are
        # using.


        def carve_arc():
            print ';start of arc'
            arc_diameter = self.bit_info.diameter_at_height(self.height)
            g.arc(x=arc_diameter, y=arc_diameter, radius=arc_diameter, direction='CCW')
            g.arc(x=-arc_diameter, y=arc_diameter, radius=arc_diameter, direction='CCW')
            print ';end of arc'

        for y_start in start_points:
            g.abs_move(x=x_start, y=y_start)
            carve_period(self.bit_diameter)
            g.abs_move(x=x_start)
        
        g.abs_move(x=self.x_margin)
        for y_start in start_points:
            # We offset by the radius to match how we offset in carve period
            g.abs_move(y=y_start + self.bit_radius)
            g.abs_move(x=0)
            carve_arc()


def get_dovetail():
    d = dovetail(wood_thickness=16.4, wood_width=295.0, height=25.4*(3.0/8.0), bit_info=DOVETAIL_BIT_2)
    return d

if __name__ == "__main__":
    d = get_dovetail()
    d.dovetail()
