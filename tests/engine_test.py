from engine import Engine


def test_empty_trigger():
    engine = Engine("test")
    assert engine.event_triggers == {}


def empty_method():
    pass


def test_simple_triger_mapping():
    engine = Engine("test")
    engine.add_event_trigger("demo_event", empty_method)
    engine.add_event_trigger("demo_event", None)
    assert engine.event_triggers["demo_event"][0] == empty_method
    assert None in engine.event_triggers["demo_event"]


def test_event_names():
    engine = Engine("test")
    engine.add_event_trigger("lowercase_event", None)
    engine.add_event_trigger("CAPS_EVENT", None)
    assert "lowercase_event" in engine.event_triggers
    assert "caps_event" in engine.event_triggers


def test_trigger_mapping_with_decorator():
    engine = Engine("test")

    @engine.event_trigger("event_1")
    def trigger1():
        pass

    @engine.event_trigger("event_2")
    def trigger2():
        pass

    @engine.event_trigger("event_1")
    def trigger3():
        pass

    assert "event_1" in engine.event_triggers
    assert "event_2" in engine.event_triggers

    assert trigger1 in engine.event_triggers["event_1"]
    assert trigger3 in engine.event_triggers["event_1"]
    assert trigger2 in engine.event_triggers["event_2"]