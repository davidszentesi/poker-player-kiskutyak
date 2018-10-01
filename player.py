from __future__ import print_function

import sys


class Player:
    VERSION = "0.5"

    def betRequest(self, game_state):
        in_action = game_state["in_action"]
        our_player = game_state["players"][in_action]
        our_cards = our_player["hole_cards"]
        first_card = our_cards[0]
        second_card = our_cards[1]
        figures = ["J", "Q", "K", "A"]
        high_cards = ["10", "J", "Q", "K", "A"]
        call = game_state["current_buy_in"] - our_player["bet"]
        pair_in_hand = first_card["rank"] == second_card["rank"] \
                       and (first_card["rank"] >= 8 or first_card["rank"] in figures)
        same_color_with_figure = (first_card["rank"] in figures or second_card["rank"] in figures) \
                                 and (first_card["suit"] == second_card["suit"])
        both_high_cards = first_card["rank"] in high_cards and second_card["rank"] in high_cards
        call_hand = pair_in_hand or same_color_with_figure or both_high_cards

        if call_hand:
            return call

        # hands in pair
        if first_card["rank"] == second_card["rank"] and (first_card["rank"] >= 7 or first_card["rank"] in figures):
            Player.log(self, "Pair in hand bet")
            return game_state["current_buy_in"] - our_player["bet"] + game_state["minimum_raise"]

        elif (first_card["rank"] >= 7 and second_card["rank"] in figures) or (
                second_card["rank"] >= 7 and first_card["rank"] in figures):

            if call < our_player["stack"] * 0.1:
                return call
            else:
                return 20

        else:
            return 20

    def showdown(self, game_state):
        pass

    def log(self, message):
        print(message, file=sys.stderr)
