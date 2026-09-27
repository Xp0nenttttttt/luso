import random

from games.uno.deck import Deck


class UnoRoom:
    def __init__(
        self,
        room
    ):
        self.room_code = room.code

        self.player_ids = list(
            room.players.keys()
        )

        self.deck = Deck()

        self.hands = {
            player_id: []
            for player_id
            in self.player_ids
        }

        self.discard_pile = []

        self.active_color = None

        self.turn_index = 0

        self.started = False

        self.winner_id = None

        self.start_game()

    # ---------------------------------
    # SERIALIZE CARD
    # ---------------------------------

    def serialize_card(
        self,
        card
    ):
        return {
            "color": card.color,
            "value": card.value
        }

    # ---------------------------------
    # START
    # ---------------------------------

    def start_game(self):

        # 7 cartes par joueur
        for _ in range(7):

            for player_id in self.player_ids:

                card = self.deck.draw()

                self.hands[
                    player_id
                ].append(
                    card
                )

        # Première carte :
        # pas de wild pour simplifier
        while True:

            first_card = self.deck.draw()

            if first_card.color is not None:
                break

        self.discard_pile.append(
            first_card
        )

        self.active_color = (
            first_card.color
        )

        # Joueur aléatoire qui commence
        self.turn_index = (
            random.randrange(
                len(
                    self.player_ids
                )
            )
        )

        self.started = True

    # ---------------------------------
    # JOUEUR ACTUEL
    # ---------------------------------

    def get_current_player_id(self):

        return self.player_ids[
            self.turn_index
        ]

    # ---------------------------------
    # ETAT PERSONNALISE
    # ---------------------------------

    def serialize_for(
        self,
        player_id,
        room
    ):

        players = []

        for other_id in self.player_ids:

            player_data = (
                room.players.get(
                    other_id,
                    {}
                )
            )

            players.append(
                {
                    "id": other_id,

                    "name": player_data.get(
                        "name",
                        "Player"
                    ),

                    "card_count": len(
                        self.hands.get(
                            other_id,
                            []
                        )
                    )
                }
            )

        top_card = (
            self.discard_pile[-1]
        )

        return {
            "room_code":
                self.room_code,

            "your_id":
                player_id,

            "players":
                players,

            "your_hand": [
                self.serialize_card(
                    card
                )
                for card
                in self.hands.get(
                    player_id,
                    []
                )
            ],

            "top_card":
                self.serialize_card(
                    top_card
                ),

            "active_color":
                self.active_color,

            "current_player_id":
                self.get_current_player_id(),

            "winner_id":
                self.winner_id
        }