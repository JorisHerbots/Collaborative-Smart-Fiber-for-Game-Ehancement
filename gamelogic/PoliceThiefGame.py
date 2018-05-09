from gamelogic.phases.StartPhase import StartPhase

# The main game file
class PoliceThiefGame:
    players = []
    activePhase = StartPhase()
    def __init__(self):
        print(self)

    def addPlayer(self, player):
        self.players.append(player)
