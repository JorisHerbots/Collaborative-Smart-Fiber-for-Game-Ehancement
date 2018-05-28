import gamelogic.policethiefgame.policethiefgame as game
from gamelogic.policethiefgame.models.playermodel import PlayerType, PlayerModel
import pytest
import time


def test_players_registration():
    game.reset()
    assert game.engine.event_triggers["entity_registered"][0] == game.entity_registered
    game.engine.initiate_event("entity_registered", {"entity": {"ipv4_address": 0}})
    game.engine.initiate_event("entity_registered", {"entity": {"ipv4_address": 1}})
    time.sleep(1)
    assert len(game.players) == 2
    assert game.players[0].type != game.players[1].type

def test_team_switch():
    game.reset()
    game.engine.initiate_event("entity_registered", {"entity": {"ipv4_address": 0}})
    game.engine.initiate_event("entity_registered", {"entity": {"ipv4_address": 1}})
    game.engine.initiate_event("entity_registered", {"entity": {"ipv4_address": 2}})
    time.sleep(1)
    assert game.players[0].type == PlayerType.THIEF
    assert game.players[1].type == PlayerType.POLICE
    assert game.players[2].type == PlayerType.THIEF

    game.engine.initiate_event("button_pressed", {"button": 0, "entity": {"ipv4_address": 0}})
    time.sleep(1)
    assert game.players[0].type == PlayerType.POLICE
    assert game.players[1].type == PlayerType.POLICE
    assert game.players[2].type == PlayerType.THIEF

    # Having no thiefs is not allowed
    game.engine.initiate_event("button_pressed", {"button": 0, "entity": {"ipv4_address": 2}})
    time.sleep(1)
    assert game.players[0].type == PlayerType.POLICE
    assert game.players[1].type == PlayerType.POLICE
    assert game.players[2].type == PlayerType.THIEF

    game.engine.initiate_event("button_pressed", {"button": 0, "entity": {"ipv4_address": 1}})
    time.sleep(1)
    assert game.players[0].type == PlayerType.POLICE
    assert game.players[1].type == PlayerType.THIEF
    assert game.players[2].type == PlayerType.THIEF

    game.engine.initiate_event("button_pressed", {"button": 0, "entity": {"ipv4_address": 1}})
    time.sleep(1)
    assert game.players[0].type == PlayerType.POLICE
    assert game.players[1].type == PlayerType.POLICE
    assert game.players[2].type == PlayerType.THIEF

def test_police_tapped():
    game.reset()
    game.engine.initiate_event("entity_registered", {"entity": {"ipv4_address": 0}})
    game.engine.initiate_event("entity_registered", {"entity": {"ipv4_address": 1}})
    game.engine.initiate_event("entity_registered", {"entity": {"ipv4_address": 2}})
    time.sleep(1)
    assert game.players[1].type == PlayerType.POLICE
    game.engine.initiate_event("game_started", {})
    game.engine.initiate_event("button_pressed", {"button": 0, "entity": {"ipv4_address": 1}})
    time.sleep(1)
    assert game.players[1].type == PlayerType.POLICE
    assert game.gametimer.is_alive()
    game.gametimer.cancel()

def test_gameplay_thiefs_caught():
    game.reset()
    # Engine players registration phase
    game.engine.initiate_event("entity_registered", {"entity": {"ipv4_address": 0}})
    game.engine.initiate_event("entity_registered", {"entity": {"ipv4_address": 1}})
    game.engine.initiate_event("entity_registered", {"entity": {"ipv4_address": 2}})
    time.sleep(1)
    assert game.activePhase == game.Phase.STARTPHASE

    # Players appointment phase
    game.engine.initiate_event("button_pressed", {"button": 0, "entity": {"ipv4_address": 0}})
    game.engine.initiate_event("button_pressed", {"button": 0, "entity": {"ipv4_address": 1}})
    time.sleep(1)
    assert game.players[0].type == PlayerType.POLICE
    assert game.players[1].type == PlayerType.THIEF
    assert game.players[2].type == PlayerType.THIEF

    # Start the game, timer should be active
    game.engine.initiate_event("game_started", {})
    time.sleep(1)
    assert game.gametimer.is_alive()
    assert game.activePhase == game.Phase.INGAMEPHASE
    assert game.players[0].type == PlayerType.POLICE
    assert game.players[1].type == PlayerType.THIEF
    assert game.players[2].type == PlayerType.THIEF

    game.engine.initiate_event("button_pressed", {"button": 0, "entity": {"ipv4_address": 1}})
    time.sleep(1)
    assert game.players[0].type == PlayerType.POLICE
    assert game.players[1].type == PlayerType.CAUGHT
    assert game.players[2].type == PlayerType.THIEF
    game.engine.initiate_event("button_pressed", {"button": 0, "entity": {"ipv4_address": 1}})
    time.sleep(1)
    assert game.players[0].type == PlayerType.POLICE
    assert game.players[1].type == PlayerType.CAUGHT
    assert game.players[2].type == PlayerType.THIEF
    game.engine.initiate_event("button_pressed", {"button": 0, "entity": {"ipv4_address": 2}})
    time.sleep(1)
    assert game.players[0].type == PlayerType.POLICE
    assert game.players[1].type == PlayerType.CAUGHT
    assert game.players[2].type == PlayerType.CAUGHT

    assert not game.thieves_won
    assert game.activePhase == game.Phase.ENDPHASE
