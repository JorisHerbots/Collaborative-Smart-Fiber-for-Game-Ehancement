class HardwareMethodNotImplementedException(Exception):
    pass


class HardwareInstance:
    def parse_config(self, json_config):
        raise HardwareMethodNotImplementedException("parse_config method has not been implemented yet")