from engine import Engine
from .player.playermodel import PlayerModel

engine = Engine("PaintBallEnhance", test_setup=True)
players = []
counts = [0, 0]

@engine.register_trigger("on_entity_registered")
def on_entity_registered(id):
    """
        When an entity is registered.
        Add the entity as player and put it in either the team of policemen or thiefs.
        :param entity:
        :return:
    """
    # If the player is already registered, there is probably a network fault.
    for player in players:
        if player.id == id:
            return

    # When there are less thieves than policemen, the new player becomes a thief and vice versa.
    if counts[0] <= counts[1]:
        players.append(PlayerModel(id, 0))
        counts[0] += 1
    else:
        players.append(PlayerModel(id, 1))
        counts[1] += 1

