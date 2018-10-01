
class Player:
    VERSION = "0.3"

    def betRequest(self, game_state):
        our_player = game_state["players"]["in_action"]
        our_cards = our_player["hole_cards"]
        if our_cards[0]["rank"] == our_cards[1]["rank"] and our_cards[0]["rank"] >= 7:
            return game_state["current_buy_in"] - our_player["bet"] + game_state["minimum_raise"]
        else:
            return 100

    def showdown(self, game_state):
        pass

