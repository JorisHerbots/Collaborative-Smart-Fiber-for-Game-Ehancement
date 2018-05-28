from enum import Enum
from ..logger import initiate_logger
from .. import config


_logger = initiate_logger(__name__, config.debug)


_name = "three_button"
_name_id = 0


class ButtonId(Enum):
    BUTTON0 = "0"
    BUTTON1 = "1"
    BUTTON2 = "2"


def create_event_dictionary(event_name, args):
    return {"name": event_name, "args": args}


def parse_config(split_config):
    """Three Button Module

    Configuration: "id|module|button_id|state|type|duration|timestamp"
        0: id
        1: module
        2: button_id (button identifiers start from 0)
        3: state 0 = off; 1 = on
        4: type 0 = rising (off -> on); 1 = falling (on -> off)
        5: duration Rising mode implies the time the button was off; Falling mode implies the time the button was held
        6: time since sync with all modules

    Following events can be generated:
        button_pressed
        button_released

    :param split_config:
    :return: list of dictionaries containing events and args (if present)
    """

    _logger.debug("Three Button module parsere initiated | #items = {} | Config {}"
                  .format(len(split_config), split_config))

    if len(split_config) != 7:
        return []

    event_list = []
    if split_config[4] == "0":
        event_list.append(create_event_dictionary("button_pressed", {"button": ButtonId(split_config[2])}))
    elif split_config[4] == "1":
        event_list.append(create_event_dictionary("button_released", {"button": ButtonId(split_config[2]),
                                                                      "duration": int(split_config[5])}))

    return event_list

