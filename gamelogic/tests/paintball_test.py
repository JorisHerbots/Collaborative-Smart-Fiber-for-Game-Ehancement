import gamelogic.paintball_enhance.paintball_enhance as paintball
import pytest
import time


def test_players_registration():
    assert paintball.engine.event_triggers["on_entity_registered"][0] == paintball.on_entity_registered
    paintball.engine.initiate_event("on_entity_registered", {"entity": {"ipv4_address": 0}})
    paintball.engine.initiate_event("on_entity_registered", {"entity": {"ipv4_address": 1}})
    time.sleep(1)
    assert(paintball.team1.size() == 1)
    assert(paintball.team2.size() == 1)
