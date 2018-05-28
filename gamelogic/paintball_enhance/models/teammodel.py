
class Team:

    def __init__(self):
        self.players = []
        pass

    def add_player(self, player):
        self.players.append(player)

    def contains_player_with_entity(self, entity):
        for player in self.players:
            if player.entity == entity:
                return True
        return False

    def retrieve_player_with_entity(self, entity):
        for player in self.players:
            if player.entity == entity:
                return player
        return None

    def size(self):
        return len(self.players)

    def remove_player(self, player):
        self.players.remove(player)