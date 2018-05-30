from gamelogic.policethiefgame.models.playermodel import PlayerType
import engine.hardware.led as led
import engine.hardware.vibration_motor as vibration_motor
def on_button_clicked(button, entity, players, counts):
    for player in players:
        if player.entity == entity:
            switch_player_team(player, counts)


def switch_player_team(player, counts):
    if player.type == PlayerType.THIEF and counts[0] > 1:
        player.type = PlayerType.POLICE
        counts[1] += 1
        counts[0] -= 1
        player.entity.send_command(led.solid_state(led.PredefinedColors.ALICE_BLUE))
    elif player.type == PlayerType.POLICE and counts[1] > 1:
        player.type = PlayerType.THIEF
        counts[0] += 1
        counts[1] -= 1
        player.entity.send_command(led.solid_state(led.PredefinedColors.DARK_RED))
    player.entity.send_command(vibration_motor.vibrate(vibration_motor.PremadeVibrationPatterns.SHORT_BLIP))
    # Change leds of models to new color