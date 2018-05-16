from .hardwaremanager import HardwareManager
from . import config


class InvalidTriggerException(Exception):
    pass

class Engine:
    def __init__(self, game_name="Unknown"):
        # Game Name this Engine represents
        self.game_name = game_name

        # Configuration parameters
        self.config = config

        # Dictionary of all triggers that correspond to a given event
        self.event_triggers = {}

        # Hardware manager instance
        self.hardware_interface = HardwareManager()

    def add_trigger(self, event_name, trigger_pointer):
        """Add a trigger to a given event name

        Decorator functionality event_trigger() available

        :param event_name: all event names should ideally be strings, if not they'll be converted to strings
        :param trigger_pointer: method call for the trigger
        """
        event_name = str(event_name).lower()
        if event_name not in self.event_triggers:
            self.event_triggers[event_name] = []

        if trigger_pointer not in self.event_triggers[event_name]:
            self.event_triggers[event_name].append(trigger_pointer)

    def register_trigger(self, event_name):
        """A decorator used to add a method as an event trigger

        :param event_name: the event name, see add_event_trigger() for more information
        """

        def decorator(f):
            self.add_trigger(event_name, f)
            return f

        return decorator

    def initiate_event(self, event_name, event_args):
        event_name = str(event_name).lower()
        if event_name not in self.event_triggers:
            return

        triggers = self.event_triggers[event_name]
        for trigger in triggers:
            try:
                trigger(**event_args)
            except TypeError:
                # TODO logging
                raise InvalidTriggerException("{} does not accept the given arguments {} for event \"{}\"".format(trigger, event_args, event_name))
