from engine.hardware import led


def test_color_strings():
    c1 = led.Color(1, 2, 3)
    assert str(c1) == "1,2,3"
