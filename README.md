GCode Boxes
===========

### GCode Boxes

A python script that generates carving instructions for half blind
dovetails.

The expectation is that you have a CNC router where you can mount one
piece (the pin piece) vertically, clamped next to the tails. You'll
need to offset the tail piece by a small amount from the pin
piece. The offset depends on the dovetail bit and cutting height, but you can
generate the g-code for carving a spacer of the required offset with
spacer.py

The dovetails.py script takes a --mirror-x argument if you want to
reverse the direction of travel along the Y axis. This is useful if
one side of your box is a different width than the other.

Video: https://youtu.be/AtGqviCXuxg.

Dependencies
------------
GCode boxes use [mecode](https://github.com/jminardi/mecode) to output the GCode.

Instructions
------------

1. Download gcode-boxes
2. Download [mecode](https://github.com/jminardi/mecode)
3. Mecode depends on numpy, so you'll need to install it.
4. Add your bit information to bit_info.py
5. Update get_dovetail in dovetails.py to match your milling needs.
6. Run spacer.py to generate the gcode for a spacer, and then mill a spacer.
7. Run dovetail.py to generate the gcode for milling the dovetails. A test cut is strongly encouraged.


### Status
[![Build Status](https://travis-ci.org/razeh/gcode-boxes.svg?branch=master)](https://travis-ci.org/razeh/gcode-boxes)
