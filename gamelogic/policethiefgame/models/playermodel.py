from enum import Enum


class PlayerType(Enum):
    POLICE = 1
    THIEF = 2
    CAUGHT = 3


# This class is for keeping data about a PlayerModel in the game
class PlayerModel:

    def __init__(self, id, type):
        self.id = id
        self.type = type