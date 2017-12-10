GCode Boxes
===========

### GCode Boxes

A short python script that will generate the carving instructions for
half bind dovetails.

The expectation is that you have a CNC router where you can mount one
piece (the pin piece) vertically, clamped next to the tails. You'll
need to offset the tail piece by a small amount from the pin
piece. The offset depends dovetail bit and cutting height, but you can
get the g-code for carving a spacer of theq required offset with
spacer.py

THere is a video of the g-code in action at https://youtu.be/AtGqviCXuxg.

Dependencies
------------
GCode boxes use mecode to output the GCode.

### Status
[![Build Status](https://travis-ci.org/razeh/gcode-boxes.svg?branch=master)](https://travis-ci.org/razeh/gcode-boxes)
