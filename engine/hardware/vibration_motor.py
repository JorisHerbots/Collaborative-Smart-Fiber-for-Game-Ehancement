import bitstring
from enum import Enum


_name = "vibration_motor"
_name_id = 2


def parse_config(split_config):
    # Filler, vibration doesn't send us updates
    pass


class InvalidPatternException(Exception):
    pass


class VibrationPattern:
    def __init__(self, pattern, interval_duration=100):
        """

        :param pattern: String representing bits; 1 = vibrate; 0 = no-vibrate
        :param interval_duration: amount of milliseconds between vibration bits in the pattern
        """
        self._pattern = ""
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
        if len(value) < 1 or len(value) > 32 or not set(value).issubset(allowed_chars):
            raise InvalidPatternException("Pattern is not a valid one, must contain at least 1 bit, maximum 32 bits "
                                          "and string can only contain a maximum of 32 elements | [{}]".format(value))
        self._pattern = value


class PremadeVibrationPatterns(Enum):
    SHORT_BLIP = VibrationPattern("1", 300)
    LONG_BLIP = VibrationPattern("1", 1500)
    TWO_SHORT_BLIPS = VibrationPattern("101", 300)
    TWO_LONG_BLIPS = VibrationPattern("11011", 300)
    THREE_SHORT_BLIPS = VibrationPattern("10101", 300)
    THREE_LONG_BLIPS = VibrationPattern("11011011", 300)

    SOS = VibrationPattern("10101011101110111010101", 75)
    GO_GO_POWER_RANGERS = VibrationPattern("111111001100110100110011", 75)


def vibrate(vibration_config, repetitions=1):
    """Create a vibrate command based on the given VibrationPattern object

    Command syntax: "id|mode|repetitions|pattern|pattern_size|interval"
        Note: id is not set by module but by entity, we have no business with it
    :param vibration_config: VibrationPattern object
    :param repetitions: amount of times the pattern needs to play; 0 = infinite
        (WARNING: Might block entity from future actions due to hardware limitations, use with caution)
    :return: command string and module ID
    """
    command = "{}|{}|{}|{}|{}".format(0, repetitions, vibration_config.pattern, vibration_config.pattern_size,
                                      vibration_config.interval_duration)
    return command, _name_id
