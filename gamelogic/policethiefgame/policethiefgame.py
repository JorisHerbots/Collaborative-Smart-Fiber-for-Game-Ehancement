from enum import Enum
from .models.playermodel import PlayerModel, PlayerType
import gamelogic.policethiefgame.phases.startphase as startphase
import gamelogic.policethiefgame.phases.endphase as endphase
import gamelogic.policethiefgame.phases.ingamephase as ingamephase
import threading as thread
from engine import Engine
import engine.hardware.led as led

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
    thieves_won = True
    # Trigger end game
    on_game_ended()


@engine.register_trigger("entity_registered")
def entity_registered(entity):
    """
        When an entity is registered.
        Add the entity as models and put it in either the team of policemen or thiefs.
    :param entity:
    :return:
    """
    try:
        # If the models is already registered, there is probably a network fault.
        for player in players:
            if player.entity == entity:
                return

        # When there are less thieves than policemen, the new models becomes a thief and vice versa.
        if counts[0] <= counts[1]:
            players.append(PlayerModel(entity, PlayerType.THIEF))
            entity.send_command(led.solid_state(led.PredefinedColors.DARK_RED))
            counts[0] += 1
        else:
            players.append(PlayerModel(entity, PlayerType.POLICE))
            entity.send_command(led.solid_state(led.PredefinedColors.ALICE_BLUE))
            counts[1] += 1
    except:
        pass



@engine.register_trigger("game_started")
def on_game_started():
    global gametimer, activePhase
    activePhase = Phase.INGAMEPHASE
    if gametimer is not None:
        gametimer.cancel()
    # Run the game timer for 15 minutes
    gametimer = thread.Timer(5, game_timer_ended)
    for player in players:
        if player.type == PlayerType.POLICE:
            player.entity.send_command(led.blink(800, led.PredefinedColors.ALICE_BLUE, 800, led.PredefinedColors.RED))
    gametimer.start()


def on_game_ended():
    global activePhase
    activePhase = Phase.ENDPHASE
    # If the thieves haven't won, that means the gametimer is still active
    if not thieves_won:
        gametimer.cancel()
    endphase.showEndGameState(thieves_won, players)
    # Wait 5 seconds to trigger end game on the engine
    thread.Timer(5, trigger_engine_end)


def trigger_engine_end():
    engine.end_game()


@engine.register_trigger("button_pressed")
def on_button_clicked(button, entity):
    if activePhase == Phase.STARTPHASE:
        startphase.on_button_clicked(button, entity, players, counts)
    elif activePhase == Phase.INGAMEPHASE:
        ingamephase.on_button_clicked(button, entity, players, engine)

