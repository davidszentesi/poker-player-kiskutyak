from __future__ import print_function

import sys


class Player:
    VERSION = "1.5"

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
        pair_in_hand_low = first_card["rank"] == second_card["rank"] \
                       and (card_dict[first_card["rank"]] <= 7 or first_card["rank"] in figures)
        same_color = first_card["suit"] == second_card["suit"]
        same_color_with_figure = (first_card["rank"] in figures or second_card["rank"] in figures) \
                                 and same_color
        both_high_cards = first_card["rank"] in high_cards and second_card["rank"] in high_cards
        call_hand = pair_in_hand or same_color_with_figure or both_high_cards
        figure = first_card["rank"] in high_cards[-4:] or second_card["rank"] in high_cards[-4:]
        middle_call_hand = figure or (same_color and possible_straight) or pair_in_hand_low

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
            highest_pair = possible_call_for_high_pair \
                                and high_card_rank == max([card["rank"] for card in community_cards])
            current_buy_in = game_state["current_buy_in"]
            if len(community_cards) == 0:
                if current_buy_in <= stack / 2:
                    return call
                else:
                    return 0

            # flop
            elif len(community_cards) == 3:
                straight = None
                flop_card_ranks = sorted(
                    [card_dict[card["rank"]] for card in community_cards] + [high_card_rank, low_card_rank])
                flop_card_suits = [card["suit"] for card in community_cards] + [first_card["suit"], second_card["suit"]]
                flush = len(set(flop_card_suits)) == 1
                for i in range(len(straights) - 5):
                    if flop_card_ranks == straights[i: i + 5]:
                        straight = True
                        break
                    else:
                        straight = False
                if flush:
                    return stack
                if straight:
                    return stack
                if possible_call_for_two_pairs or possible_call_for_drill:
                    return call + minimum_raise * 2
                elif highest_pair:
                    return call + minimum_raise
                elif possible_call_for_high_pair:
                    return call
                else:
                    return 0

            # turn
            elif len(community_cards) == 4:
                if possible_call_for_drill:
                    return stack
                elif highest_pair:
                    return call + minimum_raise * 2
                else:
                    return call

            # river
            else:
                if possible_call_for_drill:
                    return stack
                elif highest_pair:
                    return call + minimum_raise * 2
                else:
                    return call

        else:
            return 0

    def showdown(self, game_state):
        pass

    def log(self, message):
        print(message, file=sys.stderr)
