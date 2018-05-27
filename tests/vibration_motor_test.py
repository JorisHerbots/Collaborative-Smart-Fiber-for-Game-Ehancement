from engine.hardware import vibration_motor


def test_binary_to_int():
    test_8bit = vibration_motor.VibrationPattern("11111111")
    test_32bit = vibration_motor.VibrationPattern("11111111111111111111111111111111")
    assert test_8bit.pattern == 255
    assert test_32bit.pattern == 4294967295


def test_command_string():
    command, _ = vibration_motor.vibrate(vibration_motor.VibrationPattern("101", 150))
    assert command == "0|1|5|3|150"
