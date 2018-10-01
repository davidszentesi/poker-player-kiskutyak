
class Player:
    VERSION = "0.4"

    def betRequest(self, game_state):
        our_player = game_state["players"]["in_action"]
        our_cards = our_player["hole_cards"]
        first_card = our_cards[0]
        second_card = our_cards[1]
        figures = ["J", "Q", "K", "A"]
        call = game_state["current_buy_in"] - our_player["in_action"]["bet"]

        # hands in pair
        if first_card["rank"] == second_card["rank"] and (first_card["rank"] >= 7 or first_card["rank"] in figures):
            return game_state["current_buy_in"] - our_player["bet"] + game_state["minimum_raise"]

        elif (first_card["rank"] >= 7 and second_card["rank"] in figures) or (second_card["rank"] >= 7 and first_card["rank"] in figures):

            if call < our_player["stack"] * 0.1:
                return call
            else:
                return 0

        else:
            return 200

    def showdown(self, game_state):
        pass

