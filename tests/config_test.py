from engine import Engine


def test_config_available():
    engine = Engine("config tester")
    assert engine.config.config_test_available == True