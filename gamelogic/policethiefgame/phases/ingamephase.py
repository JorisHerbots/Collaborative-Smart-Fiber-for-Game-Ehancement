from gamelogic.policethiefgame.models.playermodel import PlayerType
import engine.hardware.vibration_motor as vibration_motor

def on_button_clicked(button, entity, players, engine):
    for player in players:
        if player.entity == entity and player.type == PlayerType.THIEF:
            on_thief_pressed(player, players, engine)
    # Check if police or thief and call the right methods
    pass


def on_thief_pressed(player, players, engine):
    player.type = PlayerType.CAUGHT
    found = False
    # Use library to change color of the models and set the state
    for item in players:
        if item.type == PlayerType.THIEF:
            item.entity.send_command(vibration_motor.vibrate(vibration_motor.PremadeVibrationPatterns.LONG_BLIP))
            found = True
    if found:
        return
    # All thiefs are caught so endgame state is reached
    engine.initiate_event("game_ended", {})
    # Send game ended due to thieves caught
