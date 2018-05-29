from enum import Enum
import bitstring

_name = "Led"
_name_id = 1


class InvalidPatternException(Exception):
    pass


def parse_config(split_config):
    pass


class InvalidColorValue(Exception):
    pass


class InvalidMultiColorConfigurationException(Exception):
    pass


class Color:
    def __init__(self, r, g, b):
        self._r = 0
        self._g = 0
        self._b = 0
        self.r = r
        self.g = g
        self.b = b

    def _set_color(self, color, value):
        if value < 0 or value > 255:
            raise InvalidColorValue("Color value has to be an integer in the range [0,255] | Given {}".format(value))
        color = value

    @property
    def r(self):
        return self._value

    @r.setter
    def r(self, value):
        self._set_color(self._r, value)

    @property
    def g(self):
        return self._value

    @g.setter
    def g(self, value):
        self._set_color(self._g, value)

    @property
    def b(self):
        return self._value

    @b.setter
    def b(self, value):
        self._set_color(self._b, value)

    def __repr__(self):
        return "{},{},{}".format(self.r, self.g, self.b)


class PredefinedColors(Enum):
    # Colors scraped from https://en.wikipedia.org/wiki/Web_colors#X11_color_names
    OFF = Color(0, 0, 0) # Black is the "off" color
    PINK = Color(255, 192, 203)
    LIGHT_PINK = Color(255, 182, 193)
    HOT_PINK = Color(255, 105, 180)
    DEEP_PINK = Color(255, 20, 147)
    PALE_VIOLET_RED = Color(219, 112, 147)
    MEDIUM_VIOLET_RED = Color(199, 21, 133)
    LIGHT_SALMON = Color(255, 160, 122)
    SALMON = Color(250, 128, 114)
    DARK_SALMON = Color(233, 150, 122)
    LIGHT_CORAL = Color(240, 128, 128)
    INDIAN_RED = Color(205, 92, 92)
    CRIMSON = Color(220, 20, 60)
    FIRE_BRICK = Color(178, 34, 34)
    DARK_RED = Color(139, 0, 0)
    RED = Color(255, 0, 0)
    ORANGE_RED = Color(255, 69, 0)
    TOMATO = Color(255, 99, 71)
    CORAL = Color(255, 127, 80)
    DARK_ORANGE = Color(255, 140, 0)
    ORANGE = Color(255, 165, 0)
    YELLOW = Color(255, 255, 0)
    LIGHT_YELLOW = Color(255, 255, 224)
    LEMON_CHIFFON = Color(255, 250, 205)
    LIGHT_GOLDENROD_YELLOW = Color(250, 250, 210)
    PAPAYA_WHIP = Color(255, 239, 213)
    MOCCASIN = Color(255, 228, 181)
    PEACH_PUFF = Color(255, 218, 185)
    PALE_GOLDENROD = Color(238, 232, 170)
    KHAKI = Color(240, 230, 140)
    DARK_KHAKI = Color(189, 183, 107)
    GOLD = Color(255, 215, 0)
    CORNSILK = Color(255, 248, 220)
    BLANCHED_ALMOND = Color(255, 235, 205)
    BISQUE = Color(255, 228, 196)
    NAVAJO_WHITE = Color(255, 222, 173)
    WHEAT = Color(245, 222, 179)
    BURLY_WOOD = Color(222, 184, 135)
    TAN = Color(210, 180, 140)
    ROSY_BROWN = Color(188, 143, 143)
    SANDY_BROWN = Color(244, 164, 96)
    GOLDENROD = Color(218, 165, 32)
    DARK_GOLDENROD = Color(184, 134, 11)
    PERU = Color(205, 133, 63)
    CHOCOLATE = Color(210, 105, 30)
    SADDLE_BROWN = Color(139, 69, 19)
    SIENNA = Color(160, 82, 45)
    BROWN = Color(165, 42, 42)
    MAROON = Color(128, 0, 0)
    DARK_OLIVE_GREEN = Color(85, 107, 47)
    OLIVE = Color(128, 128, 0)
    OLIVE_DRAB = Color(107, 142, 35)
    YELLOW_GREEN = Color(154, 205, 50)
    LIME_GREEN = Color(50, 205, 50)
    LIME = Color(0, 255, 0)
    LAWN_GREEN = Color(124, 252, 0)
    CHARTREUSE = Color(127, 255, 0)
    GREEN_YELLOW = Color(173, 255, 47)
    SPRING_GREEN = Color(0, 255, 127)
    MEDIUM_SPRING_GREEN = Color(0, 250, 154)
    LIGHT_GREEN = Color(144, 238, 144)
    PALE_GREEN = Color(152, 251, 152)
    DARK_SEA_GREEN = Color(143, 188, 143)
    MEDIUM_AQUAMARINE = Color(102, 205, 170)
    MEDIUM_SEA_GREEN = Color(60, 179, 113)
    SEA_GREEN = Color(46, 139, 87)
    FOREST_GREEN = Color(34, 139, 34)
    GREEN = Color(0, 128, 0)
    DARK_GREEN = Color(0, 100, 0)
    AQUA = Color(0, 255, 255)
    CYAN = Color(0, 255, 255)
    LIGHT_CYAN = Color(224, 255, 255)
    PALE_TURQUOISE = Color(175, 238, 238)
    AQUAMARINE = Color(127, 255, 212)
    TURQUOISE = Color(64, 224, 208)
    MEDIUM_TURQUOISE = Color(72, 209, 204)
    DARK_TURQUOISE = Color(0, 206, 209)
    LIGHT_SEA_GREEN = Color(32, 178, 170)
    CADET_BLUE = Color(95, 158, 160)
    DARK_CYAN = Color(0, 139, 139)
    TEAL = Color(0, 128, 128)
    LIGHT_STEEL_BLUE = Color(176, 196, 222)
    POWDER_BLUE = Color(176, 224, 230)
    LIGHT_BLUE = Color(173, 216, 230)
    SKY_BLUE = Color(135, 206, 235)
    LIGHT_SKY_BLUE = Color(135, 206, 250)
    DEEP_SKY_BLUE = Color(0, 191, 255)
    DODGER_BLUE = Color(30, 144, 255)
    CORNFLOWER_BLUE = Color(100, 149, 237)
    STEEL_BLUE = Color(70, 130, 180)
    ROYAL_BLUE = Color(65, 105, 225)
    BLUE = Color(0, 0, 255)
    MEDIUM_BLUE = Color(0, 0, 205)
    DARK_BLUE = Color(0, 0, 139)
    NAVY = Color(0, 0, 128)
    MIDNIGHT_BLUE = Color(25, 25, 112)
    LAVENDER = Color(230, 230, 250)
    THISTLE = Color(216, 191, 216)
    PLUM = Color(221, 160, 221)
    VIOLET = Color(238, 130, 238)
    ORCHID = Color(218, 112, 214)
    FUCHSIA = Color(255, 0, 255)
    MAGENTA = Color(255, 0, 255)
    MEDIUM_ORCHID = Color(186, 85, 211)
    MEDIUM_PURPLE = Color(147, 112, 219)
    BLUE_VIOLET = Color(138, 43, 226)
    DARK_VIOLET = Color(148, 0, 211)
    DARK_ORCHID = Color(153, 50, 204)
    DARK_MAGENTA = Color(139, 0, 139)
    PURPLE = Color(128, 0, 128)
    INDIGO = Color(75, 0, 130)
    DARK_SLATE_BLUE = Color(72, 61, 139)
    SLATE_BLUE = Color(106, 90, 205)
    MEDIUM_SLATE_BLUE = Color(123, 104, 238)
    WHITE = Color(255, 255, 255)
    SNOW = Color(255, 250, 250)
    HONEYDEW = Color(240, 255, 240)
    MINT_CREAM = Color(245, 255, 250)
    AZURE = Color(240, 255, 255)
    ALICE_BLUE = Color(240, 248, 255)
    GHOST_WHITE = Color(248, 248, 255)
    WHITE_SMOKE = Color(245, 245, 245)
    SEASHELL = Color(255, 245, 238)
    BEIGE = Color(245, 245, 220)
    OLD_LACE = Color(253, 245, 230)
    FLORAL_WHITE = Color(255, 250, 240)
    IVORY = Color(255, 255, 240)
    ANTIQUE_WHITE = Color(250, 235, 215)
    LINEN = Color(250, 240, 230)
    LAVENDER_BLUSH = Color(255, 240, 245)
    MISTY_ROSE = Color(255, 228, 225)
    GAINSBORO = Color(220, 220, 220)
    LIGHT_GRAY = Color(211, 211, 211)
    SILVER = Color(192, 192, 192)
    DARK_GRAY = Color(169, 169, 169)
    GRAY = Color(128, 128, 128)
    DIM_GRAY = Color(105, 105, 105)
    LIGHT_SLATE_GRAY = Color(119, 136, 153)
    SLATE_GRAY = Color(112, 128, 144)
    DARK_SLATE_GRAY = Color(47, 79, 79)

def solid_state(color, duration=0):
    """Solid Color Led

    Configuration: "id|mode|color|duration"

    :type duration: Time in msec; 0 = forever
    :type color: Color obj
    :return: command string and module ID
    """
    command = "0|{}|{}".format(color, duration)
    return command, _name_id


def rainbow(interval, repetitions=0):
    """Rainbow LED modus

    Configuration: "id|mode|repetitions|interval"

    :type repetitions: amount of times the rainbow needs to repeat; 0 = forever
    :type duration: time between two colors in msecs
    :return: command string and module ID
    """
    command = "1|{}|{}".format(repetitions, interval)
    return command, _name_id


def blink(interval_1, color_1, interval_2, color_2, repetitions=0):
    """Blinking mode

    Blink between two configured colors
    Configuration: "id|mode|repetitions|interval_1|color_1|interval_2|color_2"

    :param interval_1: time in msecs color 1 stays on
    :param color_1: Color object
    :param interval_2: time in msecs color 2 stays on
    :param color_2: Color object
    :param repetitions: amount of times the blinking needs to happen; 0 = forever
    :return: command string and module ID
    """
    command = "2|{}|{}|{}|{}|{}".format(interval_1, color_1, interval_2, color_2)


class _LedPattern:
    def __init__(self, pattern, interval_duration, max_bits):
        """

        :type max_bits: maximum number of bits for the provided pattern
        :param pattern: String representing bits; 1 = vibrate; 0 = no-vibrate
        :param interval_duration: amount of milliseconds between vibration bits in the pattern
        """
        self._pattern = ""
        self._max_bits = int(max_bits)
        self.pattern = str(pattern)
        self.pattern_size = len(self._pattern)
        self.interval_duration = interval_duration

    @property
    def pattern(self):
        """Retrieve the pattern as a uint value

        :return: 32 bit unsigned integer
        """
        if self._pattern == "":
            raise InvalidPatternException("No pattern set.")
        bitstring_as_int = bitstring.BitArray(bin=self._pattern)
        return bitstring_as_int.uint

    @pattern.setter
    def pattern(self, value):
        value = str(value)
        allowed_chars = set('01')
        if len(value) < 1 or len(value) > self._max_bits or not set(value).issubset(allowed_chars):
            raise InvalidPatternException("Pattern is not a valid one, must contain at least 1 bit, maximum {} bits "
                                          "and string can only contain a maximum of 32 elements | [{}]"
                                          .format(self._max_bits, value))
        self._pattern = value


def single_color_pattern(color, pattern, interval = 100, repetitions = 0):
    """Pattern mode with only a single color

    Configuration: "id|mode|repetitions|pattern|pattern_size|interval|color"

    :param color: Color object
    :param pattern: string of bits (read left to right); maximum of 31 bits allowed
    :param interval: time in msecs between two bits in the pattern
    :param repetitions: amount of times the pattern repeats; 0 = forever
    :return: command string and module ID
    """
    pattern_obj = _LedPattern(pattern, interval, 31)
    command = "3|{}|{}|{}|{}|{}".format(repetitions, pattern_obj.pattern, pattern_obj.pattern_size, interval, color)
    return command, _name_id


def multi_color_pattern(colors, pattern, interval = 100, repetitions = 0):
    """Pattern mode with multiple colors

    Configuration: "id|mode|repetitions|pattern|pattern_size|interval|color"

    :type colors: list of color objects; maximum of 8 colors allowed
    :param pattern: string of bits (read left to right); maximum of 8 bits; bits must match amount of colors
    :param interval: time in msecs between two bits in the pattern
    :param repetitions: amount of times the pattern repeats; 0 = forever
    :return: command string and module ID
    """
    try:
        if len(colors) < 1:
            raise InvalidMultiColorConfigurationException("You need to supply at least 1 color in the list of colors")

        pattern_obj = _LedPattern(pattern, interval, max(8, len(colors)))
        command = "4|{}|{}|{}|{}|".format(repetitions, pattern_obj.pattern, pattern_obj.pattern_size, interval)
        color_string = "|".join(colors[0:pattern_obj.pattern_size])

        return "{}{}".format(command, color_string), _name_id
    except TypeError:
        raise InvalidMultiColorConfigurationException("Couldn't understand color configuration, was a list given?")


def fade(color_1, ontime_1, interval_a, color_2, ontime_2, interval_b, color_3, ontime_3, repetitions = 0):
    """Fade mode

    Fade between 3 given colors
    Configuration: "id|mode|repetitions|color_1|ontime_1|interval_a|color_2|ontime_2|interval_b|color_3|ontime_3"

    :param color_1: color object
    :param ontime_1: time in msecs that color_1 should be on
    :param interval_a: time in msecs between color_1 and color_2 transition
    :param color_2: color object
    :param ontime_2: time in msecs that color_2 should be on
    :param interval_b: time in msecs between color_ and color_3 transition
    :param color_3: color object
    :param ontime_3: time in msecs that color_3 should be on
    :param repetitions: amount of times the fade repeats; 0 = forever
    :return: command string and module ID
    """
    command = "5|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(repetitions, color_1, ontime_1, interval_a, color_2, ontime_2,
                                                    interval_b, color_3, ontime_3)
    return command, _name_id
