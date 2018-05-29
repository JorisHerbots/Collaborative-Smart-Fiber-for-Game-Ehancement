import engine.hardware.led as led
import engine.hardware.vibration_motor as vibration_motor

def showEndGameState(thieves_won, players):
    if thieves_won:
        for player in players:
            player.entity.send_command(vibration_motor.vibrate(vibration_motor.PremadeVibrationPatterns.LONG_BLIP))
            player.entity.send_command(led.solid_state(led.PredefinedColors.DARK_RED))
    else:
        for player in players:
            player.entity.send_command(vibration_motor.vibrate(vibration_motor.PremadeVibrationPatterns.LONG_BLIP))
            player.entity.send_command(led.solid_state(led.PredefinedColors.ALICE_BLUE))
