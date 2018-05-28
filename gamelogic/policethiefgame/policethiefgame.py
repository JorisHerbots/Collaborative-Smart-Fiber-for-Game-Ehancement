from enum import Enum
from .models.playermodel import PlayerModel, PlayerType
import gamelogic.policethiefgame.phases.startphase as startphase
import gamelogic.policethiefgame.phases.endphase as endphase
import gamelogic.policethiefgame.phases.ingamephase as ingamephase
import threading as thread
from engine import Engine


class Phase(Enum):
    STARTPHASE = 1
    INGAMEPHASE = 2
    ENDPHASE = 3


engine = Engine("PoliceThief")
# A list of players of type PlayerModel
players = []
# Map counts of models teams: thiefs, policemen
counts = [0,0]
# The currently active phase that will decentitye the behavior of the system
activePhase = Phase.STARTPHASE
# The timer that keeps track of the current running game
gametimer = None

thieves_won = False


def reset():
    global players, counts, activePhase, gametimer
    players = []
    counts = [0, 0]
    activePhase = Phase.STARTPHASE
    gametimer = None


def game_timer_ended():
    print('Timer ended')
    # The timer of the game has ended and the thiefs haven't been caught, so thieves win!
    # Trigger end game
    engine.initiate_event("game_ended", {})


@engine.register_trigger("entity_registered")
def entity_registered(entity):
    """
        When an entity is registered.
        Add the entity as models and put it in either the team of policemen or thiefs.
    :param entity:
    :return:
    """
    # If the models is already registered, there is probably a network fault.
    for player in players:
        if player.entity == entity:
            return

    # When there are less thieves than policemen, the new models becomes a thief and vice versa.
    if counts[0] <= counts[1]:
        players.append(PlayerModel(entity, PlayerType.THIEF))
        counts[0] += 1
    else:
        players.append(PlayerModel(entity, PlayerType.POLICE))
        counts[1] += 1
    # Change leds of models to new color


@engine.register_trigger("game_started")
def on_game_started():
    global gametimer, activePhase
    activePhase = Phase.INGAMEPHASE
    if gametimer is not None:
        gametimer.cancel()
    # Run the game timer for 15 minutes
    gametimer = thread.Timer(5, game_timer_ended)

    print("Timer started.")
    gametimer.start()


@engine.register_trigger("game_ended")
def on_game_ended():
    global activePhase
    activePhase = Phase.ENDPHASE
    if not thieves_won:
        gametimer.cancel()
    endphase.showEndGameState(thieves_won)


@engine.register_trigger("button_pressed")
def on_button_clicked(button, entity):
    if activePhase == Phase.STARTPHASE:
        startphase.on_button_clicked(button, entity, players, counts)
    elif activePhase == Phase.INGAMEPHASE:
        ingamephase.on_button_clicked(button, entity, players, engine)

