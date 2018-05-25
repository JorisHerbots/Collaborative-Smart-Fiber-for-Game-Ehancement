from .hardware import led, three_button, vibration_motor
from .logger import initiate_logger
from . import config, entitymanager


_logger = initiate_logger(__name__, config.debug)


class HardwareMethodNotImplementedException(Exception):
    pass


class HardwareComponentUnknownYetExisting(Exception):
    pass


class HardwareManager:
    def __init__(self):
        # Hardware components
        self.hardware_list = [led, three_button, vibration_motor]

        # Hardware configuration parsers
        self.hardware_configuration_parsers = {}
        for component in self.hardware_list:
            try:
                self.hardware_configuration_parsers[str(component._name_id)] = component.parse_config
            except NameError:
                raise HardwareMethodNotImplementedException("{} does not contain a _name variable and/or parse_config "
                                                            "method".format_map(str(component)))

    def find_events(self, entity, payload):
        """Walk through a client configuration and find all possible events

        Every single hardware component module contains a parser_config() method
                parser_config() is the hardcoded logic that will look for certain types of configurations and extract
                whether or not an event has happened.

        Event names
                At this point in time, no control system is in place to check for correct event names.
                As a good practise, all events should be documented.

        :param json_config:
        :return: list of all found events(in the form of a dictionary: {event: name, args: argsdict})
        """
        if entity is None:
            _logger.error("HardwareManager has received an undefined entity as source. Should not be possible!! | "
                          "Entity [{}] | Payload [{}]".format(str(entity), str(payload)))
            return []
        if payload is None or payload == "":
            _logger.warning("HardwareManager has received an empty payload from source. | Entity [{}] | Payload [{}]"
                            .format(entity, payload))
            return []

        # Payload could contain multiple entries separated by a "\n"
        #split_payload = str(payload).split("\n")
        split_payload = str(payload).replace("\\n", "\n").splitlines()

        events = []
        for singular_payload in split_payload:
            _logger.debug("Processing raw singular payload data | [{}]".format(singular_payload))

            # All payload data is separated by pipes
            singular_payload_data = singular_payload.split("|")

            # Determine where this event originated from
            # Every entity has a list of unique ID's which are linked to a certain module
            # This unique ID is always assumed to be the first entry in a payload
            try:
                module_id = entity.get_module_id_from_unique_id(singular_payload_data[0])
                _logger.debug("Hardwaremanager was able to retrieve a module ID from a client payload unique ID | "
                              "Module ID [{}] | Unique ID [{}]".format(module_id, singular_payload_data[0]))

                if module_id not in self.hardware_configuration_parsers:
                    raise HardwareComponentUnknownYetExisting("Module ID \"{}\" not known to Hardware Manager, "
                                                              "yet found in an entity. | Hardware {}"
                                                              .format(module_id, self.hardware_configuration_parsers))
                module_event_data = self.hardware_configuration_parsers[module_id](singular_payload_data)
                for event in module_event_data:
                    if not event.get("args"):
                        continue
                    event["args"]["entity"] = entity
                try:
                    events.extend(module_event_data)
                except Exception:
                    _logger.error("Couldn't extend event list. Module most probably didn't return a list. | Module "
                                  "event data [{}]".format(module_event_data))

            except entitymanager.UniqueIdUnknownException:
                _logger.error("Entity issued a call with an unknown unique ID. Did hardware change? Did a new "
                              "component not register correctly? Ignoring payload. | Entity [{}] | Payload [{}]"
                              .format(entity, singular_payload_data))
        return events


def create_lookup_list(*components):
    """Create a list from all component modules

    Universal way of creating a lookup table for components
        In case module namings change, this list creator assures compatibility
    :param components: argument list of python modules (from hardware)
    :return: list of all component names
    """
    return [str(component._name_id) for component in components]
