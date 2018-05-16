import logging
import sys


engine_default_logging_handler = logging.StreamHandler(sys.stdout)
engine_default_logging_handler.setFormatter(logging.Formatter(
    '[%(asctime)s | %(levelname)s] %(message)s'
))


def initiate_logger(logger_name, debug=False):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    logger.addHandler(engine_default_logging_handler)
    return logger
