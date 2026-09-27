try:
    from games.uno.deck import Deck
    from games.uno.card import Card
except ModuleNotFoundError:
    from deck import Deck
    from card import Card


top_card = Card(
    "red",
    7
)


card1 = Card(
    "red",
    3
)

card2 = Card(
    "blue",
    7
)

card3 = Card(
    "green",
    4
)

card4 = Card(
    None,
    "wild"
)


print(
    card1.is_playable_on(top_card)
)

print(
    card2.is_playable_on(top_card)
)

print(
    card3.is_playable_on(top_card)
)

print(
    card4.is_playable_on(top_card)
)

deck = Deck()


print(
    "Nombre de cartes :",
    deck.remaining_cards()
)


print("\n5 cartes piochées :")

for _ in range(5):

    card = deck.draw()

    print(card)


print(
    "\nCartes restantes :",
    deck.remaining_cards()
)