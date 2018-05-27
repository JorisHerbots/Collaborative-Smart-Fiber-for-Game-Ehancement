from engine import Engine


def test_config_available():
    engine = Engine("config tester", _test_setup=True)
    assert engine.config.config_test_available == True