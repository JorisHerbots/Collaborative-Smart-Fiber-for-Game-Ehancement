from enum import Enum
from models.playermodel import PlayerModel, PlayerType
import phases.startphase as StartPhase
import phases.endphase as EndPhase
import phases.ingamephase as InGamePhase
from engine import Engine

class Phase(Enum):
    STARTPHASE = 1
    INGAMEPHASE = 2
    ENDPHASE = 3

def startGame():
    engine = Engine("PoliceThief")
    # A list of players of type PlayerModel
    players = []
    # Map counts of player teams: thiefs, policemen
    counts = [0,0]
    # The currently active phase that will decide the behavior of the system
    activePhase = Phase.STARTPHASE
    # The timer that keeps track of the current running game
    gametimer = None

    thieves_won = False

    @engine.register_trigger("onEntityRegistered")
    def onEntityRegistered(entity):
        """
            When an entity is registered.
            Add the entity as player and put it in either the team of policemen or thiefs.
        :param entity:
        :return:
        """
        # If the player is already registered, there is probably a network fault.
        for player in players:
            if player.id == entity.id:
                return
        # When there are less thieves than policemen, the new player becomes a thief and vice versa.
        if counts[0] <= counts[1]:
            players.append(PlayerModel(entity.id, PlayerType.THIEF))
            counts[0] += 1
        else:
            players.append(PlayerModel(entity.id, PlayerType.POLICE))
            counts[1] += 1

    def gameTimerEnded():
        print('Timer ended')
        thieves_won = True
        # The timer of the game has ended and the thiefs haven't been caught, so thieves win!
        # Trigger end game

    @engine.register_trigger("onGameStarted")
    def onGameStart():
        activePhase = Phase.INGAMEPHASE
        InGamePhase.startTimer(gameTimerEnded, gametimer)

    @engine.register_trigger("onGameEnded")
    def onGameEnded():
        activePhase = Phase.ENDPHASE
        if not thieves_won:
            gametimer.cancel()
        EndPhase.showEndGameState(thieves_won)

    @engine.register_trigger("buttonClicked")
    def onButtonClicked(id, entity, duration):
        if activePhase == Phase.STARTPHASE:
            StartPhase.onButtonClicked(id,entity, duration, players, counts)
        elif activePhase == Phase.INGAMEPHASE:
            InGamePhase.onButtonClicked(id, entity, duration, players, timer)

    engine.initiate_event("buttonClicked", {"id": None, "entity": {"id": 1}, "duration": None})
    engine.initiate_event("onGameStarted", {})

startGame()
