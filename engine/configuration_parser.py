from threading import Thread
import queue
from .logger import initiate_logger
from . import config


_logger = initiate_logger(__name__, config.debug)
_halt_event = "STOP_CONFIGURATION_PARSER_PROCESS"


class ConfigurationParser:
    def __init__(self):
        # FIFO queue holding all JSON configurations that need parsing and processing
        self.configuration_queue = queue.Queue()

    def process_queue(self, hardware_interface, event_queue):
        global _logger, _halt_event
        """Infinitely processing queue

        To halt the process a special type of queue message needs to be inserted, in following format:
            "STOP_CONFIGURATION_PARSER_PROCESS"

        It's advised to run this in a separate thread
            The queue itself is by default thread safe (see queue library)
        """
        _logger.info("Configuration parser queue processor initialised.")
        while True:
            queue_item = self.configuration_queue.get()
            _logger.info("New configuration found on queue, processing now...")
            _logger.debug("Queue item info | {}".format(queue_item))

            if str(queue_item) == _halt_event:
                _logger.info("Process queue configuration parser received a halt request, halting queue processing.")
                break

            try:
                events = hardware_interface.find_events(queue_item.get("entity"), queue_item.get("payload"))
                _logger.debug("Hardware interface returned event list. | Raw payload [{}] | Event data [{}]"
                              .format(queue_item.get("payload"), events))
                [event_queue.put({"event_name": event.get("name"),
                                  "event_args": event.get("args")}) for event in events]
            except Exception as e:
                _logger.warning("Couldn't parse a configuration from a client. | {}".format(e))


def setup_configuration_parser(hardware_interface, event_queue):
    """Setup a configuration parser object

    Process runs in another thread, see process_queue() for more info
    :param event_queue: Queue where all events need to be gathered for later execution by the engine core
    :type hardware_interface: Harware interface for passing through queue items
    """
    cp = ConfigurationParser()
    Thread(target=cp.process_queue, kwargs={"hardware_interface": hardware_interface,
                                            "event_queue": event_queue}).start()
    return cp


def stop_queue_processing(configuration_parser):
    configuration_parser.configuration_queue.put(_halt_event)
