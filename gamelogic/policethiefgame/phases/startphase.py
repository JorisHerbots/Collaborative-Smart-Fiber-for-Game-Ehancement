from gamelogic.policethiefgame.models.playermodel import PlayerType


def on_button_clicked(button, entity, players, counts):
    for player in players:
        if player.id == entity["ipv4_address"]:
            switch_player_team(player, counts)


def switch_player_team(player, counts):
    if player.type == PlayerType.THIEF and counts[0] > 1:
        player.type = PlayerType.POLICE
        counts[1] += 1
        counts[0] -= 1
    elif player.type == PlayerType.POLICE and counts[1] > 1:
        player.type = PlayerType.THIEF
        counts[0] += 1
        counts[1] -= 1
    # Change leds of models to new color