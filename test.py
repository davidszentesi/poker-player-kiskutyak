def betRequest(game_state):
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
        # Player.log(self, "Pair in hand bet")
        return game_state["current_buy_in"] - our_player["bet"] + game_state["minimum_raise"]

    elif (first_card["rank"] >= 7 and second_card["rank"] in figures) or (
            second_card["rank"] >= 7 and first_card["rank"] in figures):

        if call < our_player["stack"] * 0.1:
            return call
        else:
            return 20

    else:
        return 20


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
                  "rank": "K",
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
