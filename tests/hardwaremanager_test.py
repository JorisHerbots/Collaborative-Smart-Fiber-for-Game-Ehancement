from engine import hardwaremanager
from engine.hardware import led,three_button,vibration_motor

def test_harware_parser_dict_name():
    hwm = hardwaremanager.HardwareManager()
    assert led._name in hwm.hardware_configuration_parsers
    assert three_button._name in hwm.hardware_configuration_parsers
    assert vibration_motor._name in hwm.hardware_configuration_parsers

def test_harware_parser_dict_method_pointer():
    hwm = hardwaremanager.HardwareManager()
    assert hwm.hardware_configuration_parsers[led._name] == led.parse_config
    assert hwm.hardware_configuration_parsers[three_button._name] == three_button.parse_config
    assert hwm.hardware_configuration_parsers[vibration_motor._name] == vibration_motor.parse_config
