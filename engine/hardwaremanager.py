from .hardware import led, three_button, vibration_motor
from .logger import initiate_logger
from . import config


_logger = initiate_logger(__name__, config.debug)


class HardwareMethodNotImplementedException(Exception):
    pass


class HardwareManager:
    def __init__(self):
        # Hardware components
        self.hardware_list = [led, three_button, vibration_motor]

        # Hardware configuration parsers
        self.hardware_configuration_parsers = {}
        for component in self.hardware_list:
            try:
                self.hardware_configuration_parsers[component._name_id] = component.parse_config
            except NameError:
                raise HardwareMethodNotImplementedException("{} does not contain a _name variable and/or parse_config "
                                                            "method".format_map(str(component)))

    def find_events(self, json_config):
        """Walk through a JSON configuration and find all possible events

        Every single hardware component module contains a parser_config() method
                parser_config() is the hardcoded logic that will look for certain types of configurations and extract
                whether or not an event has happened.

        Event names
                At this point in time, no control system is in place to check for correct event names.
                As a good practise, all events should be documented.

        :param json_config:
        :return: dictionary of all found events
        """
        if json_config is None:
            return {}

        # for component_config in json_config:
        #     if component_config.get("name") is not None and component_config["name"] in self.hardware_list:
        #         self.hardware_list[component_config["name"]](component_config)
        #     else:
        #         _logger.warning("Fault component configuration found during parsing. (Name missing or wrong?) | {}"
        #                         .format(component_config))


def create_lookup_list(*components):
    """Create a list from all component modules

    Universal way of creating a lookup table for components
        In case module namings change, this list creator assures compatibility
    :param components: argument list of python modules (from hardware)
    :return: list of all component names
    """
    return [str(component._name_id) for component in components]