from enum import Enum

class PhaseEvent:
    GAME_INITREQUEST = 1
    GAME_STARTREQUEST = 2
    GAME_ENDREQUEST = 3


# Defining the methods that gamephases need to hold
class GamePhase:
    game = None

    def __init__(self):
        pass

    def runPhase(self):
        pass

    def register(self, game):
        self.game = game

    def notify(self, event):
        if self.game is not None:
            self.game.onPhaseEvent(event)
