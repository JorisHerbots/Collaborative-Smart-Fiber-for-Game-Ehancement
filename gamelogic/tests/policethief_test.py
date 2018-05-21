import gamelogic.policethiefgame.policethiefgame as game
from gamelogic.policethiefgame.models.playermodel import PlayerType, PlayerModel
import pytest


def test_players_registration():
    game.reset()
    assert game.engine.event_triggers["on_entity_registered"][0] == game.on_entity_registered
    game.engine.initiate_event("on_entity_registered", {"id": 0})
    game.engine.initiate_event("on_entity_registered", {"id": 1})
    assert len(game.players) == 2
    assert game.players[0].type != game.players[1].type

def test_team_switch():
    game.reset()
    game.engine.initiate_event("on_entity_registered", {"id": 0})
    game.engine.initiate_event("on_entity_registered", {"id": 1})
    game.engine.initiate_event("on_entity_registered", {"id": 2})

    assert game.players[0].type == PlayerType.THIEF
    assert game.players[1].type == PlayerType.POLICE
    assert game.players[2].type == PlayerType.THIEF

    game.engine.initiate_event("button_clicked", {"id": 0, "entity": {"id": 0}, "duration": 0})
    assert game.players[0].type == PlayerType.POLICE
    assert game.players[1].type == PlayerType.POLICE
    assert game.players[2].type == PlayerType.THIEF

    # Having no thiefs is not allowed
    game.engine.initiate_event("button_clicked", {"id": 0, "entity": {"id": 2}, "duration": 0})
    assert game.players[0].type == PlayerType.POLICE
    assert game.players[1].type == PlayerType.POLICE
    assert game.players[2].type == PlayerType.THIEF

    game.engine.initiate_event("button_clicked", {"id": 0, "entity": {"id": 1}, "duration": 0})
    assert game.players[0].type == PlayerType.POLICE
    assert game.players[1].type == PlayerType.THIEF
    assert game.players[2].type == PlayerType.THIEF

    game.engine.initiate_event("button_clicked", {"id": 0, "entity": {"id": 1}, "duration": 0})
    assert game.players[0].type == PlayerType.POLICE
    assert game.players[1].type == PlayerType.POLICE
    assert game.players[2].type == PlayerType.THIEF

def test_police_tapped():
    game.reset()
    game.engine.initiate_event("on_entity_registered", {"id": 0})
    game.engine.initiate_event("on_entity_registered", {"id": 1})
    game.engine.initiate_event("on_entity_registered", {"id": 2})

    assert game.players[1].type == PlayerType.POLICE
    game.engine.initiate_event("game_started", {})
    game.engine.initiate_event("button_clicked", {"id": 0, "entity": {"id": 1}, "duration": 0})
    assert game.players[1].type == PlayerType.POLICE
    assert game.gametimer.is_alive()
    game.gametimer.cancel()

def test_gameplay_thiefs_caught():
    game.reset()
    # Engine players registration phase
    game.engine.initiate_event("on_entity_registered", {"id": 0})
    game.engine.initiate_event("on_entity_registered", {"id": 1})
    game.engine.initiate_event("on_entity_registered", {"id": 2})
    assert game.activePhase == game.Phase.STARTPHASE

    # Players appointment phase
    game.engine.initiate_event("button_clicked", {"id": 0, "entity": {"id": 0}, "duration": 0})
    game.engine.initiate_event("button_clicked", {"id": 0, "entity": {"id": 1}, "duration": 0})
    assert game.players[0].type == PlayerType.POLICE
    assert game.players[1].type == PlayerType.THIEF
    assert game.players[2].type == PlayerType.THIEF

    # Start the game, timer should be active
    game.engine.initiate_event("game_started", {})
    assert game.gametimer.is_alive()
    assert game.activePhase == game.Phase.INGAMEPHASE
    assert game.players[0].type == PlayerType.POLICE
    assert game.players[1].type == PlayerType.THIEF
    assert game.players[2].type == PlayerType.THIEF

    game.engine.initiate_event("button_clicked", {"id": 0, "entity": {"id": 1}, "duration": 0})
    assert game.players[0].type == PlayerType.POLICE
    assert game.players[1].type == PlayerType.CAUGHT
    assert game.players[2].type == PlayerType.THIEF
    game.engine.initiate_event("button_clicked", {"id": 0, "entity": {"id": 1}, "duration": 0})
    assert game.players[0].type == PlayerType.POLICE
    assert game.players[1].type == PlayerType.CAUGHT
    assert game.players[2].type == PlayerType.THIEF
    game.engine.initiate_event("button_clicked", {"id": 0, "entity": {"id": 2}, "duration": 0})
    assert game.players[0].type == PlayerType.POLICE
    assert game.players[1].type == PlayerType.CAUGHT
    assert game.players[2].type == PlayerType.CAUGHT

    assert not game.thieves_won
    assert game.activePhase == game.Phase.ENDPHASE
