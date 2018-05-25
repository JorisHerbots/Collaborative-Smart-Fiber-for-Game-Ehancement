from engine import hardwaremanager
from engine.hardware import led,three_button,vibration_motor

def test_harware_parser_dict_name():
    hwm = hardwaremanager.HardwareManager()
    assert str(led._name_id) in hwm.hardware_configuration_parsers
    assert str(three_button._name_id) in hwm.hardware_configuration_parsers
    assert str(vibration_motor._name_id) in hwm.hardware_configuration_parsers

def test_harware_parser_dict_method_pointer():
    hwm = hardwaremanager.HardwareManager()
    assert hwm.hardware_configuration_parsers[str(led._name_id)] == led.parse_config
    assert hwm.hardware_configuration_parsers[str(three_button._name_id)] == three_button.parse_config
    assert hwm.hardware_configuration_parsers[str(vibration_motor._name_id)] == vibration_motor.parse_config
