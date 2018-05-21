from gamelogic.policethiefgame.models.playermodel import PlayerType


def on_button_clicked(id, entity, duration, players, engine):
    for player in players:
        if player.id == entity["id"] and player.type == PlayerType.THIEF:
            on_thief_pressed(player, players, engine)
    # Check if police or thief and call the right methods
    pass


def on_thief_pressed(player, players, engine):
    player.type = PlayerType.CAUGHT
    # Use library to change color of the player and set the state
    for item in players:
        if item.type == PlayerType.THIEF:
            return
    # All thiefs are caught so endgame state is reached
    engine.initiate_event("game_ended", {})
    # Send game ended due to thieves caught
