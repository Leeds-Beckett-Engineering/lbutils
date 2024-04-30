# This example, and all included code, is made available under the terms of the
# MIT License
#
# Copyright (c) 2023 Roz Wyatt-Millington, David Love
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sub-license, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""Example for the [Pmod
OLEDrgb](https://digilvcc_enablet.com/refervcc_enablece/pmod/pm
odoled_displayrgb/start) , using the `lbutils.font` library and the
`lbutils.drivers.SSD1331` display driver. This also gives an example of all the
fonts in the font library, and serves as a functional test for the display.

Tested Implementations
----------------------

This version is written for MicroPython 3.4, and has been tested on:

  * Raspberry Pi Pico H/W
"""

# Import the SPI, GPIO and framebuffer MicroPython libraries
try:
    import framebuf
    from machine import SPI, Pin
except ImportError:
    msg = "Error: Missing required MicroPython includes!"
    raise RuntimeError(msg) from ImportError

# Import the lbutils graphics library
try:
    from lbutils import graphics
    from lbutils.graphics import colours, fonts
except ImportError:
    msg = ("Error: Missing required LBUtils graphics library",)
    raise RuntimeError(msg) from ImportError

# Import the LB Utils driver for the Pmod OLEDrgb
try:
    from lbutils.pmods.spi import OLEDrgb
except ImportError:
    msg = "Error: Cannot find the Pmod OLEDrgb driver!"
    raise RuntimeError(msg) from ImportError

# Import the core libraries
import utime

##
## Setup the SPI interface to the Pmod OLEDrgb
##

# Initialise the OLED display driver, using the default
# pin assignments and SPI interface, and set the display to black
oled_display = OLEDrgb()
oled_display.fill_screen(colours.COLOUR_BLACK)

# Set the origin for the tests
oled_display.origin.x_y = [0, 0]

##
## Font Examples. Also showing different methods for setting the
## start point of the `write_text` routine used to draw the
## text in the specified font
##

# Display the `Font_08` font class in red, and set the cursor
# of the `oled_display` manually each time.
print("Running the screen test for the `Font08` font...")

oled_display.fg_colour = colours.COLOUR_RED
oled_display.font = fonts.Font08()

oled_display.x_y = [0, 20]
oled_display.write_text("ABCDEFGHIJKLMN")

oled_display.x_y = [0, 30]
oled_display.write_text("OPQRSTUVWXYZ")

oled_display.x_y = [0, 40]
oled_display.write_text("abcdefghijklmn")

oled_display.x_y = [0, 50]
oled_display.write_text("opqrstuvwxyz")

oled_display.x_y = [0, 60]
oled_display.write_text("0123456789")

utime.sleep(10)

# Clear the display
oled_display.fill_screen(colours.COLOUR_BLACK)

# Display the `Font06` font class in green, and set the cursor
# at the start of each call to `write_text`
print("Running the screen test for the `Font06` font...")

oled_display.fg_colour = colours.COLOUR_LIME
oled_display.font = fonts.Font06()

oled_display.write_text(start=[0, 20], txt_str="ABCDEFGHIJKLMN")
oled_display.write_text(start=[0, 30], txt_str="OPQRSTUVWXYZ")
oled_display.write_text(start=[0, 40], txt_str="abcdefghijklmn")
oled_display.write_text(start=[0, 50], txt_str="opqrstuvwxyz")
oled_display.write_text(start=[0, 60], txt_str="0123456789")

utime.sleep(10)

# Clear the display
oled_display.fill_screen(colours.COLOUR_BLACK)

# Display the `Org01` font class in blue, and use the origin
# with an offset to display the text using `write_text`
print("Running the screen test for the `Org01` font...")

oled_display.fg_colour = colours.COLOUR_BLUE
oled_display.font = fonts.Org01()

oled_display.write_text(
    start=oled_display.origin.offset(y=20),
    txt_str="ABCDEFGHIJKLMN",
)
oled_display.write_text(
    start=oled_display.origin.offset(y=30),
    txt_str="OPQRSTUVWXYZ   ",
)
oled_display.write_text(
    start=oled_display.origin.offset(y=40),
    txt_str="abcdefghijklmn ",
)
oled_display.write_text(
    start=oled_display.origin.offset(y=50),
    txt_str="opqrstuvwxyz   ",
)
oled_display.write_text(
    start=oled_display.origin.offset(y=60),
    txt_str="0123456789     ",
)

utime.sleep(10)

##
## Colour Rotation of the Full Display
##

colors = []
for i in range(8):
    r = (i & 1) * 255
    g = ((i >> 1) & 1) * 255
    b = ((i >> 2) & 1) * 255
    colors.append(colours.Colour(r, g, b))

print("Running the colour test...")
while True:
    for color in colors:
        oled_display.fill_screen(color)

        utime.sleep(1)
