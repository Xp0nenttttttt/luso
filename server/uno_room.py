import random

from games.uno.deck import Deck


class UnoRoom:

    VALID_COLORS = [
        "red",
        "blue",
        "green",
        "yellow"
    ]

    def __init__(
        self,
        room
    ):

        self.room_code = room.code
        self.replay_votes = set()
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

        self.turn_index = self.player_ids.index(
            room.host_id
        )

        self.winner_id = None

        self.started = False

        self.start_game()

    # =================================================
    # CARDS
    # =================================================

    def serialize_card(
        self,
        card
    ):

        return {
            "color": card.color,
            "value": card.value
        }

    # =================================================
    # START
    # =================================================

    def start_game(self):

        for _ in range(7):

            for player_id in self.player_ids:

                self.hands[
                    player_id
                ].append(
                    self.draw_from_deck()
                )

        # Première carte simple :
        # on évite les Wild et les effets
        while True:

            card = self.draw_from_deck()

            if (
                card.color is not None
                and card.value not in [
                    "skip",
                    "reverse",
                    "+2"
                ]
            ):
                break

            self.deck.cards.insert(
                0,
                card
            )

        self.discard_pile.append(
            card
        )

        self.active_color = (
            card.color
        )

        self.started = True

    # =================================================
    # DECK
    # =================================================

    def recycle_deck(self):

        if len(
            self.discard_pile
        ) <= 1:
            return False

        top_card = (
            self.discard_pile.pop()
        )

        recycled = (
            self.discard_pile[:]
        )

        self.discard_pile = [
            top_card
        ]

        random.shuffle(
            recycled
        )

        self.deck.cards.extend(
            recycled
        )

        return True

    def draw_from_deck(self):

        card = self.deck.draw()

        if card is not None:
            return card

        if not self.recycle_deck():
            raise ValueError(
                "Plus aucune carte disponible."
            )

        card = self.deck.draw()

        if card is None:
            raise ValueError(
                "Impossible de piocher."
            )

        return card

    # =================================================
    # TURN
    # =================================================

    def get_current_player_id(self):

        return self.player_ids[
            self.turn_index
        ]

    def next_turn(self):

        self.turn_index = (
            self.turn_index + 1
        ) % len(
            self.player_ids
        )

    def is_player_turn(
        self,
        player_id
    ):

        return (
            self.get_current_player_id()
            == player_id
        )

    # =================================================
    # PLAYABLE
    # =================================================

    def is_card_playable(
        self,
        card
    ):

        top_card = (
            self.discard_pile[-1]
        )

        # Wild / +4
        if card.color is None:
            return True

        # Même couleur active
        if (
            card.color
            == self.active_color
        ):
            return True

        # Même valeur
        if (
            card.value
            == top_card.value
        ):
            return True

        return False

    # =================================================
    # DRAW MULTIPLE
    # =================================================

    def draw_cards(
        self,
        player_id,
        amount
    ):

        for _ in range(amount):

            self.hands[
                player_id
            ].append(
                self.draw_from_deck()
            )

    # =================================================
    # PLAY CARD
    # =================================================

    def play_card(
        self,
        player_id,
        hand_index,
        chosen_color=None
    ):

        if self.winner_id:
            raise ValueError(
                "La partie est terminée."
            )

        if not self.is_player_turn(
            player_id
        ):
            raise ValueError(
                "Ce n'est pas ton tour."
            )

        hand = self.hands[
            player_id
        ]

        if (
            hand_index < 0
            or hand_index >= len(hand)
        ):
            raise ValueError(
                "Carte invalide."
            )

        card = hand[
            hand_index
        ]

        if not self.is_card_playable(
            card
        ):
            raise ValueError(
                "Cette carte n'est pas jouable."
            )

        # Wild / +4 :
        # la couleur doit être choisie
        if card.color is None:

            if (
                chosen_color
                not in self.VALID_COLORS
            ):
                raise ValueError(
                    "Choisis une couleur."
                )

        # Retire de la main
        card = hand.pop(
            hand_index
        )

        self.discard_pile.append(
            card
        )

        # Couleur active
        if card.color is None:

            self.active_color = (
                chosen_color
            )

        else:

            self.active_color = (
                card.color
            )

        # -----------------------------
        # VICTOIRE
        # -----------------------------

        if len(hand) == 0:

            self.winner_id = (
                player_id
            )

            return

        # -----------------------------
        # ADVERSAIRE
        # -----------------------------

        opponent_index = (
            self.turn_index + 1
        ) % len(
            self.player_ids
        )

        opponent_id = (
            self.player_ids[
                opponent_index
            ]
        )

        # -----------------------------
        # SKIP
        # -----------------------------

        if card.value == "skip":

            # À 2 joueurs :
            # l'adversaire saute son tour.
            # Le joueur rejoue.
            return

        # -----------------------------
        # REVERSE
        # -----------------------------

        if card.value == "reverse":

            # Même comportement que Skip
            # avec seulement 2 joueurs.
            return

        # -----------------------------
        # +2
        # -----------------------------

        if card.value == "+2":

            self.draw_cards(
                opponent_id,
                2
            )

            # L'adversaire saute son tour
            return

        # -----------------------------
        # +4
        # -----------------------------

        if card.value == "+4":

            self.draw_cards(
                opponent_id,
                4
            )

            # L'adversaire saute son tour
            return

        # -----------------------------
        # NORMAL / WILD
        # -----------------------------

        self.next_turn()

    # =================================================
    # DRAW ONE
    # =================================================

    def draw_card(
        self,
        player_id
    ):

        if self.winner_id:
            raise ValueError(
                "La partie est terminée."
            )

        if not self.is_player_turn(
            player_id
        ):
            raise ValueError(
                "Ce n'est pas ton tour."
            )

        card = self.draw_from_deck()

        self.hands[
            player_id
        ].append(
            card
        )

        # Dans notre règle :
        # piocher termine le tour.
        self.next_turn()

    # =================================================
    # SERIALIZE
    # =================================================

    def serialize_for(
        self,
        player_id,
        room
    ):

        players = []

        for other_id in self.player_ids:

            data = room.players.get(
                other_id,
                {}
            )

            players.append(
                {
                    "id": other_id,

                    "name": data.get(
                        "name",
                        "Player"
                    ),

                    "card_count": len(
                        self.hands.get(
                            other_id,
                            []
                        )
                    ),
                    
                }
            )

        hand = self.hands.get(
            player_id,
            []
        )

        playable_indices = []

        if self.winner_id is None:

            for index, card in enumerate(
                hand
            ):

                if self.is_card_playable(
                    card
                ):

                    playable_indices.append(
                        index
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
                for card in hand
            ],

            "playable_indices":
                playable_indices,

            "top_card":
                self.serialize_card(
                    self.discard_pile[-1]
                ),

            "active_color":
                self.active_color,

            "current_player_id":
                self.get_current_player_id(),

            "winner_id":
                self.winner_id,
            "replay_votes": list(
                self.replay_votes
            ),
            
            "replay_required": len(
                self.player_ids
            ),
        }
    # =================================================
    # REPLAY
    # =================================================

    def vote_replay(
        self,
        player_id
    ):
        if self.winner_id is None:
            raise ValueError(
                "La partie n'est pas terminée."
            )

        if player_id not in self.player_ids:
            raise ValueError(
                "Joueur invalide."
            )

        self.replay_votes.add(
            player_id
        )


    def wants_replay(
        self,
        player_id
    ):
        return (
            player_id
            in self.replay_votes
        )


    def everyone_wants_replay(self):
        return (
            len(self.replay_votes)
            == len(self.player_ids)
        )