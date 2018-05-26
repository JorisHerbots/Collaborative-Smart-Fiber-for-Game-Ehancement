from engine import configuration_parser
from threading import Thread
from time import sleep


def test_configuration_parser_processes_queue():
    cp = configuration_parser.ConfigurationParser()
    assert cp.configuration_queue.empty() == True
    cp.configuration_queue.put("~Test Item~")
    assert cp.configuration_queue.empty() == False

    Thread(target=cp.process_queue, kwargs={"hardware_interface": None, "event_queue": None}).start()
    sleep(1)
    assert cp.configuration_queue.empty() == True
    configuration_parser.stop_queue_processing(cp)
    sleep(1)
    assert cp.configuration_queue.empty() == True

