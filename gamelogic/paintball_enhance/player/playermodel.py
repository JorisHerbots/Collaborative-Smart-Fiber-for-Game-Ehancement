from enum import Enum

# This class is for keeping data about a PlayerModel in the game
class PlayerModel:
    team = 0
    id = 1

    def __init__(self, id, team):
        self.id = id
        self.team = team