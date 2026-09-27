import pygame

from games.uno.deck import Deck


class UnoGame:
    def __init__(self, progression):
        self.progression = progression
        # -----------------------------
        # FONTS
        # -----------------------------

        self.title_font = pygame.font.Font(None, 55)
        self.font = pygame.font.Font(None, 32)
        self.card_font = pygame.font.Font(None, 38)
        self.small_font = pygame.font.Font(None, 24)

        # -----------------------------
        # TAILLE DES CARTES
        # -----------------------------

        self.card_width = 90
        self.card_height = 130

        # -----------------------------
        # BOUTONS
        # -----------------------------

        self.draw_button = pygame.Rect(
            780,
            315,
            160,
            55
        )

        self.restart_button = pygame.Rect(
            540,
            450,
            200,
            60
        )

        # Rectangles des cartes du joueur
        self.player_card_rects = []
        # -----------------------------
        # CHOIX DE COULEUR JOKER
        # -----------------------------

        self.color_buttons = {
            "red": pygame.Rect(390, 340, 110, 60),
            "blue": pygame.Rect(520, 340, 110, 60),
            "green": pygame.Rect(650, 340, 110, 60),
            "yellow": pygame.Rect(780, 340, 110, 60)
}
        # -----------------------------
        # COULEURS
        # -----------------------------

        self.colors = {
            "red": "#d94a4a",
            "blue": "#4385d8",
            "green": "#48a868",
            "yellow": "#e5c84c"
        }

        self.reset_game()

    # -----------------------------
    # NOUVELLE PARTIE
    # -----------------------------

    def reset_game(self):

        self.deck = Deck()
        self.earned_xp = 0
        self.xp_given = False

        self.unlocked_rewards = []
        self.player_hand = []
        self.bot_hand = []

        self.discard_pile = []

        self.turn = "player"

        self.winner = None

        self.active_color = None

        self.message = "A ton tour"
        # Aucun choix de couleur en attente
        self.pending_color_choice = False

        self.pending_wild_card = None

        self.pending_wild_player = None
        # Timer du bot
        self.bot_action_time = None

        # -------------------------
        # DISTRIBUTION
        # -------------------------

        for _ in range(7):

            self.player_hand.append(
                self.deck.draw()
            )

            self.bot_hand.append(
                self.deck.draw()
            )

        # -------------------------
        # PREMIERE CARTE
        # -------------------------

        self.create_first_card()

    # -----------------------------
    # PREMIERE CARTE
    # -----------------------------

    def create_first_card(self):

        while True:

            card = self.deck.draw()

            # On évite de commencer
            # directement sur un Joker.
            if card.color is not None:

                self.discard_pile.append(
                    card
                )

                self.active_color = card.color

                break

            # Remet le Joker dans le paquet
            self.deck.cards.insert(
                0,
                card
            )

            self.deck.shuffle()

    # -----------------------------
    # CARTE AU CENTRE
    # -----------------------------

    def get_top_card(self):

        return self.discard_pile[-1]

    # -----------------------------
    # VERIFIER SI JOUABLE
    # -----------------------------

    def can_play(self, card):

        top_card = self.get_top_card()

        # Joker
        if card.color is None:
            return True

        # Même couleur active
        if card.color == self.active_color:
            return True

        # Même valeur
        if card.value == top_card.value:
            return True

        return False

    # -----------------------------
    # PIOCHE
    # -----------------------------

    def draw_card(self):

        # Si la pioche est vide,
        # on recycle la défausse.
        if self.deck.remaining_cards() == 0:

            self.recycle_discard_pile()

        return self.deck.draw()

    # -----------------------------
    # RECYCLER LA DEFAUSSE
    # -----------------------------

    def recycle_discard_pile(self):

        if len(self.discard_pile) <= 1:
            return

        # On garde la dernière carte
        top_card = self.discard_pile.pop()

        # Toutes les autres retournent
        # dans la pioche
        self.deck.cards.extend(
            self.discard_pile
        )

        self.discard_pile = [
            top_card
        ]

        self.deck.shuffle()

    # -----------------------------
    # CHOIX COULEUR JOKER
    # -----------------------------

    def choose_best_color(self, hand):

        counts = {
            "red": 0,
            "blue": 0,
            "green": 0,
            "yellow": 0
        }

        for card in hand:

            if card.color in counts:

                counts[
                    card.color
                ] += 1

        # Choisit la couleur la plus présente
        best_color = max(
            counts,
            key=counts.get
        )

        return best_color
    # -----------------------------
    # FAIRE PIOCHER PLUSIEURS CARTES
    # -----------------------------

    def draw_cards(self, hand, amount):

        for _ in range(amount):

            card = self.draw_card()

            if card is not None:
                hand.append(card)


    # -----------------------------
    # TOUR NORMAL SUIVANT
    # -----------------------------

    def next_turn(self, player_type):

        if player_type == "player":

            self.turn = "bot"

            self.message = "Tour du bot..."

            self.bot_action_time = (
                pygame.time.get_ticks()
                + 650
            )

        else:

            self.turn = "player"

            self.message = "A ton tour"

            self.bot_action_time = None


    # -----------------------------
    # MEME JOUEUR REJOUE
    # -----------------------------

    def repeat_turn(self, player_type):

        if player_type == "player":

            self.turn = "player"

            self.message = "Le bot passe son tour !"

            self.bot_action_time = None

        else:

            self.turn = "bot"

            self.message = "Tu passes ton tour !"

            self.bot_action_time = (
                pygame.time.get_ticks()
                + 650
            )


    # -----------------------------
    # EFFETS DES CARTES
    # -----------------------------

    def apply_card_effect(
        self,
        card,
        player_type
    ):

        # -------------------------
        # SKIP
        # -------------------------

        if card.value == "skip":

            self.repeat_turn(
                player_type
            )

            return


        # -------------------------
        # REVERSE
        # -------------------------
        #
        # À 2 joueurs :
        # Reverse = Skip

        if card.value == "reverse":

            self.repeat_turn(
                player_type
            )

            return


        # -------------------------
        # +2
        # -------------------------

        if card.value == "+2":

            if player_type == "player":

                self.draw_cards(
                    self.bot_hand,
                    2
                )

            else:

                self.draw_cards(
                    self.player_hand,
                    2
                )

            self.repeat_turn(
                player_type
            )

            return


        # -------------------------
        # +4
        # -------------------------

        if card.value == "+4":

            if player_type == "player":

                self.draw_cards(
                    self.bot_hand,
                    4
                )

            else:

                self.draw_cards(
                    self.player_hand,
                    4
                )

            self.repeat_turn(
                player_type
            )

            return


        # -------------------------
        # CARTE NORMALE / WILD
        # -------------------------

        self.next_turn(
            player_type
        )
    
    def give_end_game_xp(self):

        if self.xp_given:
            return

        if self.winner is None:
            return


        # XP pour avoir terminé
        xp_amount = 20


        # Bonus victoire
        if self.winner == "player":

            xp_amount += 50


        rewards = self.progression.add_xp(
            xp_amount
        )
        self.earned_xp = xp_amount

        self.unlocked_rewards = rewards
        self.xp_given = True


        # Petit message console temporaire
        print(
            f"+{xp_amount} XP"
        )


        for reward in rewards:

            print(
                f"NOUVELLE RECOMPENSE : {reward}"
            )

    # -----------------------------
    # CHOISIR COULEUR DU JOKER
    # -----------------------------

    def select_wild_color(
        self,
        color
    ):

        if not self.pending_color_choice:
            return

        self.active_color = color

        card = self.pending_wild_card

        player_type = (
            self.pending_wild_player
        )

        self.pending_color_choice = False

        self.pending_wild_card = None

        self.pending_wild_player = None

        # Maintenant seulement
        # on applique l'effet du Joker

        self.apply_card_effect(
            card,
            player_type
        )
    # -----------------------------
    # JOUER UNE CARTE
    # -----------------------------

    def play_card(
        self,
        hand,
        index,
        player_type
    ):

        card = hand.pop(
            index
        )

        self.discard_pile.append(
            card
        )


        # -----------------------------
        # VICTOIRE
        # -----------------------------

        if len(hand) == 0:

            # Met quand même une couleur
            # active cohérente
            if card.color is not None:

                self.active_color = (
                    card.color
                )

            self.winner = (
                player_type
            )

            if player_type == "player":

                self.message = (
                    "VICTOIRE !"
                )

            else:

                self.message = (
                    "Le bot a gagne"
                )

            return


        # -----------------------------
        # JOKER / +4
        # -----------------------------

        if card.color is None:

            # -------------------------
            # JOUEUR
            # -------------------------

            if player_type == "player":

                self.pending_color_choice = (
                    True
                )

                self.pending_wild_card = (
                    card
                )

                self.pending_wild_player = (
                    player_type
                )

                self.message = (
                    "Choisis une couleur"
                )

                return


            # -------------------------
            # BOT
            # -------------------------

            else:

                self.active_color = (
                    self.choose_best_color(
                        self.bot_hand
                    )
                )

                self.apply_card_effect(
                    card,
                    player_type
                )

                return


        # -----------------------------
        # CARTE NORMALE
        # -----------------------------

        self.active_color = (
            card.color
        )

        self.apply_card_effect(
            card,
            player_type
        )
    # -----------------------------
    # PIOCHE JOUEUR
    # -----------------------------

    def player_draw(self):

        if self.turn != "player":
            return

        card = self.draw_card()

        if card is not None:

            self.player_hand.append(
                card
            )

        # Pour cette V1 :
        # piocher termine le tour.
        self.turn = "bot"

        self.message = "Tour du bot..."

        self.bot_action_time = (
            pygame.time.get_ticks()
            + 650
        )

    # -----------------------------
    # BOT
    # -----------------------------

    def bot_turn(self):

        if self.turn != "bot":
            return

        # Cherche une carte jouable
        for index, card in enumerate(
            self.bot_hand
        ):

            if self.can_play(card):

                self.play_card(
                    self.bot_hand,
                    index,
                    "bot"
                )

                return

        # -------------------------
        # AUCUNE CARTE
        # -------------------------

        new_card = self.draw_card()

        if new_card is not None:

            self.bot_hand.append(
                new_card
            )

            # Si la carte piochée est jouable,
            # le bot la joue directement.
            if self.can_play(new_card):

                self.play_card(
                    self.bot_hand,
                    len(self.bot_hand) - 1,
                    "bot"
                )

                return

        # Sinon il passe son tour
        self.turn = "player"

        self.message = "A ton tour"

        self.bot_action_time = None

    # -----------------------------
    # UPDATE
    # -----------------------------

    def update(self):

        if self.winner is not None:
            self.give_end_game_xp()
            return

        if (
            self.turn == "bot"
            and self.bot_action_time is not None
        ):

            if (
                pygame.time.get_ticks()
                >= self.bot_action_time
            ):

                self.bot_turn()

    # -----------------------------
    # EVENTS
    # -----------------------------

    def handle_event(
        self,
        event,
        mouse_pos
    ):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        if event.button != 1:
            return
        # -------------------------
        # CHOIX COULEUR JOKER
        # -------------------------

        if self.pending_color_choice:

            for color, rect in (
                self.color_buttons.items()
            ):

                if rect.collidepoint(
                    mouse_pos
                ):

                    self.select_wild_color(
                        color
                    )

                    return

            # Tant que la couleur
            # n'est pas choisie,
            # aucun autre clic ne fonctionne.

            return
        # -------------------------
        # FIN DE PARTIE
        # -------------------------

        if self.winner is not None:

            if self.restart_button.collidepoint(
                mouse_pos
            ):

                self.reset_game()

            return

        # Le joueur ne peut cliquer
        # que pendant son tour.
        if self.turn != "player":
            return

        # -------------------------
        # PIOCHER
        # -------------------------

        if self.draw_button.collidepoint(
            mouse_pos
        ):

            self.player_draw()

            return

        # -------------------------
        # CARTES DU JOUEUR
        # -------------------------

        # On parcourt à l'envers car
        # les cartes peuvent se chevaucher.
        for index in range(
            len(self.player_card_rects) - 1,
            -1,
            -1
        ):

            rect = self.player_card_rects[
                index
            ]

            if rect.collidepoint(
                mouse_pos
            ):

                card = self.player_hand[
                    index
                ]

                if self.can_play(card):

                    self.play_card(
                        self.player_hand,
                        index,
                        "player"
                    )

                else:

                    self.message = (
                        "Cette carte n'est pas jouable"
                    )

                break

    # -----------------------------
    # DESSINER UNE CARTE
    # -----------------------------

    def draw_card_visual(
        self,
        screen,
        card,
        rect
    ):

        # Joker
        if card.color is None:

            color = "#222222"

            text_color = "white"

        else:

            color = self.colors[
                card.color
            ]

            if card.color == "yellow":
                text_color = "#222222"
            else:
                text_color = "white"

        # Carte
        pygame.draw.rect(
            screen,
            color,
            rect,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            "white",
            rect,
            width=4,
            border_radius=10
        )

        # -------------------------
        # TEXTE
        # -------------------------

        value = str(
            card.value
        ).upper()

        if value == "REVERSE":
            value = "REV"

        elif value == "SKIP":
            value = "SKIP"

        elif value == "WILD":
            value = "WILD"

        text = self.card_font.render(
            value,
            True,
            text_color
        )

        text_rect = text.get_rect(
            center=rect.center
        )

        screen.blit(
            text,
            text_rect
        )
    
    def draw_color_picker(
        self,
        screen,
        mouse_pos
    ):

        if not self.pending_color_choice:
            return


        # -----------------------------
        # OVERLAY
        # -----------------------------

        overlay = pygame.Surface(
            (1280, 720),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 160)
        )

        screen.blit(
            overlay,
            (0, 0)
        )


        # -----------------------------
        # PANEL
        # -----------------------------

        panel = pygame.Rect(
            330,
            250,
            620,
            220
        )

        pygame.draw.rect(
            screen,
            "#202431",
            panel,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            "white",
            panel,
            3,
            border_radius=12
        )


        title = self.font.render(
            "Choisis une couleur",
            True,
            "white"
        )

        title_rect = title.get_rect(
            center=(640, 295)
        )

        screen.blit(
            title,
            title_rect
        )


        # -----------------------------
        # COULEURS
        # -----------------------------

        for color, rect in (
            self.color_buttons.items()
        ):

            draw_rect = rect.copy()

            if rect.collidepoint(
                mouse_pos
            ):

                draw_rect = rect.inflate(
                    8,
                    8
                )

            pygame.draw.rect(
                screen,
                self.colors[color],
                draw_rect,
                border_radius=8
            )

            pygame.draw.rect(
                screen,
                "white",
                draw_rect,
                3,
                border_radius=8
            )
    # -----------------------------
    # CARTE CACHEE DU BOT
    # -----------------------------

    def draw_hidden_card(
        self,
        screen,
        rect
    ):

        # -----------------------------
        # DOS DE CARTE EQUIPE
        # -----------------------------

        profile = (
            self.progression
            .stats
            .data
            .get(
                "profile",
                {}
            )
        )


        card_back = profile.get(
            "card_back",
            "default"
        )


        # -----------------------------
        # STYLES
        # -----------------------------

        styles = {

            "default": {
                "background": "#292d7a",
                "detail": "#555bc0"
            },

            "retro_blue": {
                "background": "#163b78",
                "detail": "#5fa8ff"
            }
        }


        style = styles.get(
            card_back,
            styles["default"]
        )


        # -----------------------------
        # CARTE
        # -----------------------------

        pygame.draw.rect(
            screen,
            style["background"],
            rect,
            border_radius=8
        )


        pygame.draw.rect(
            screen,
            "white",
            rect,
            3,
            border_radius=8
        )


        pygame.draw.rect(
            screen,
            style["detail"],
            rect.inflate(
                -18,
                -18
            ),
            3,
            border_radius=5
        )


    # -----------------------------
    # MAIN DRAW
    # -----------------------------

    def draw(
        self,
        screen,
        mouse_pos
    ):

        screen.fill(
            "#176b3a"
        )

        # -------------------------
        # TITRE
        # -------------------------

        title = self.title_font.render(
            "UNO",
            True,
            "white"
        )

        title_rect = title.get_rect(
            center=(640, 32)
        )

        screen.blit(
            title,
            title_rect
        )

        # -------------------------
        # MAIN DU BOT
        # -------------------------

        bot_count = len(
            self.bot_hand
        )

        bot_text = self.small_font.render(
            f"BOT - {bot_count} cartes",
            True,
            "white"
        )

        bot_text_rect = bot_text.get_rect(
            center=(640, 70)
        )

        screen.blit(
            bot_text,
            bot_text_rect
        )

        if bot_count > 0:

            spacing = min(
                45,
                500 / max(
                    1,
                    bot_count
                )
            )

            total_width = (
                self.card_width
                + spacing * (
                    bot_count - 1
                )
            )

            start_x = (
                640 - total_width / 2
            )

            for index in range(
                bot_count
            ):

                rect = pygame.Rect(
                    start_x + index * spacing,
                    90,
                    self.card_width,
                    self.card_height
                )

                self.draw_hidden_card(
                    screen,
                    rect
                )

        # -------------------------
        # PIOCHE
        # -------------------------

        deck_rect = pygame.Rect(
            430,
            280,
            self.card_width,
            self.card_height
        )

        self.draw_hidden_card(
            screen,
            deck_rect
        )

        deck_count = self.small_font.render(
            str(
                self.deck.remaining_cards()
            ),
            True,
            "white"
        )

        deck_count_rect = (
            deck_count.get_rect(
                center=(
                    deck_rect.centerx,
                    deck_rect.bottom + 18
                )
            )
        )

        screen.blit(
            deck_count,
            deck_count_rect
        )

        # -------------------------
        # CARTE CENTRALE
        # -------------------------

        top_rect = pygame.Rect(
            595,
            280,
            self.card_width,
            self.card_height
        )

        self.draw_card_visual(
            screen,
            self.get_top_card(),
            top_rect
        )

        # -------------------------
        # COULEUR ACTIVE
        # -------------------------

        active_text = self.small_font.render(
            "Couleur active",
            True,
            "white"
        )

        screen.blit(
            active_text,
            (590, 425)
        )

        active_rect = pygame.Rect(
            700,
            424,
            22,
            22
        )

        pygame.draw.rect(
            screen,
            self.colors[
                self.active_color
            ],
            active_rect
        )

        pygame.draw.rect(
            screen,
            "white",
            active_rect,
            2
        )

        # -------------------------
        # BOUTON PIOCHER
        # -------------------------

        if (
            self.turn == "player"
            and self.draw_button.collidepoint(
                mouse_pos
            )
        ):

            button_color = "#6b76df"

        else:

            button_color = "#5059b8"

        pygame.draw.rect(
            screen,
            button_color,
            self.draw_button,
            border_radius=8
        )

        draw_text = self.font.render(
            "PIOCHER",
            True,
            "white"
        )

        draw_text_rect = draw_text.get_rect(
            center=self.draw_button.center
        )

        screen.blit(
            draw_text,
            draw_text_rect
        )

        # -------------------------
        # MESSAGE
        # -------------------------

        message_text = self.font.render(
            self.message,
            True,
            "white"
        )

        message_rect = (
            message_text.get_rect(
                center=(640, 480)
            )
        )

        screen.blit(
            message_text,
            message_rect
        )

        # -------------------------
        # MAIN DU JOUEUR
        # -------------------------

        self.player_card_rects = []

        card_count = len(
            self.player_hand
        )

        if card_count > 0:

            max_width = 1100

            if card_count == 1:
                spacing = 0

            else:

                spacing = min(
                    100,
                    (
                        max_width
                        - self.card_width
                    )
                    / (
                        card_count - 1
                    )
                )

            total_width = (
                self.card_width
                + spacing * (
                    card_count - 1
                )
            )

            start_x = (
                640
                - total_width / 2
            )

            for index, card in enumerate(
                self.player_hand
            ):

                rect = pygame.Rect(
                    start_x
                    + index * spacing,
                    555,
                    self.card_width,
                    self.card_height
                )

                # Carte jouable :
                # légèrement remontée
                if (
                    self.turn == "player"
                    and self.can_play(card)
                ):

                    rect.y -= 10

                self.player_card_rects.append(
                    rect
                )

                self.draw_card_visual(
                    screen,
                    card,
                    rect
                )
        # -------------------------
        # CHOIX COULEUR JOKER
        # -------------------------

        self.draw_color_picker(
            screen,
            mouse_pos
        )
        # -------------------------
        # FIN DE PARTIE
        # -------------------------

        if self.winner is not None:

            overlay = pygame.Surface(
                (1280, 720),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 170)
            )

            screen.blit(
                overlay,
                (0, 0)
            )

            if self.winner == "player":

                result = "VICTOIRE !"

            else:

                result = "DEFAITE"

            result_text = self.title_font.render(
                result,
                True,
                "white"
            )

            result_rect = result_text.get_rect(
                center=(640, 330)
            )

            screen.blit(
                result_text,
                result_rect
            )

            pygame.draw.rect(
                screen,
                "#5f78ff",
                self.restart_button,
                border_radius=8
            )
            xp_text = self.font.render(
                f"+{self.earned_xp} XP",
                True,
                "#f5c45f"
            )

            xp_rect = xp_text.get_rect(
                center=(640, 380)
            )

            screen.blit(
                xp_text,
                xp_rect
            )
            restart_text = self.font.render(
                "REJOUER",
                True,
                "white"
            )

            restart_rect = (
                restart_text.get_rect(
                    center=self.restart_button.center
                )
            )

            screen.blit(
                restart_text,
                restart_rect
            )

        # -------------------------
        # RETOUR
        # -------------------------

        back_text = self.small_font.render(
            "ESC - Quitter la partie",
            True,
            "white"
        )

        screen.blit(
            back_text,
            (20, 685)
        )