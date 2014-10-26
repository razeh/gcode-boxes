from mecode import G
import time


class box(object):
    def __init__(self, width, height):
        self.g = G()
        self.height = height
        self.width = width
        self.dimensions = [height, width]
        self.tabs = [3, 3]
        self.tab_depth = 20
        self.bit_size = 1
        self.mark_height = 10
        self.position_savepoints = []

    def save_position(self):
        g = self.g
        self.position_savepoints.append((g.current_position["x"],
                                         g.current_position["y"],
                                         g.current_position["z"]))
        print "saving ", self.position_savepoints[-1]

    def restore_position(self):
        g = self.g
        return_position = self.position_savepoints.pop()
        print "restoring ", return_position
        g.abs_move(return_position[0], return_position[1], return_position[2])

    def meander(self, x, y, start='LL', orientation='x'):
        g = self.g
        self.save_position()
        g.meander(x, y, self.bit_size*3, start, orientation)
        self.restore_position()

    def mark(self):
        g = self.g
        g.move(0, 0, self.mark_height)
        g.move(0, 0, -self.mark_height)
        self.mark_height += 5
        print g.current_position

    def move(self, index, amount):
        g = self.g
        args = {'y': (0, amount),
                'x': (amount, 0)}[index]
        g.move(*args)

    def box_side(self, index, direction):
        assert direction in [-1,1]
        g = self.g
        
        lookup= {'x':0, 'y':1}[index]

        meander_direction = { ('x',1)  : 'UL',
                              ('y',1)  : 'LL',
                              ('y',-1) : 'LR',
                            }[(index, direction)]

        tab_count = self.tabs[lookup]
        width = self.dimensions[lookup]/(1+(tab_count-1)*2.0)
        width *= direction
        for i in range(tab_count):

            dimensions = {'x': (width, self.tab_depth, meander_direction, index),
                          'y': (self.tab_depth, width, meander_direction, index) } [index]
            self.meander(*dimensions)


            if i != (tab_count-1):
                self.move(index, width*2)
            else:
                self.move(index, width)


    def box_level(self):
        g = self.g

        self.box_side('y', direction=1)
        self.box_side('x', direction=1)
        self.box_side('y', direction=-1)

        g.move(-self.height, 0)



if __name__ == "__main__":
    b = box(100, 200)
    b.box_level()
    b.g.view(backend="matplotlib")
    #time.sleep(600)
