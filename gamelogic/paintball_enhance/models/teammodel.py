
class Team:

    def __init__(self):
        self.players = []
        pass

    def add_player(self, player):
        self.players.append(player)

    def contains_player_with_id(self, id):
        for player in self.players:
            if player.id == id:
                return True
        return False

    def retrieve_player_with_id(self, id):
        for player in self.players:
            if player.id == id:
                return player
        return None

    def size(self):
        return len(self.players)

    def remove_player(self, player):
        self.players.remove(player)