import gamelogic.paintball_enhance.paintball_enhance as paintball
from engine.entitymanager import Entity
import pytest
import time


def test_players_registration():
    assert paintball.engine.event_triggers["entity_registered"][0] == paintball.entity_registered
    first = Entity(0, "0|0\n1|1\n2|2")
    second = Entity(1, "0|0\n1|1\n2|2")
    paintball.engine.initiate_event("entity_registered", {"entity": first})
    paintball.engine.initiate_event("entity_registered", {"entity": second})
    time.sleep(1)
    assert(paintball.team1.size() == 1)
    assert(paintball.team2.size() == 1)

def test_team_communication():
    paintball.reset()
    assert paintball.engine.event_triggers["entity_registered"][0] == paintball.entity_registered
    first = Entity(0, "0|0\n1|1\n2|2")
    second = Entity(1, "0|0\n1|1\n2|2")
    third = Entity(2, "0|0\n1|1\n2|2")
    fourth = Entity(3, "0|0\n1|1\n2|2")
    paintball.engine.initiate_event("entity_registered", {"entity": first})
    paintball.engine.initiate_event("entity_registered", {"entity": second})
    paintball.engine.initiate_event("entity_registered", {"entity": third})
    paintball.engine.initiate_event("entity_registered", {"entity": fourth})
    time.sleep(1)
    assert(paintball.team1.size() == 2)
    assert(paintball.team2.size() == 2)
    paintball.engine.initiate_event("button_pressed", {"button": 0, "entity": first})
    paintball.engine.initiate_event("button_pressed", {"button": 0, "entity": third})
    time.sleep(1)
    for player in paintball.team1.players:
        assert len(player.entity.pop_all_command()) == 1
