from threading import Thread
import queue
from .logger import initiate_logger
from . import config


_logger = initiate_logger(__name__, config.debug)
_halt_event = "STOP_CONFIGURATION_PARSER_PROCESS"


class ConfigurationParser:
    def __init__(self):
        # FIFO queue holding all configurations that need parsing and processing
        self.configuration_queue = queue.Queue()

    def process_queue(self):
        global _logger, _halt_event
        """Infinitely processing queue

        To halt the process a special type of queue message needs to be inserted, in following format:
            "STOP_CONFIGURATION_PARSER_PROCESS"

        It's advised to run this in a seperate thread
            The queue itself is by default thread safe (see queue library)
        """
        _logger.info("Configuration parser queue processor initialised.")
        while True:
            queue_item = self.configuration_queue.get()
            _logger.info("New configuration found on queue, processing now...")
            _logger.debug("Queue item info | {}".format(queue_item))

            if str(queue_item) is _halt_event:
                _logger.info("Process queue configuration parser received a halt request, halting queue processing.")
                break


def setup_configuration_parser():
    cp = ConfigurationParser()
    Thread(target=cp.process_queue).start()
    return cp


def stop_queue_processing(configuration_parser):
    configuration_parser.configuration_queue.put(_halt_event)
