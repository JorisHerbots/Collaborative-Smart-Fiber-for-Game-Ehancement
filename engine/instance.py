from .hardwaremanager import HardwareManager
from . import config, logger


class InvalidTriggerException(Exception):
    pass

class Engine:
    def __init__(self, game_name="Unknown"):
        # Game Name this Engine represents
        self.game_name = str(game_name)

        # Configuration parameters
        self.config = config

        # Logger
        self.logger = logger.initiate_logger("engine.instance", self.config.debug)

        # Dictionary of all triggers that correspond to a given event
        self.event_triggers = {}

        # Hardware manager instance
        self.hardware_interface = HardwareManager()

        self.logger.info("Engine initialised | Game name: \"{}\"".format(str(game_name)))

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
            self.logger.info("Trigger [{}] initialised added for event [{}]".format(trigger_pointer, event_name))

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
                self.logger.debug("Initiating trigger [{}] for event [{}] with parameters [{}]".format(trigger, event_name, event_args))
                trigger(**event_args)
            except TypeError:
                self.logger.error("Could not call trigger {}".format(trigger))
                raise InvalidTriggerException("{} does not accept the given arguments {} for event \"{}\"".format(trigger, event_args, event_name))
