from engine import Engine


def test_config_available():
    engine = Engine("config tester", test_setup=True)
    assert engine.config.config_test_available == True