import math

class BitInfo(object):
    def __init__(self, largest_bit_diameter, bit_angle, depth_of_cut):
        " Bit angle is in radians. "
        self.largest_bit_diameter = largest_bit_diameter
        self.bit_angle = bit_angle
        self.depth_of_cut = depth_of_cut
    
    def diameter_at_height(self, height):
        return self.largest_bit_diameter - (height * math.tan(self.bit_angle))

TO_MM=25.4  # number of milimeters in an inch
DOVETAIL_BIT_1 = BitInfo(TO_MM/2.0, 14 * (math.pi/180.0), TO_MM/2.0)
DOVETAIL_BIT_2 = BitInfo((5.0/16.0) * TO_MM, 8 * (math.pi/180.0), TO_MM/2.0)
DOVETAIL_BIT_3 = BitInfo(TO_MM*.75, 14 * (math.pi/180.0), (14.0/16.0)*TO_MM)
STRAIGHT_BIT_1 = BitInfo(24.4/4, 0.0, TO_MM)
