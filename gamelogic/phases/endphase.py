
class EndPhase:
    players = []

    def __init__(self, players):
        self.players = players

    def onButtonClicked(self, id, entity, duration):
        pass

    def endGameStarted(self):
        # Show engame state to players (eg. all leds to winning team color)
        pass

    def restartGameRequested(self):
        # Reinitialize to default options
        pass
