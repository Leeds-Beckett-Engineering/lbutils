# Copyright (c) 2023 David Love
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Interface for the [Pmod
LED](https://digilent.com/reference/pmod/pmodoledrgb/start) GPIO module. This
class is also an example of a minimal GPIO Pmod, and can be used as the base
class for more extensive implementations.

## Pin Layout

The table below shows the standard GPIO pin numbers for the Pico H/W on the the
Leeds Beckett micron-controller development board, using the standard PMod
header below.

!!! note "Check the Header Row in Use"
    The [`LED`][lbutils.pmods.gpio.led] Pmod uses only a _single_ row of the
    header pins at any one time. This means that _either_ Table 1 _or_ Table 2_ will
    be in use: but **not** both at the same time.

    By default the [`LED`][lbutils.pmods.gpio.led] class
    assumes the module is connected to the _upper_ header in Table 1. This can be
    changed to use the lower row in Table 2 in the constructor for the
    [`LED`][lbutils.pmods.gpio.led] class: but must be specified explicitly.

![PMod J1 Header Layout](https://digilent.com/reference/_media/reference/pmod/pmod-pinout-1x6.png)

|        | Pin Name      | Number       | Description    |
|--------|---------------|--------------|----------------|
| Pin 1  | LD0           | 17           | LED 0          |
| Pin 2  | LD1           | 19           | LED 1          |
| Pin 3  | LD2           |              | LED 2          |
| Pin 4  | LD3           | 18           | LED 3          |
| Pin 5  | GND           | 3            | Ground         |
| Pin 6  | VCC           | 5            | VCC (+3.3V)    |

**Table 1: The Default Pin Layout for the `LED` PMod (Upper Header)**

|        | Pin Name      | Number       | Description    |
|--------|---------------|--------------|----------------|
| Pin 7  | LD0           | 14           | LED 0          |
| Pin 8  | LD1           |              | LED 1          |
| Pin 9  | LD2           | 22           | LED 2          |
| Pin 10 | LD3           |              | LED 3          |
| Pin 11 | GND           | 3            | Ground         |
| Pin 12 | VCC           | 5            | VCC (+3.3V)    |

**Table 2: The Default Pin Layout for the `LED` PMod (Lower Header)**

## Examples

  * Rotating Rope Light: `examples/pmods/pmod_led_example.py`

## References

* **Reference Manual:**
[LED](https://digilent.com/reference/pmod/pmodled/reference-manual)
"""

# Import the typing hints if available. Use our backup version
# if the official library is missing
try:
    from typing import List, Literal, Optional, Union
except ImportError:
    from lbutils.std.typing import List, Literal, Optional, Union  # type: ignore

# Import the core libraries
import ustruct
import utime

# Reference the MicroPython SPI and Pin library
from machine import SPI, Pin

# Allow the use of MicroPython constants
from micropython import const

# Import the common GPIO utilities and definitions
from .common import PMOD_ROW, PMOD_PIN_UPPER, PMOD_PIN_LOWER

###
### Classes
###


class LED:
    """Provides a simple GPIO interface for the `LED` Pmod, allowing the control
    of four LEDS. This class assumes the Pmod is connected to the _upper_ header
    row: this can be changed by setting the `pmod_row` in the constructor as
    `pmod_row = PMOD_ROW.UPPER`.

    The interface to this class is deliberately simple, as the `LED` Pmod is a
    good example of a general GPIO module. This class is therefore intended to act
    as an example for more sophisticated GPIO: either by direct use as a base class
    or by the code examples.

    Attributes
    ----------

    led0: bool
        The state of LED 0. When `True` LED 0 is on; when `False` LED 0 is off.
    led1: bool
        The state of LED 1. When `True` LED 0 is on; when `False` LED 0 is off.
    led2: bool
        The state of LED 1. When `True` LED 0 is on; when `False` LED 0 is off.
    led3: bool
        The state of LED 1. When `True` LED 0 is on; when `False` LED 0 is off.

    Methods
    -------

    * `set_state()`. Set the state of the named LEDs in a single call.
    """

    ##
    ## Constructors
    ##

    def __init__(self, pmod_row: PMOD_ROW = PMOD_ROW.UPPER) -> None:
        """Initialise the GPIO interface, and set all of the LEDs (GPIO Pins) to
        'off'.

        !!! note "Parameter Defaults for Pico H/W Dev Board"
            By default the `Pin` numbering for the upper row of Pmod connectors
            is used: if the lower row of Pmod connectors is required set the `pmod_row` parameter
            to `PMOD_ROW.LOWER`.

        Example
        -------

        A detailed example can be found in the `examples/pmods/
        pmod_led_example.py` folder. For the normal case, where the Pmod is connected to
        the upper row of header pins, the client only needs to call the constructor with
        the default values

        ````python
        # Instantiate the GPIO module with the default pin assignments
        # for the upper row of header pins
        led_controller = lbutils.pmods.gpio.LED()
        ````

        If the lower row of header pins is required, then the constructor argument
        **must** be set, for instance as

        ````python
        # Instantiate the GPIO module with the default pin assignments
        # for the lower row of header pins
        from lbutils.pmods.gpio import LED, PMOD_ROW

        led_controller = LED(pmod_row = PMOD_ROW.LOWER)
        ````

        Individual LEDs can then be turned on using the relevant attributes, e.g.

        ````python
        led_controller.led0 = True
        ````

        Similarly a direct assignment will also turn the stated LED off, as in

        ````python
        led_controller.led1 = False
        ````

        All the LEDs can be set to a specific state using the `set_state()`
        method, and passing in the state of the LEDs in order. For instance to turn only
        LED 2 `ON`, the client can call the method as

        ````python
        led_controller.set_state(False, False, True, False)
        ````

        Individual LEDs can also be named; for example the equivalent call to
        the above can be written as

        ````python
        led_controller.set_state(led0 = False, led1 = False, led2 = True, led3 = False)
        ````

        The use of named parameters in `set_state` also allows individual LEDs
        to be set (and named) directly, for instance as

        ````python
        led_controller.set_state(led2 = True)
        ````

        Note, however, that the state of LEDs which are _not_ named **will not
        change**. There is no 'implicit' state, and so the above is _not_ equivalent to
        the previous examples. The current state of the unnamed LEDS _will not_ be
        altered by this call: for instance the above example will _not_ modify the
        current state of `led0`, `led1` or `led3`.


        Parameters
        ----------
        pmod_row: PMOD_ROW
            Set the row (pin order) of the Pmod header to use. By default this
            class will use the upper row (equivalent to '`pmod_row = PMOD_PIN_UPPER`'). To
            use the lower row of pins set `pmod_row` explicitly as `pmod_row =
            PMOD_PIN_LOWER`.
        """
        # Set the local attributes
        self.pmod_row = pmod_row

        # Initialise the GPIO pins
        if pmod_row == PMOD_ROW.UPPER:
            self._GPIO0 = Pin(PMOD_PIN_UPPER.GPIO0, Pin.OUT)
            self._GPIO1 = Pin(PMOD_PIN_UPPER.GPIO1, Pin.OUT)
            self._GPIO2 = Pin(PMOD_PIN_UPPER.GPIO2, Pin.OUT)
            self._GPIO3 = Pin(PMOD_PIN_UPPER.GPIO3, Pin.OUT)
        else:
            self._GPIO0 = Pin(PMOD_PIN_LOWER.GPIO0, Pin.OUT)
            self._GPIO1 = Pin(PMOD_PIN_LOWER.GPIO1, Pin.OUT)
            self._GPIO2 = Pin(PMOD_PIN_LOWER.GPIO2, Pin.OUT)
            self._GPIO3 = Pin(PMOD_PIN_LOWER.GPIO3, Pin.OUT)

    ##
    ## Public Attributes
    ##

    pmod_row: PMOD_ROW

    ##
    ## Properties
    ##

    @property
    def led0(self) -> bool:
        """Sets, or returns, the current state of LED 0.

        When _reading_ from this property, a `bool` is returned with `True`
        representing the `HIGH` (or `ON`) state of the LED, and `False`
        representing the `LOW` (or `OFF`) state of the LED.

        When _writing_ to this property use `True` to set the LED output `HIGH`
        (or `ON`), or `False` to set the output `LOW` (or `OFF`).
        """
        return self._GPIO0.value()

    @led0.setter
    def led0(self, state: bool) -> None:
        self._GPIO0.value(state)

    @property
    def led1(self) -> bool:
        """Sets, or returns, the current state of LED 1.

        When _reading_ from this property, a `bool` is returned with `True`
        representing the `HIGH` (or `ON`) state of the LED, and `False`
        representing the `LOW` (or `OFF`) state of the LED.

        When _writing_ to this property use `True` to set the LED output `HIGH`
        (or `ON`), or `False` to set the output `LOW` (or `OFF`).
        """
        return self._GPIO1.value()

    @led1.setter
    def led1(self, state: bool) -> None:
        self._GPIO1.value(state)

    @property
    def led2(self) -> bool:
        """Sets, or returns, the current state of LED 2.

        When _reading_ from this property, a `bool` is returned with `True`
        representing the `HIGH` (or `ON`) state of the LED, and `False`
        representing the `LOW` (or `OFF`) state of the LED.

        When _writing_ to this property use `True` to set the LED output `HIGH`
        (or `ON`), or `False` to set the output `LOW` (or `OFF`).
        """
        return self._GPIO2.value()

    @led2.setter
    def led2(self, state: bool) -> None:
        self._GPIO2.value(state)

    @property
    def led3(self) -> bool:
        """Sets, or returns, the current state of LED 3.

        When _reading_ from this property, a `bool` is returned with `True`
        representing the `HIGH` (or `ON`) state of the LED, and `False`
        representing the `LOW` (or `OFF`) state of the LED.

        When _writing_ to this property use `True` to set the LED output `HIGH`
        (or `ON`), or `False` to set the output `LOW` (or `OFF`).
        """
        return self._GPIO3.value()

    @led3.setter
    def led3(self, state: bool) -> None:
        self._GPIO3.value(state)

    ##
    ## Methods
    ##

    def set_state(
        self,
        led0: Optional[bool] = None,
        led1: Optional[bool] = None,
        led2: Optional[bool] = None,
        led3: Optional[bool] = None,
        leds: Optional[List[bool]] = None,
    ) -> None:
        """Set the state of the named LEDs in a single call, using `True` for
        `HIGH` (or `ON`) and `False` for `LOW` (or `OFF`). This state can be set
        by **one** of the following.

        1. Using the `List` of `bool` values in the `leds` parameter to set the
        GPIO outputs. The first value in the list will be used to set LED 0, the second
        LED 1, etc. Missing values will _not_ result in a change of state.
        2. Using (some of) the parameters `led0` to `led3` to set the
        appropriate LED to the given state. These parameters can either be used as named
        values (e.g. `led1 = True`), or by position (e.g. `set_state(False, True)` to
        set LED 1). Missing position (or named) parameters will _not_ result in a change
        of state.

        Note that using the `leds` parameter will override any values set for
        `led0` to `led3`: both methods _cannot_ be used simultaneously in a single call.
        Similarly any LED whose state is not specified by either name or position using
        any of the above methods **will not** be set: instead it will be left at its
        current value.

        Raises
        ------

        ValueError:
            If the `leds` list is specified, and the types in the list cannot be
            converted to `bool` when setting the state of an LED.
        """

        # If the `leds` array is given, attempt to use this as
        # the source for the LED states. We will leave the exception
        # handling to the caller if they don't obey the type specification
        if leds is not None:
            if leds[0] is not None:
                self._GPIO0.value(leds[0])
            else:
                return

            if leds[1] is not None:
                self._GPIO1.value(leds[1])
            else:
                return

            if leds[2] is not None:
                self._GPIO2.value(leds[2])
            else:
                return

            if leds[3] is not None:
                self._GPIO3.value(leds[3])

            return

        # If we haven't been given a list of LED states, attempt to set the
        # state from the named arguments
        else:
            if led0 is not None:
                self._GPIO0.value(led0)

            if led1 is not None:
                self._GPIO1.value(led1)

            if led2 is not None:
                self._GPIO2.value(led2)

            if led3 is not None:
                self._GPIO3.value(led3)

            return
