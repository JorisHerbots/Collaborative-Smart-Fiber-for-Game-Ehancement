from models.playermodel import PlayerType

def onButtonClicked(id, entity, duration, players, counts):
    for player in players:
        if player.id == entity.id:
            switchPlayerTeam(player, counts)

def switchPlayerTeam(player, counts):
    if player.type == PlayerType.THIEF and counts[1] > 1:
        player.type = PlayerType.POLICE
        counts[1] -= 1
        counts[0] += 1
    elif player.type == PlayerType.POLICE and counts[0] > 1:
        player.type = PlayerType.THIEF
        counts[0] -= 1
        counts[1] += 1
