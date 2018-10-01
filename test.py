def betRequest(game_state):
    in_action = game_state["in_action"]
    our_player = game_state["players"][in_action]
    our_cards = our_player["hole_cards"]
    community_cards = game_state["community_cards"]
    first_card = our_cards[0]
    second_card = our_cards[1]
    figures = ["J", "Q", "K", "A"]
    high_cards = ["10", "J", "Q", "K", "A"]
    card_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13,
                 "A": 14}
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
            possible_call_for_pair = [True for card in community_cards if card["rank"] == high_card_rank]
            if possible_call_for_pair:
                return call
            else:
                return 0

    else:
        return 0

json = {
  "tournament_id":"550d1d68cd7bd10003000003",
  "game_id":"550da1cb2d909006e90004b1",
  "round":0,
  "bet_index":0,
  "small_blind": 10,
  "current_buy_in": 320,
  "pot": 400,
  "minimum_raise": 240,
  "dealer": 1,
  "orbits": 7,
  "in_action": 1,
  "players": [
      {
          "id": 0,
          "name": "Albert",
          "status": "active",
          "version": "Default random player",
          "stack": 1010,
          "bet": 320
      },
      {
          "id": 1,
          "name": "Bob",
          "status": "active",
          "version": "Default random player",
          "stack": 1590,
          "bet": 80,
          "hole_cards": [
              {
                  "rank": "K",
                  "suit": "hearts"
              },
              {
                  "rank": "2",
                  "suit": "spades"
              }
          ]
      },
      {
          "id": 2,
          "name": "Chuck",
          "status": "out",
          "version": "Default random player",
          "stack": 0,
          "bet": 0
      }
  ],
  "community_cards": [
      {
          "rank": "4",
          "suit": "spades"
      },
      {
          "rank": "A",
          "suit": "hearts"
      },
      {
          "rank": "6",
          "suit": "clubs"
      }
  ]
}
print betRequest(json)
