import random

try:
    from .card import Card
except ImportError:  # exécution directe du script
    from card import Card


class Deck:
    def __init__(self):
        self.cards = []

        self.create_deck()

        self.shuffle()

    # -----------------------------
    # CREATION DU PAQUET
    # -----------------------------

    def create_deck(self):

        colors = [
            "red",
            "blue",
            "green",
            "yellow"
        ]

        # -------------------------
        # CARTES COLOREES
        # -------------------------

        for color in colors:

            # Un seul 0 par couleur
            self.cards.append(
                Card(
                    color,
                    0
                )
            )

            # Deux cartes de chaque nombre
            # de 1 à 9
            for number in range(1, 10):

                self.cards.append(
                    Card(
                        color,
                        number
                    )
                )

                self.cards.append(
                    Card(
                        color,
                        number
                    )
                )


            # -------------------------
            # CARTES SPECIALES
            # -------------------------

            special_cards = [
                "skip",
                "reverse",
                "+2"
            ]

            for special in special_cards:

                # 2 cartes de chaque type
                self.cards.append(
                    Card(
                        color,
                        special
                    )
                )

                self.cards.append(
                    Card(
                        color,
                        special
                    )
                )


        # -------------------------
        # JOKERS
        # -------------------------

        for _ in range(4):

            self.cards.append(
                Card(
                    None,
                    "wild"
                )
            )


        # -------------------------
        # +4
        # -------------------------

        for _ in range(4):

            self.cards.append(
                Card(
                    None,
                    "+4"
                )
            )

    # -----------------------------
    # MELANGER
    # -----------------------------

    def shuffle(self):

        random.shuffle(
            self.cards
        )

    # -----------------------------
    # PIOCHER
    # -----------------------------

    def draw(self):

        if len(self.cards) == 0:
            return None

        return self.cards.pop()

    # -----------------------------
    # NOMBRE DE CARTES
    # -----------------------------

    def remaining_cards(self):

        return len(
            self.cards
        )