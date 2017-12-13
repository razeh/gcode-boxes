GCode Boxes
===========

### GCode Boxes

A python script that generates carving instructions for half bind
dovetails.

The expectation is that you have a CNC router where you can mount one
piece (the pin piece) vertically, clamped next to the tails. You'll
need to offset the tail piece by a small amount from the pin
piece. The offset depends on the dovetail bit and cutting height, but you can
generate the g-code for carving a spacer of the required offset with
spacer.py

Video: https://youtu.be/AtGqviCXuxg.

Dependencies
------------
GCode boxes use mecode to output the GCode.

### Status
[![Build Status](https://travis-ci.org/razeh/gcode-boxes.svg?branch=master)](https://travis-ci.org/razeh/gcode-boxes)
