import gamelogic.policethiefgame.policethiefgame as game
import pytest

def test_players_registration():
    assert game.engine.event_triggers["on_entity_registered"][0] == game.on_entity_registered
    game.engine.initiate_event("on_entity_registered", {"id": 0})
    game.engine.initiate_event("on_entity_registered", {"id": 1})
    assert len(game.players) == 2
    assert game.players[0].type != game.players[1].type

