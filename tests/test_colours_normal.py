# This module, and all included code, is made available under the terms of the MIT Licence
#
# Copyright (c) 2023 David Love
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
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
"""Tests of the `colours` module using a normal byte order for words in the
colour conversion routines of the `Colour` class.

!!! note

Binary strings are used in the checks of the bit values to make it easier to
locate stray and incorrect bits. If a test fails, `pytest` should report the
correct binary representation, and the one received from the method.

Run as: `py.test test_colours_normal.py`
"""

from lbutils.graphics.colours import DEVICE_WORD_ORDER, Colour


def test_colour_white_565_normal():
    """Test that initialising the `Colour` class with Red = 255, Green = 255 and
    Blue = 255 gives the correct RGB565 response for the normal bit order.

    Expectation
    -----------

    **Pass**: Return value is 0xFF

    On-Failure
    ----------

      * Check the platform byte ordering has been correctly determined
      * Check the bit pattern returned against the expected in the method docstring
    """
    colour = Colour(255, 255, 255, word_order=DEVICE_WORD_ORDER.NORMAL)
    bin_string = f"{colour.as_rgb565:016b}"
    assert bin_string == "1111111111111111"
    assert colour.as_rgb565 == 0xFFFF


def test_colour_white_888_normal():
    """Test that initialising the `Colour` class with Red = 255, Green = 255 and
    Blue = 255 gives the correct RGB888 response for the normal bit order.

    Expectation
    -----------

    **Pass**: Return value is 0xFFFFFF

    On-Failure
    ----------

      * Check the platform byte ordering has been correctly determined
      * Check the bit pattern returned against the expected in the method docstring
    """
    colour = Colour(255, 255, 255, word_order=DEVICE_WORD_ORDER.NORMAL)

    bin_string = f"{colour.as_rgb888:024b}"
    assert bin_string == "111111111111111111111111"
    assert colour.as_rgb888 == 0xFFFFFF


def test_colour_black_565_normal():
    """Test that initialising the `Colour` class with Red = 0, Green = 0 and
    Blue = 0 gives the correct RGB565 response for the normal bit order.

    Expectation
    -----------

    **Pass**: Return value is 0x0

    On-Failure
    ----------

      * Check the platform byte ordering has been correctly determined
      * Check the bit pattern returned against the expected in the method docstring
    """
    colour = Colour(0, 0, 0, word_order=DEVICE_WORD_ORDER.NORMAL)
    bin_string = f"{colour.as_rgb565:016b}"
    assert bin_string == "0000000000000000"
    assert colour.as_rgb565 == 0x0


def test_colour_black_888_normal():
    """Test that initialising the `Colour` class with Red = 0, Green = 0 and
    Blue = 0 gives the correct RGB888 response for the normal bit order.

    Expectation
    -----------

    **Pass**: Return value is 0x0

    On-Failure
    ----------

      * Check the platform byte ordering has been correctly determined
      * Check the bit pattern returned against the expected in the method docstring
    """
    colour = Colour(0, 0, 0, word_order=DEVICE_WORD_ORDER.NORMAL)

    bin_string = f"{colour.as_rgb888:024b}"
    assert bin_string == "000000000000000000000000"
    assert colour.as_rgb888 == 0x0


def test_colour_red_565_normal():
    """Test that initialising the `Colour` class with Red = 255, Green = 0 and
    Blue = 0 gives the correct RGB565 response for the normal bit order.

    Expectation
    -----------

    **Pass**: Return value is 0xF8

    On-Failure
    ----------

      * Check the platform byte ordering has been correctly determined
      * Check the bit pattern returned against the expected in the method docstring
    """
    colour = Colour(255, 0, 0, word_order=DEVICE_WORD_ORDER.NORMAL)
    bin_string = f"{colour.as_rgb565:016b}"
    assert bin_string == "1111100000000000"
    assert colour.as_rgb565 == 0xF800


def test_colour_red_888_normal():
    """Test that initialising the `Colour` class with Red = 255, Green = 0 and
    Blue = 0 gives the correct RGB888 response for the normal bit order.

    Expectation
    -----------

    **Pass**: Return value is 0xFF0000

    On-Failure
    ----------

      * Check the platform byte ordering has been correctly determined
      * Check the bit pattern returned against the expected in the method docstring
    """
    colour = Colour(255, 0, 0, word_order=DEVICE_WORD_ORDER.NORMAL)

    bin_string = f"{colour.as_rgb888:024b}"
    assert bin_string == "111111110000000000000000"
    assert colour.as_rgb888 == 0xFF0000


def test_colour_green_565_normal():
    """Test that initialising the `Colour` class with Red = 0, Green = 255 and
    Blue = 0 gives the correct RGB565 response for the normal bit order.

    Expectation
    -----------

    **Pass**: Return value is 0x7E0

    On-Failure
    ----------

      * Check the platform byte ordering has been correctly determined
      * Check the bit pattern returned against the expected in the method docstring
    """
    colour = Colour(0, 255, 0, word_order=DEVICE_WORD_ORDER.NORMAL)
    bin_string = f"{colour.as_rgb565:016b}"
    assert bin_string == "0000011111100000"
    assert colour.as_rgb565 == 0x07E0


def test_colour_green_888_normal():
    """Test that initialising the `Colour` class with Red = 0, Green = 255 and
    Blue = 0 gives the correct RGB888 response for the normal bit order.

    Expectation
    -----------

    **Pass**: Return value is 0x00FF00

    On-Failure
    ----------

      * Check the platform byte ordering has been correctly determined
      * Check the bit pattern returned against the expected in the method docstring
    """
    colour = Colour(0, 255, 0, word_order=DEVICE_WORD_ORDER.NORMAL)

    bin_string = f"{colour.as_rgb888:024b}"
    assert bin_string == "000000001111111100000000"
    assert colour.as_rgb888 == 0x00FF00


def test_colour_blue_565_normal():
    """Test that initialising the `Colour` class with Red = 0, Green = 0 and
    Blue = 255 gives the correct RGB565 response for the normal bit order.

    Expectation
    -----------

    **Pass**: Return value is 0x7E0

    On-Failure
    ----------

      * Check the platform byte ordering has been correctly determined
      * Check the bit pattern returned against the expected in the method docstring
    """
    colour = Colour(0, 0, 255, word_order=DEVICE_WORD_ORDER.NORMAL)
    bin_string = f"{colour.as_rgb565:016b}"
    assert bin_string == "0000000000011111"
    assert colour.as_rgb565 == 0x001F


def test_colour_blue_888_normal():
    """Test that initialising the `Colour` class with Red = 0, Green = 0 and
    Blue = 255 gives the correct RGB888 response for the normal bit order.

    Expectation
    -----------

    **Pass**: Return value is 0x0000FF

    On-Failure
    ----------

      * Check the platform byte ordering has been correctly determined
      * Check the bit pattern returned against the expected in the method docstring
    """
    colour = Colour(0, 0, 255, word_order=DEVICE_WORD_ORDER.NORMAL)
    bin_string = f"{colour.as_rgb888:024b}"
    assert bin_string == "000000000000000011111111"
    assert colour.as_rgb888 == 0x0000FF


def test_colour_beckett_565_normal():
    """Test that initialising the `Colour` class with Red = 0, Green = 255 and
    Blue = 0 gives the correct RGB565 response for the normal bit order.

    Expectation
    -----------

    **Pass**: Return value is 0x7E0

    On-Failure
    ----------

      * Check the platform byte ordering has been correctly determined
      * Check the bit pattern returned against the expected in the method docstring
    """
    colour = Colour(61, 41, 108, word_order=DEVICE_WORD_ORDER.NORMAL)
    bin_string = f"{colour.as_rgb565:016b}"
    assert bin_string == "0011100101001101"
    assert colour.as_rgb565 == 0x394D


def test_colour_beckett_888_normal():
    """Test that initialising the `Colour` class with Red = 0, Green = 255 and
    Blue = 0 gives the correct RGB888 response for the normal bit order.

    Expectation
    -----------

    **Pass**: Return value is 0x3D296C

    On-Failure
    ----------

      * Check the platform byte ordering has been correctly determined
      * Check the bit pattern returned against the expected in the method docstring
    """
    colour = Colour(61, 41, 108, word_order=DEVICE_WORD_ORDER.NORMAL)

    bin_string = f"{colour.as_rgb888:024b}"
    assert bin_string == "001111010010100101101100"
    assert colour.as_rgb888 == 0x3D296C
