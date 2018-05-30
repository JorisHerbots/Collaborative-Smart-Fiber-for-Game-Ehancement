from enum import Enum


# This class is for keeping data about a PlayerModel in the game
class PlayerModel:

    def __init__(self, entity):
        self.entity = entity
        self.hitted = False