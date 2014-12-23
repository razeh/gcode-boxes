#!/usr/bin/env python

from mecode import GMatrix
import math
import time


class box(object):
    def __init__(self, height, width, depth, thickness, depth_increment, depth_to_carve):
        self.g = GMatrix()
        self.height = height
        self.width = width
        self.depth = depth
        self.thickness = thickness
        self.depth_increment = depth_increment
        self.depth_to_carve = depth_to_carve
        self.dimensions = {"height": height, "width": width, "depth":depth}
        self.tabs = {"height":2, "width":3, "depth":2}
        self.bit_size = 3.175
        self.g.linewidth = self.bit_size
        self.tab_depth = self.thickness - (self.bit_size/2.0)
        self.connector_depth = 5
        self.connector_length = 3
        self.mark_height = 10
        self.position_savepoints = []

    def should_make_connector(self):
        g = self.g
        current_z = g.current_position['z']
        if current_z <= -(self.thickness - self.connector_depth):
            return True
        return False

    def move_with_connector(self, distance):
        g = self.g
        if self.should_make_connector():
            lower_cut_distance = (distance - self.connector_length)/2.0
            g.move(0, lower_cut_distance)
            g.move(z=self.connector_depth)
            g.move(0, self.connector_length)
            g.move(z=-self.connector_depth)
            g.move(0, lower_cut_distance)

        else:
            g.move(0, distance)

    def box(self, x, y):
        " Carve a box x by y wide with little bitsize indents"
        g = self.g
        indent = self.bit_size/2.0
        g.move(y=self.bit_size * .5)
        g.move(x+indent)
        g.move(-indent)
        g.move(y=y - self.bit_size)
        g.move(indent)
        g.move(-indent -x)
        g.move(y=self.bit_size * .5)

    def meander(self, x, y):
        g = self.g
        self.box(x,y)
        g.meander(x, y, self.bit_size, 'LL', 'y')
        # add in a little notch because the bit is circular
        g.move(self.bit_size/2.0)
        g.move(-self.bit_size/2.0)
        g.move(y=-y)
        g.move(self.bit_size/2.0)
        g.move(-self.bit_size/2.0)
        g.move(-x)

    def mark(self):
        g = self.g
        g.move(0, 0, self.mark_height)
        g.move(0, 0, -self.mark_height)
        self.mark_height += 5
        print g.current_position

    def box_panel(self, index, alternate=False):
        g = self.g
        tab_count = self.tabs[index]
        width = self.dimensions[index]/(1+(tab_count-1)*2.0)

        if alternate:
            for i in range(tab_count):
                self.move_with_connector(width)
                if i != (tab_count-1):
                    self.box(self.tab_depth, width)
        else:
            for i in range(tab_count):
                self.box(self.tab_depth, width)
                if i != (tab_count-1):
                    self.move_with_connector(width)


    def box_bottom(self):
        g = self.g
        self.box_panel('depth')
        g.push_matrix()
        g.rotate(-math.pi/2)
        self.box_panel('width')
        g.rotate(-math.pi/2)
        self.box_panel('depth')
        g.rotate(-math.pi/2)
        self.box_panel('width')
        g.pop_matrix()
        
    def box_side(self):
        g = self.g
        g.push_matrix()
        self.box_panel('depth', alternate=True)
        g.rotate(-math.pi/2)
        self.box_panel('height', alternate=True)
        g.rotate(-math.pi/2)
        g.move(0, self.depth)
        g.rotate(-math.pi/2)
        self.box_panel('height', alternate=True)
        g.pop_matrix()
    
    def box_front(self):
        g = self.g
        g.push_matrix()
        self.box_panel('width', alternate=True)
        g.rotate(-math.pi/2)
        self.box_panel('height')
        g.rotate(-math.pi/2)
        g.move(0, self.width)
        g.rotate(-math.pi/2)
        self.box_panel('height')
        g.pop_matrix()

    def box_drill(self, func, start_x=0, start_y=0):
        g = self.g
        start_z = g.current_position['z']
        
        if self.g.current_position['x'] != start_x \
           or self.g.current_position['y'] != start_y:
            start_color = g.current_color
            g.current_color="red"
            g.abs_move(z=10)
            g.abs_move(start_x, start_y)
            g.abs_move(z=0)
            g.current_color=start_color

        z = -self.depth_increment
        while True:
            g.abs_move(z=z)
            func()
            z -= self.depth_increment
            if -z > self.depth_to_carve:
                g.abs_move(z=-self.thickness)
                func()
                break

        g.abs_move(z=start_z)

if __name__ == "__main__":
    b = box(height=60, width=70, depth=60, thickness=14,
            depth_increment = 1, depth_to_carve = 18)
    box_gap = 30

    b.g.feed(1000) # plywood
    
    #b.box_drill(b.box_bottom)
    b.box_drill(b.box_side)
    #b.box_drill(b.box_side, b.width+box_gap)
    #b.box_drill(b.box_side, b.width+b.height+box_gap*2)
    #b.box_drill(b.box_front, b.width+(b.height*2)+box_gap*3)
    #b.box_drill(b.box_front, b.width+(b.height*3)+box_gap*4)

    b.g.view(backend="matplotlib")

