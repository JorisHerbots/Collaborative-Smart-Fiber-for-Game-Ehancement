class ButtonType:
    ATTACK = 1,
    DEFENSE = 2,
    HIT = 3


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
        pass
    elif button_type == ButtonType.DEFENSE:
        # Call defense mode vibrate for the whole team
        pass
    elif button_type == ButtonType.HIT:
        # Switch between hitted and not hitted for a player
        pass