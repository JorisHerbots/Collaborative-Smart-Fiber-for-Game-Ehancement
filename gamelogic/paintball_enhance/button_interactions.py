import engine.hardware.vibration_motor as vibration_motor
import engine.hardware.led as led

class ButtonType:
    ATTACK = 0
    DEFENSE = 1
    HIT = 2


def get_button_type(button_id):
    """
    Placeholder function to calculate the button type from the given id
    Probably needs change depending on how the id's were calculated
    :param button_id:
    :return:
    """
    if button_id == ButtonType.ATTACK:
        return ButtonType.ATTACK
    elif button_id == ButtonType.DEFENSE:
        return ButtonType.DEFENSE
    elif button_id == ButtonType.HIT:
        return ButtonType.HIT


def execute_button(button_type, entity, engine, team):
    if button_type == ButtonType.ATTACK:
        # Call attack mode vibrate for the whole team
        for player in team.players:
            if player.entity != entity:
                player.entity.send_command(vibration_motor.vibrate(vibration_motor.PremadeVibrationPatterns.TWO_LONG_BLIPS))

    elif button_type == ButtonType.DEFENSE:
        # Call defense mode vibrate for the whole team
        for player in team.players:
            if player.entity != entity:
                player.entity.send_command(vibration_motor.vibrate(vibration_motor.PremadeVibrationPatterns.THREE_SHORT_BLIPS))

    elif button_type == ButtonType.HIT:
        # Switch between hitted and not hitted for a player
        for player in team.players:
            if player.entity == entity:
                if not player.hitted:
                    entity.send_command(led.solid_state(led.PredefinedColors.RED))
                    player.hitted = True
                else:
                    entity.send_command(led.solid_state(team.color))
                    player.hitted = False
                entity.send_command(vibration_motor.vibrate(vibration_motor.PremadeVibrationPatterns.SHORT_BLIP))