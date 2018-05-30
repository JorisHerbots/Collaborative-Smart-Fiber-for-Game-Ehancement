from engine import Engine
from gamelogic.paintball_enhance.models.playermodel import PlayerModel
from gamelogic.paintball_enhance.models.teammodel import Team
import gamelogic.paintball_enhance.button_interactions as buttons
import engine.hardware.led as led

class Phase:
    STARTPHASE = 1,
    INGAMEPHASE = 2


engine = Engine("PaintBall", host="0.0.0.0")
team1 = Team(led.PredefinedColors.BLUE)
team2 = Team(led.PredefinedColors.GREEN)
active_phase = Phase.STARTPHASE

def reset():
    global team1, team2, active_phase
    team1 = Team(led.PredefinedColors.BLUE)
    team2 = Team(led.PredefinedColors.GREEN)
    active_phase = Phase.STARTPHASE


@engine.register_trigger("entity_registered")
def entity_registered(entity):
    """
        When an entity is registered.
        Add the entity as models and put it in either the team1 or team2.
        :param entity:
        :return:
    """

    # If the models is already registered in team1 or 2, there is probably a network fault.
    if team1.contains_player_with_entity(entity):
        return
    elif team2.contains_player_with_entity(entity):
        return

    # When team1 has less players than team2, the new models becomes part of team1 and vice versa.
    if team1.size() <= team2.size():
        team1.add_player(PlayerModel(entity))
        entity.send_command(led.solid_state(team1.color))
    else:
        team2.add_player(PlayerModel(entity))
        entity.send_command(led.solid_state(team2.color))

    # Show team color for models


@engine.register_trigger("button_pressed")
def on_button_clicked(button, entity):
    if active_phase == Phase.STARTPHASE:
        switch_team_of_player_entity(entity)
    elif active_phase == Phase.INGAMEPHASE:
        buttontype = buttons.get_button_type(button)
        if team1.contains_player_with_entity(entity):
            buttons.execute_button(buttontype, entity, engine, team1)
        elif team2.contains_player_with_entity(entity):
            buttons.execute_button(buttontype, entity, engine, team2)


@engine.register_trigger("game_started")
def on_game_started():
    global active_phase
    active_phase = Phase.INGAMEPHASE


def on_game_ended():
    pass


def switch_team_of_player_entity(player_entity):
    if team1.contains_player_with_entity(player_entity):
        player = team1.retrieve_player_with_entity(player_entity)
        team2.add_player(player)
        team1.remove_player(player)
        player_entity.send_command(led.solid_state(team2.color))
    elif team2.contains_player_with_entity(player_entity):
        player = team2.retrieve_player_with_entity(player_entity)
        team1.add_player(player)
        team2.remove_player(player)
        player_entity.send_command(led.solid_state(team1.color))
