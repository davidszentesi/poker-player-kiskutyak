from __future__ import print_function

import sys


class Player:
    VERSION = "1.1"

    def betRequest(self, game_state):
        in_action = game_state["in_action"]
        our_player = game_state["players"][in_action]
        stack = our_player["stack"]
        our_cards = our_player["hole_cards"]
        community_cards = game_state["community_cards"]
        minimum_raise = game_state["minimum_raise"]
        first_card = our_cards[0]
        second_card = our_cards[1]
        straights = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        figures = ["J", "Q", "K", "A"]
        high_cards = ["10", "J", "Q", "K", "A"]
        card_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12,
                     "K": 13,
                     "A": 14}
        possible_straight = abs(card_dict[first_card["rank"]] - card_dict[second_card["rank"]]) <= 4
        call = game_state["current_buy_in"] - our_player["bet"]
        pair_in_hand = first_card["rank"] == second_card["rank"] \
                       and (card_dict[first_card["rank"]] >= 8 or first_card["rank"] in figures)
        same_color = first_card["suit"] == second_card["suit"]
        same_color_with_figure = (first_card["rank"] in figures or second_card["rank"] in figures) \
                                 and same_color
        both_high_cards = first_card["rank"] in high_cards and second_card["rank"] in high_cards
        call_hand = pair_in_hand or same_color_with_figure or both_high_cards
        figure = first_card["rank"] in high_cards[-4:] or second_card["rank"] in high_cards[-4:]
        middle_call_hand = figure or (same_color and possible_straight)

        if call_hand:
            return call

        elif middle_call_hand:
            high_card_rank = max(card_dict[first_card["rank"]], card_dict[second_card["rank"]])
            low_card_rank = min(card_dict[first_card["rank"]], card_dict[second_card["rank"]])
            possible_call_for_high_pair = [True for card in community_cards if card["rank"] == high_card_rank]
            possible_call_for_two_pairs = possible_call_for_high_pair \
                                          or [True for card in community_cards if card["rank"] == low_card_rank]
            possible_call_for_drill = [card["rank"] for card in community_cards].count(first_card["rank"]) >= 2 \
                                      or [card["rank"] for card in community_cards].count(second_card["rank"]) >= 2
            if len(community_cards) == 0:
                return call

            # flop
            elif len(community_cards) == 3:
                straight = None
                highest_flop_pair = possible_call_for_high_pair \
                                    and high_card_rank == max([card["rank"] for card in community_cards])
                flop_card_ranks = sorted(
                    [card_dict[card["rank"]] for card in community_cards] + [high_card_rank, low_card_rank])
                for i in range(len(straights) - 5):
                    if flop_card_ranks == straights[i: i + 5]:
                        straight = True
                        break
                    else:
                        straight = False
                if straight:
                    return stack
                if possible_call_for_two_pairs or possible_call_for_drill or highest_flop_pair:
                    return call + minimum_raise
                elif possible_call_for_high_pair:
                    return call
                else:
                    return 0

            # turn & river
            else:
                return call

        else:
            return 0

    def showdown(self, game_state):
        pass

    def log(self, message):
        print(message, file=sys.stderr)
