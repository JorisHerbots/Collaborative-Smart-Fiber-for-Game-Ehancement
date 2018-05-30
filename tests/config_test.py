from engine import Engine


def test_config_available():
    engine = Engine("config tester", port=8090, _test_setup=True)
    assert engine.config.config_test_available == True