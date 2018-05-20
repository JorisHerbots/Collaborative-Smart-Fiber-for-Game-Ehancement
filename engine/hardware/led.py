from enum import Enum

_name = "Led"
_name_id = 1


class State(Enum):
    OFF = 0
    ON = 1
    FLASHING = 2


def parse_config(raw_config):
    pass


def set_state(state, duration):
    """Set LED state helper

    :param state: desired state
    :param duration: in case a flashing state was selected, the duration species how long the led flashes
    :return: json configuration for the desired state
    """
    pass