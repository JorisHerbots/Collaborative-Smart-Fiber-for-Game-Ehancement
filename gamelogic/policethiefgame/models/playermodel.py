from enum import Enum


class PlayerType(Enum):
    POLICE = 1
    THIEF = 2
    CAUGHT = 3


# This class is for keeping data about a PlayerModel in the game
class PlayerModel:

    def __init__(self, entity, type):
        self.entity = entity
        self.type = type