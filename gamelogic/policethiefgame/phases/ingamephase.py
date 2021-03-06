from gamelogic.policethiefgame.models.playermodel import PlayerType
import engine.hardware.vibration_motor as vibration_motor
import engine.hardware.led as led
import gamelogic.policethiefgame as game

def on_button_clicked(button, entity, players, engine):
    for player in players:
        if player.entity == entity and player.type == PlayerType.THIEF:
            return on_thief_pressed(player, players, engine)
    # Check if police or thief and call the right methods
    return False


def on_thief_pressed(player, players, engine):
    player.type = PlayerType.CAUGHT
    player.entity.send_command(led.solid_state(led.PredefinedColors.GREEN))
    found = False
    for item in players:
        if item.type == PlayerType.THIEF:
            found = True
            item.entity.send_command(vibration_motor.vibrate(vibration_motor.PremadeVibrationPatterns.LONG_BLIP))
    if found:
        return False
    # All thiefs are caught so endgame state is reached

    # Send game ended due to thieves caught
    return True