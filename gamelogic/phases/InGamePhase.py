from phases.GamePhase import GamePhase, PhaseEvent
from models.PlayerModel import PlayerType, PlayerModel

class InGamePhase(GamePhase):
    players = []

    def __init__(self, players):
        self.players = players

    def runPhase(self):
        # Call functions based on events
        pass

    def onThiefPressed(self, player):
        for item in self.players:
            if item.id == player.id:
                item.type = PlayerType.CAUGHT
                # Use library to change color of the player and set the state
                break
        for item in self.players:
            if item.type == PlayerType.THIEF:
                return
        # All thiefs are caught so endgame state is reached
        self.notify(PhaseEvent.GAME_ENDREQUEST)
