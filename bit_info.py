import math

class BitInfo(object):
    def __init__(self, largest_bit_diameter, bit_angle):
        " Bit angle is in radians. "
        self.largest_bit_diameter = largest_bit_diameter
        self.bit_angle = bit_angle
    
    def diameter_at_height(self, height):
        return self.largest_bit_diameter - (height * math.tan(self.bit_angle))

    
DOVETAIL_BIT_1 = BitInfo(25.4/2.0, 14 * (math.pi/180.0))
DOVETAIL_BIT_2 = BitInfo((5.0/16.0) * 25.4, 8 * (math.pi/180.0))
STRAIGHT_BIT_1 = BitInfo(24.4/4, 0.0)
