from enum import Enum
from .models.playermodel import PlayerModel, PlayerType
import gamelogic.policethiefgame.phases.startphase as startphase
import gamelogic.policethiefgame.phases.endphase as endphase
import gamelogic.policethiefgame.phases.ingamephase as ingamephase
from engine import Engine


class Phase(Enum):
    STARTPHASE = 1
    INGAMEPHASE = 2
    ENDPHASE = 3


engine = Engine("PoliceThief", test_setup= True)
# A list of players of type PlayerModel
players = []
# Map counts of player teams: thiefs, policemen
counts = [0,0]
# The currently active phase that will decide the behavior of the system
activePhase = Phase.STARTPHASE
# The timer that keeps track of the current running game
gametimer = None

thieves_won = False

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
        players.append(PlayerModel(id, PlayerType.THIEF))
        counts[0] += 1
    else:
        players.append(PlayerModel(id, PlayerType.POLICE))
        counts[1] += 1


def game_timer_ended():
    print('Timer ended')
    # The timer of the game has ended and the thiefs haven't been caught, so thieves win!
    # Trigger end game


@engine.register_trigger("game_started")
def on_game_started():
    activePhase = Phase.INGAMEPHASE
    ingamephase.startTimer(game_timer_ended(), gametimer)


@engine.register_trigger("on_game_ended")
def on_gamed_ended():
    activePhase = Phase.ENDPHASE
    if not thieves_won:
        gametimer.cancel()
    endphase.showEndGameState(thieves_won)


@engine.register_trigger("button_clicked")
def on_button_clicked(id, entity, duration):
    if activePhase == Phase.STARTPHASE:
        startphase.onButtonClicked(id,entity, duration, players, counts)
    elif activePhase == Phase.INGAMEPHASE:
        ingamephase.onButtonClicked(id, entity, duration, players, timer)

