from __future__ import print_function

import sys


class Player:
    VERSION = "0.6"

    def betRequest(self, game_state):
        in_action = game_state["in_action"]
        our_player = game_state["players"][in_action]
        our_cards = our_player["hole_cards"]
        community_cards = game_state["community_cards"]
        first_card = our_cards[0]
        second_card = our_cards[1]
        figures = ["J", "Q", "K", "A"]
        high_cards = ["10", "J", "Q", "K", "A"]
        card_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
        possible_straight = abs(card_dict[first_card["rank"]] - card_dict[second_card["rank"]]) <= 4
        call = game_state["current_buy_in"] - our_player["bet"]
        pair_in_hand = first_card["rank"] == second_card["rank"] \
                       and (first_card["rank"] >= 8 or first_card["rank"] in figures)
        same_color = first_card["suit"] == second_card["suit"]
        same_color_with_figure = (first_card["rank"] in figures or second_card["rank"] in figures) \
                                 and same_color
        both_high_cards = first_card["rank"] in high_cards and second_card["rank"] in high_cards
        call_hand = pair_in_hand or same_color_with_figure or both_high_cards
        ace_or_king = first_card["rank"] in high_cards[-2:] or second_card["rank"] in high_cards[-2:]
        middle_call_hand = ace_or_king or same_color or possible_straight

        if call_hand:
            return call

        elif middle_call_hand:
            if len(community_cards) == 0:
                return call
            elif len(community_cards) == 3:
                high_card_rank = max(first_card["rank"], second_card["rank"])
                possible_call = [True for card in community_cards if card["rank"] == high_card_rank]
                if possible_call:
                    return call
                else:
                    return 0

        else:
            return 0

    def showdown(self, game_state):
        pass

    def log(self, message):
        print(message, file=sys.stderr)
