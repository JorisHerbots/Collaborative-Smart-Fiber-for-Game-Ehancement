from phases.StartPhase import StartPhase
from phases.EndPhase import EndPhase
from phases.InGamePhase import InGamePhase

# The main game file
from phases.GamePhase import PhaseEvent


class PoliceThiefGame:
    players = []
    activePhase = StartPhase()

    def __init__(self):
        print(self)

    def addPlayer(self, player):
        self.players.append(player)

    def onPhaseEvent(self, event):
        if event == PhaseEvent.GAME_STARTREQUEST:
            self.activePhase = InGamePhase(self.players)
        elif event == PhaseEvent.GAME_ENDREQUEST:
            self.activePhase = EndPhase(self.players)
        elif event == PhaseEvent.GAME_INITREQUEST:
            self.activePhase = StartPhase()

        self.activePhase.register(self)
        self.activePhase.runPhase()

game = PoliceThiefGame()
