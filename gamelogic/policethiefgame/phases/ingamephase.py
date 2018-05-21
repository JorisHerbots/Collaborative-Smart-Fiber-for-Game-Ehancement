from gamelogic.policethiefgame.models.playermodel import PlayerType
import threading as thread

def startTimer(func, timer):
    if timer is not None:
        timer.cancel()
    # Run the game timer for 15 minutes
    timer = thread.Timer(5, func)
    print("Timer started.")
    timer.start()

def onButtonClicked(id, entity, duration, players, timer):
    for player in players:
        if player.id == entity.id and player.type == PlayerType.THIEF:
            onThiefPressed(player, players, timer)
    # Check if police or thief and call the right methods
    pass

def onThiefPressed(player, players, timer):
    player.type = PlayerType.CAUGHT
    # Use library to change color of the player and set the state
    for item in players:
        if item.type == PlayerType.THIEF:
            return
    # All thiefs are caught so endgame state is reached
    timer.cancel()
    # Send game ended due to thieves caught
