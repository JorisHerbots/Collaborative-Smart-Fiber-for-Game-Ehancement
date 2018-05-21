from engine import Engine
from .models.playermodel import PlayerModel
from .models.teammodel import Team
import gamelogic.paintball_enhance.button_interactions as buttons


class Phase:
    STARTPHASE = 1,
    INGAMEPHASE = 2


engine = Engine("PaintBall", test_setup=True)
team1 = Team()
team2 = Team()
active_phase = Phase.STARTPHASE


@engine.register_trigger("on_entity_registered")
def on_entity_registered(id):
    """
        When an entity is registered.
        Add the entity as models and put it in either the team1 or team2.
        :param entity:
        :return:
    """
    # If the models is already registered in team1 or 2, there is probably a network fault.
    if team1.contains_player_with_id(id):
        return
    elif team2.contains_player_with_id(id):
        return

    # When team1 has less players than team2, the new models becomes part of team1 and vice versa.
    if team1.size() <= team2.size():
        team1.add_player(PlayerModel(id))
    else:
        team2.add_player(PlayerModel(id))

    # Show team color for models


@engine.register_trigger("button_clicked")
def on_button_clicked(id, entity, duration):
    if active_phase == Phase.STARTPHASE:
        switch_team_of_playerid(entity.id)
    elif active_phase == Phase.INGAMEPHASE:
        buttontype = buttons.get_button_type(id)
        if team1.contains_player_with_id(entity.id):
            buttons.execute_button(buttontype, entity, engine, team1)
        elif team2.contains_player_with_id(entity.id):
            buttons.execute_button(buttontype, entity, engine, team2)


@engine.register_trigger("game_started")
def on_game_started():
    global active_phase
    active_phase = Phase.INGAMEPHASE


@engine.register_trigger("game_ended")
def on_game_ended():
    # Reset state of all players of hit to non-hit
    pass


def switch_team_of_playerid(player_id):
    if team1.contains_player_with_id(player_id):
        player = team1.retrieve_player_with_id(player_id)
        team2.add_player(player)
        team1.remove_player(player)
    elif team2.contains_player_with_id(player_id):
        player = team2.retrieve_player_with_id(player_id)
        team1.add_player(player)
        team2.remove_player(player)
