from .hardwaremanager import HardwareManager
from .entitymanager import EntityManager
from . import config, logger, httpserver, configuration_parser
from queue import Queue
from threading import Thread
from enum import Enum
import time


class InvalidTriggerException(Exception):
    pass


class Engine:
    class EngineState(Enum):
        REGISTER_PHASE = 0
        RUNNING_PHASE = 1
        END_PHASE = 2

    def __init__(self, game_name="Unknown", host="127.0.0.1", port=8080, _test_setup = False):
        # Phase the engine is currently in
        self.phase = self.EngineState.REGISTER_PHASE

        # Game Name this Engine represents
        self.game_name = str(game_name)

        # Configuration parameters
        self.config = config

        # Logger
        self.logger = logger.initiate_logger("Engine", self.config.debug)

        # Dictionary of all triggers that correspond to a given event
        self.event_triggers = {}

        # Queue of events that need to be handled
        self.event_queue = Queue()

        # Hardware manager instance
        self.hardware_interface = HardwareManager()

        # Entity manager instance
        self.entitymanager_interface = EntityManager()

        # Configuration parser instance
        self.configuration_parser_instance = configuration_parser.setup_configuration_parser(self.hardware_interface,
                                                                                             self.event_queue)

        # HTTP server instance
        self.http_server_instance = httpserver.run_server(self.configuration_parser_instance.configuration_queue,
                                                          self.entitymanager_interface,
                                                          self._start_game, self._is_game_running,
                                                          self.initiate_event, host, port)
        # TODO PARAMS HERE (Given @ boot??)

        self.logger.info("Engine initialised | Game name: \"{}\"".format(str(game_name)))

        # Event processor
        Thread(target=self._process_events).start()

        # Only do an immediate shutdown of all interfaces when in a test_setup is run
        if _test_setup:
            self.end_game()

    def _cleanup_interfaces(self):
        self.logger.info("Cleaning up Engine interfaces running on separate threads.")
        httpserver.stop_server(self.http_server_instance)
        configuration_parser.stop_queue_processing(self.configuration_parser_instance)
        self.event_queue.put("STOP_EVENT_QUEUE")

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
            self.logger.info("Trigger [{}] initialised for event [{}]".format(trigger_pointer, event_name))

    def register_trigger(self, event_name):
        """A decorator used to add a method as an event trigger

        :param event_name: the event name, see add_event_trigger() for more information
        """

        def decorator(f):
            self.add_trigger(event_name, f)
            return f

        return decorator

    def initiate_event(self, event_name, event_args):
        """Initiate an event

        Event will be handled in separate thread. No guarantees it will be executed immediately after this call.

        :param event_name: string event name, has to be know by the system, will raise exception else
        :param event_args: args of the event call (see method definition of the corresponding pointer)
        """
        self.event_queue.put_nowait({"event_name": event_name, "event_args": event_args})

    def _process_events(self):
        """Event processor
        Should be called in a separate thread

        """
        while True:
            event = self.event_queue.get()
            if event == "STOP_EVENT_QUEUE":
                self.logger.debug("Event processor received HALT request, halting now.")
                return

            event_name = str(event.get("event_name")).lower()
            event_args = event.get("event_args")
            self.logger.debug("New event found | Name [{}] | Args [{}]".format(event_name, event_args))

            if event_name not in self.event_triggers:
                continue

            triggers = self.event_triggers[event_name]
            for trigger in triggers:
                try:
                    self.logger.debug("Initiating trigger [{}] for event [{}] with parameters [{}]"
                                      .format(trigger, event_name, event_args))
                    trigger(**event_args)
                except TypeError:
                    self.logger.error("{} does not accept the given arguments {} for event \"{}\""
                                      .format(trigger, event_args, event_name))

    def _is_game_running(self):
        """Way for interfaces to retrieve game state info

        Note: Only used by server due to weird way HTTPServer works with its handlers
        TODO: Find better way for sharing this information

        :return: boolean
        """
        return self.phase == self.EngineState.RUNNING_PHASE

    def _start_game(self):
        """Set the engine into running phase

        Signal certain interfaces they can advance in their processing
        """
        self.phase = self.EngineState.RUNNING_PHASE
        self.initiate_event("game_started", {})

    def end_game(self):
        """Signal halt to Engine

        All interfaces will stop working upon issuing this request
        """
        self.phase = self.EngineState.END_PHASE
        self._cleanup_interfaces()
