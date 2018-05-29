from engine import Engine
from engine.instance import InvalidTriggerException
import pytest


def test_empty_trigger():
    engine = Engine("test", _test_setup=True)
    assert engine.event_triggers == {}


def empty_method():
    pass


def test_simple_triger_mapping():
    engine = Engine("test", port=8091,  _test_setup=True)
    engine.add_trigger("demo_event", empty_method)
    engine.add_trigger("demo_event", None)
    assert engine.event_triggers["demo_event"][0] == empty_method
    assert None in engine.event_triggers["demo_event"]


def test_event_names():
    engine = Engine("test", port=8092,  _test_setup=True)
    engine.add_trigger("lowercase_event", None)
    engine.add_trigger("CAPS_EVENT", None)
    assert "lowercase_event" in engine.event_triggers
    assert "caps_event" in engine.event_triggers


def test_trigger_mapping_with_decorator():
    engine = Engine("test", port=8093,  _test_setup=True)

    @engine.register_trigger("event_1")
    def trigger1():
        pass

    @engine.register_trigger("event_2")
    def trigger2():
        pass

    @engine.register_trigger("event_1")
    def trigger3():
        pass

    assert "event_1" in engine.event_triggers
    assert "event_2" in engine.event_triggers

    assert trigger1 in engine.event_triggers["event_1"]
    assert trigger3 in engine.event_triggers["event_1"]
    assert trigger2 in engine.event_triggers["event_2"]


def test_triggers():
    engine = Engine("test", port=8094,  _test_setup=True)

    @engine.register_trigger("demo_event")
    def trigger(a,b,c):
        assert a is None
        assert b is None
        assert c is None

    engine.initiate_event("demo_event", {"a": None, "b": None, "c": None})

    # Removed
    # with pytest.raises(InvalidTriggerException):
    #     engine.initiate_event("demo_event", {})