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

def test_team_communication():
    assert paintball.engine.event_triggers["on_entity_registered"][0] == paintball.on_entity_registered
    paintball.engine.initiate_event("on_entity_registered", {"entity": {"ipv4_address": 0}})
    paintball.engine.initiate_event("on_entity_registered", {"entity": {"ipv4_address": 1}})
    paintball.engine.initiate_event("on_entity_registered", {"entity": {"ipv4_address": 2}})
    paintball.engine.initiate_event("on_entity_registered", {"entity": {"ipv4_address": 3}})
    time.sleep(1)
    assert(paintball.team1.size() == 2)
    assert(paintball.team2.size() == 2)
    paintball.engine.initiate_event("button_pressed", {"button": 0, "entity": {"ipv4_address": 0}})
    paintball.engine.initiate_event("button_pressed", {"button": 0, "entity": {"ipv4_address": 2}})
    time.sleep(1)
    for player in paintball.team1.players:
        assert len(player.entity.pop_all_command()) == 1
