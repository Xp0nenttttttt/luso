class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __repr__(self):
        return f"Card({self.color}, {self.value})"

    def __str__(self):
        if self.color is None:
            return str(self.value)

        return f"{self.color} {self.value}"

    def is_playable_on(self, other_card):
        """
        Vérifie si cette carte peut être jouée
        sur la carte actuellement posée.
        """

        # Joker = toujours jouable
        if self.color is None:
            return True

        # Même couleur
        if self.color == other_card.color:
            return True

        # Même valeur
        if self.value == other_card.value:
            return True

        return False