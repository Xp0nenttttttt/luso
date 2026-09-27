import pygame
from pathlib import Path

from asset_paths import asset_path


class UnoOnline:
    
    COLORS = {
        "red": "#e74c3c",
        "blue": "#3498db",
        "green": "#2ecc71",
        "yellow": "#f1c40f",
        None: "#20242f"
    }


    def __init__(
        self,
        network
    ):
        self.last_action_id = None

        self.card_animation = None

        self.card_animation_duration = 0.28
        self.avatar_cache = {}
        self.theme = {
            "bg": "#0b0e16",
            "table": "#131a27",
            "table_inner": "#182233",

            "panel": "#161b28",
            "panel_alt": "#20283a",

            "border": "#303b52",

            "text": "#ffffff",
            "muted": "#8d97aa",

            "accent": "#62d9ff",
            "success": "#5de39a",

            "red": "#e74c3c",
            "blue": "#3498db",
            "green": "#2ecc71",
            "yellow": "#f1c40f"
        }

        self.card_hover_y = 18
        self.card_rects = []

        self.pending_wild_index = None


        self.draw_rect = pygame.Rect(
            740,
            285,
            150,
            60
        )


        self.color_rects = {
            "red": pygame.Rect(
                440,
                320,
                90,
                90
            ),

            "blue": pygame.Rect(
                540,
                320,
                90,
                90
            ),

            "green": pygame.Rect(
                640,
                320,
                90,
                90
            ),

            "yellow": pygame.Rect(
                740,
                320,
                90,
                90
            )
        }

        self.network = network
        self.replay_rect = pygame.Rect(
            390,
            450,
            230,
            60
        )

        self.lobby_rect = pygame.Rect(
            660,
            450,
            230,
            60
        )
        self.title_font = pygame.font.Font(
            None,
            50
        )

        self.font = pygame.font.Font(
            None,
            30
        )

        self.small_font = pygame.font.Font(
            None,
            22
        )

    # ---------------------------------
    # EVENTS
    # ---------------------------------

    def handle_event(
        self,
        event,
        mouse_pos
    ):

        # =================================================
        # CHOIX COULEUR WILD
        # =================================================

        if (
            self.pending_wild_index
            is not None
        ):

            if (
                event.type
                == pygame.KEYDOWN
                and event.key
                == pygame.K_ESCAPE
            ):

                self.pending_wild_index = None

                return None


            if (
                event.type
                == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):

                for color, rect in (
                    self.color_rects.items()
                ):

                    if rect.collidepoint(
                        mouse_pos
                    ):

                        self.network.uno_play_card(
                            self.pending_wild_index,
                            color
                        )

                        self.pending_wild_index = None

                        return None

            return None


        # =================================================
        # NORMAL
        # =================================================
        state = self.network.uno_state
        if (
            state is not None
            and state.get(
                "winner_id"
            ) is not None
        ):

            if (
                event.type
                == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):

                if self.replay_rect.collidepoint(
                    mouse_pos
                ):

                    self.network.uno_replay_vote()

                    return None


                if self.lobby_rect.collidepoint(
                    mouse_pos
                ):

                    self.network.uno_return_lobby()

                    return None


            # Empêche de jouer des cartes
            # après la fin de partie.
            return None
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                return "back"


        if (
            event.type
            == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):

            state = (
                self.network.uno_state
            )

            if state is None:
                return None


            my_turn = (
                state[
                    "current_player_id"
                ]
                == state[
                    "your_id"
                ]
            )

            if not my_turn:
                return None


            # -------------------------
            # PIOCHER
            # -------------------------

            if self.draw_rect.collidepoint(
                mouse_pos
            ):

                self.network.uno_draw_card()

                return None


            # -------------------------
            # JOUER UNE CARTE
            # -------------------------

            playable = state.get(
                "playable_indices",
                []
            )


            for item in reversed(
                self.card_rects
            ):

                if not item[
                    "rect"
                ].collidepoint(
                    mouse_pos
                ):
                    continue


                index = item[
                    "index"
                ]

                if index not in playable:
                    return None


                card = state[
                    "your_hand"
                ][index]


                # Wild ou +4
                if (
                    card.get(
                        "color"
                    )
                    is None
                ):

                    self.pending_wild_index = (
                        index
                    )

                    return None


                self.network.uno_play_card(
                    index
                )

                return None


        return None

    # ---------------------------------
    # CARTE
    # ---------------------------------

    def draw_card(
        self,
        screen,
        card,
        rect,
        playable=True,
        hovered=False
    ):

        color = self.COLORS.get(
            card.get("color"),
            "#252936"
        )

        # Ombre
        shadow = pygame.Rect(
            rect.x + 5,
            rect.y + 7,
            rect.width,
            rect.height
        )

        pygame.draw.rect(
            screen,
            "#05070c",
            shadow,
            border_radius=12
        )

        # Carte
        pygame.draw.rect(
            screen,
            color,
            rect,
            border_radius=12
        )

        # Zone intérieure
        inner = rect.inflate(
            -14,
            -14
        )

        pygame.draw.ellipse(
            screen,
            "#f5f5f5",
            inner
        )

        # Valeur
        value = str(
            card.get(
                "value",
                "?"
            )
        ).upper()

        text_color = color

        text = self.font.render(
            value,
            True,
            text_color
        )

        screen.blit(
            text,
            text.get_rect(
                center=rect.center
            )
        )

        # Petit symbole en haut
        small = self.small_font.render(
            value,
            True,
            "white"
        )

        screen.blit(
            small,
            (
                rect.x + 9,
                rect.y + 7
            )
        )

        # Carte non jouable
        if not playable:

            overlay = pygame.Surface(
                (
                    rect.width,
                    rect.height
                ),
                pygame.SRCALPHA
            )

            overlay.fill(
                (
                    0,
                    0,
                    0,
                    130
                )
            )

            screen.blit(
                overlay,
                rect.topleft
            )

        # Hover
        if hovered:

            pygame.draw.rect(
                screen,
                self.theme["accent"],
                rect,
                4,
                border_radius=12
            )

        elif playable:

            pygame.draw.rect(
                screen,
                "#e7edf5",
                rect,
                2,
                border_radius=12
            )
    # ---------------------------------
    # DRAW
    # ---------------------------------

    def draw(
        self,
        screen,
        mouse_pos
    ):

        self.draw_background(
            screen
        )

        state = (
            self.network.uno_state
        )

        if state is None:

            loading = self.title_font.render(
                "Connexion à la partie...",
                True,
                "white"
            )

            screen.blit(
                loading,
                loading.get_rect(
                    center=(
                        640,
                        360
                    )
                )
            )

            return


        # =================================================
        # DONNEES
        # =================================================

        my_id = state[
            "your_id"
        ]

        my_turn = (
            state[
                "current_player_id"
            ]
            == my_id
        )

        opponent = (
            self.get_opponent()
        )

        my_player = None

        for player in state[
            "players"
        ]:

            if player[
                "id"
            ] == my_id:

                my_player = player

                break


        # =================================================
        # ROOM
        # =================================================

        room_text = self.small_font.render(
            f"ROOM {state['room_code']}",
            True,
            self.theme["muted"]
        )

        screen.blit(
            room_text,
            (
                25,
                22
            )
        )


        # =================================================
        # TOUR
        # =================================================

        turn_text = (
            "À TON TOUR"
            if my_turn
            else "TOUR DE L'ADVERSAIRE"
        )

        turn_color = (
            self.theme["success"]
            if my_turn
            else self.theme["muted"]
        )

        rendered_turn = (
            self.font.render(
                turn_text,
                True,
                turn_color
            )
        )

        turn_bg = pygame.Rect(
            490,
            18,
            300,
            42
        )

        pygame.draw.rect(
            screen,
            "#151b28",
            turn_bg,
            border_radius=20
        )

        screen.blit(
            rendered_turn,
            rendered_turn.get_rect(
                center=turn_bg.center
            )
        )


        # =================================================
        # ADVERSAIRE
        # =================================================

        if opponent:

            self.draw_player_panel(
                screen,
                opponent["name"],
                opponent.get(
                    "character",
                    "lucie"
                ),
                opponent["card_count"],
                pygame.Rect(
                    80,
                    90,
                    260,
                    75
                ),
                state[
                    "current_player_id"
                ]
                == opponent["id"]
            )

            self.draw_opponent_hand(
                screen,
                opponent
            )


        # =================================================
        # TON PROFIL
        # =================================================

        if my_player:

            self.draw_player_panel(
                screen,
                my_player["name"],
                my_player.get(
                    "character",
                    "lucie"
                ),
                len(
                    state[
                        "your_hand"
                    ]
                ),
                pygame.Rect(
                    80,
                    555,
                    260,
                    75
                ),
                my_turn
            )


        # =================================================
        # CARTE CENTRALE
        # =================================================

        top_card_rect = pygame.Rect(
            595,
            265,
            90,
            130
        )

        self.draw_card(
            screen,
            state[
                "top_card"
            ],
            top_card_rect
        )


        # =================================================
        # PIOCHE
        # =================================================

        self.draw_rect = pygame.Rect(
            760,
            265,
            90,
            130
        )

        self.draw_draw_pile(
            screen,
            mouse_pos,
            my_turn
        )


        # =================================================
        # COULEUR ACTIVE
        # =================================================

        self.draw_active_color(
            screen,
            state[
                "active_color"
            ]
        )


        # =================================================
        # MAIN DU JOUEUR
        # =================================================

        hand = state[
            "your_hand"
        ]

        playable_indices = (
            state.get(
                "playable_indices",
                []
            )
        )

        self.card_rects = []

        card_width = 82
        card_height = 118

        # Les cartes peuvent se chevaucher
        # si la main devient grande.
        if len(hand) <= 10:

            spacing = 67

        else:

            spacing = max(
                35,
                int(
                    670
                    / len(hand)
                )
            )


        total_width = (
            card_width
            + max(
                0,
                len(hand) - 1
            ) * spacing
        )

        start_x = (
            640
            - total_width // 2
        )


        # Détermine d'abord
        # quelle carte est survolée.
        hovered_index = None


        for index in reversed(
            range(
                len(hand)
            )
        ):

            x = (
                start_x
                + index * spacing
            )

            test_rect = pygame.Rect(
                x,
                550,
                card_width,
                card_height
            )

            if test_rect.collidepoint(
                mouse_pos
            ):

                hovered_index = index

                break


        # Dessin
        for index, card in enumerate(
            hand
        ):

            x = (
                start_x
                + index * spacing
            )

            y = 550

            hovered = (
                index
                == hovered_index
            )

            playable = (
                my_turn
                and index
                in playable_indices
            )

            if (
                hovered
                and playable
            ):

                y -= self.card_hover_y


            rect = pygame.Rect(
                x,
                y,
                card_width,
                card_height
            )


            self.draw_card(
                screen,
                card,
                rect,
                playable=playable,
                hovered=(
                    hovered
                    and playable
                )
            )


            self.card_rects.append(
                {
                    "index": index,
                    "rect": rect
                }
            )


        # =================================================
        # MESSAGE D'ERREUR
        # =================================================

        if self.network.last_error:

            error = self.small_font.render(
                self.network.last_error,
                True,
                "#ff7185"
            )

            screen.blit(
                error,
                error.get_rect(
                    center=(
                        640,
                        690
                    )
                )
            )
        self.draw_card_animation(
            screen
        )

        # =================================================
        # VICTOIRE
        # =================================================

        winner_id = state.get(
            "winner_id"
        )

        if winner_id is not None:

            self.draw_end_screen(
                screen,
                mouse_pos,
                state
            )

            return


        # =================================================
        # WILD
        # =================================================

        if (
            self.pending_wild_index
            is not None
        ):

            self.draw_color_selector(
                screen,
                mouse_pos
            )
    def get_opponent(self):

        state = self.network.uno_state

        if state is None:
            return None

        for player in state["players"]:

            if player["id"] != state["your_id"]:
                return player

        return None
    def draw_background(self, screen):

        screen.fill(
            self.theme["bg"]
        )

        # Grand panneau/table
        table_rect = pygame.Rect(
            55,
            70,
            1170,
            575
        )

        pygame.draw.rect(
            screen,
            self.theme["table"],
            table_rect,
            border_radius=28
        )

        pygame.draw.rect(
            screen,
            self.theme["border"],
            table_rect,
            2,
            border_radius=28
        )

        # Centre de la table
        inner_rect = pygame.Rect(
            220,
            180,
            840,
            290
        )

        pygame.draw.rect(
            screen,
            self.theme["table_inner"],
            inner_rect,
            border_radius=150
        )

        pygame.draw.rect(
            screen,
            "#263349",
            inner_rect,
            2,
            border_radius=150
        )
    def draw_card_back(
        self,
        screen,
        rect
    ):

        shadow = pygame.Rect(
            rect.x + 4,
            rect.y + 5,
            rect.width,
            rect.height
        )

        pygame.draw.rect(
            screen,
            "#05070c",
            shadow,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            "#151d30",
            rect,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            "#53698d",
            rect,
            3,
            border_radius=10
        )

        inner = rect.inflate(
            -14,
            -14
        )

        pygame.draw.rect(
            screen,
            "#202c45",
            inner,
            border_radius=8
        )

        # Motif
        center = rect.center

        pygame.draw.circle(
            screen,
            "#5bbfe7",
            center,
            18,
            3
        )

        pygame.draw.circle(
            screen,
            "#334a68",
            center,
            9
        )
    def draw_opponent_hand(
        self,
        screen,
        opponent
    ):

        if opponent is None:
            return

        card_count = opponent.get(
            "card_count",
            0
        )

        card_width = 55
        card_height = 80

        spacing = 28

        total_width = (
            card_width
            + max(
                0,
                card_count - 1
            ) * spacing
        )

        start_x = (
            640
            - total_width // 2
        )

        for index in range(
            card_count
        ):

            rect = pygame.Rect(
                start_x
                + index * spacing,

                105,

                card_width,
                card_height
            )

            self.draw_card_back(
                screen,
                rect
            )
    def draw_player_panel(
        self,
        screen,
        name,
        character,
        card_count,
        rect,
        active=False
    ):
        color = (
            "#21384a"
            if active
            else self.theme["panel"]
        )

        pygame.draw.rect(
            screen,
            color,
            rect,
            border_radius=12
        )

        border = (
            self.theme["accent"]
            if active
            else self.theme["border"]
        )

        pygame.draw.rect(
            screen,
            border,
            rect,
            2,
            border_radius=12
        )

        avatar_center = (
            rect.x + 38,
            rect.centery
        )
        avatar = self.get_avatar(
            character
        )

        if avatar is not None:
            avatar_rect = avatar.get_rect(
                center=avatar_center
            )
            screen.blit(
                avatar,
                avatar_rect
            )
        else:
            pygame.draw.circle(
                screen,
                "#3c4860",
                avatar_center,
                25
            )


        name_text = self.font.render(
            name,
            True,
            self.theme["text"]
        )

        screen.blit(
            name_text,
            (
                rect.x + 80,
                rect.y + 12
            )
        )

        cards_text = self.small_font.render(
            f"{card_count} cartes",
            True,
            self.theme["muted"]
        )

        screen.blit(
            cards_text,
            (
                rect.x + 80,
                rect.y + 45
            )
        )
    def draw_draw_pile(
        self,
        screen,
        mouse_pos,
        enabled
    ):

        rect = self.draw_rect

        # Faux empilement
        for offset in [
            10,
            6,
            3
        ]:

            stack_rect = pygame.Rect(
                rect.x + offset,
                rect.y - offset,
                90,
                130
            )

            pygame.draw.rect(
                screen,
                "#12192a",
                stack_rect,
                border_radius=10
            )

        pile_rect = pygame.Rect(
            rect.x,
            rect.y,
            90,
            130
        )

        self.draw_card_back(
            screen,
            pile_rect
        )

        hovered = (
            pile_rect.collidepoint(
                mouse_pos
            )
            and enabled
        )

        if hovered:

            pygame.draw.rect(
                screen,
                self.theme["accent"],
                pile_rect,
                4,
                border_radius=10
            )

        text = self.small_font.render(
            "PIOCHER",
            True,
            (
                "white"
                if enabled
                else self.theme["muted"]
            )
        )

        screen.blit(
            text,
            text.get_rect(
                center=(
                    pile_rect.centerx,
                    pile_rect.bottom + 25
                )
            )
        )

        # IMPORTANT :
        # le rect utilisé pour cliquer
        # devient celui de la pile.
        self.draw_rect = pile_rect
    def draw_active_color(
        self,
        screen,
        active_color
    ):

        colors = {
            "red": self.theme["red"],
            "blue": self.theme["blue"],
            "green": self.theme["green"],
            "yellow": self.theme["yellow"]
        }

        color = colors.get(
            active_color,
            "#555555"
        )

        label = self.small_font.render(
            "COULEUR ACTIVE",
            True,
            self.theme["muted"]
        )

        screen.blit(
            label,
            label.get_rect(
                center=(
                    640,
                    430
                )
            )
        )

        pygame.draw.circle(
            screen,
            color,
            (
                640,
                463
            ),
            14
        )

        pygame.draw.circle(
            screen,
            "white",
            (
                640,
                463
            ),
            14,
            2
        )
    def draw_end_screen(
        self,
        screen,
        mouse_pos,
        state
    ):

        winner_id = state.get(
            "winner_id"
        )

        overlay = pygame.Surface(
            (
                1280,
                720
            ),
            pygame.SRCALPHA
        )

        overlay.fill(
            (
                5,
                7,
                13,
                220
            )
        )

        screen.blit(
            overlay,
            (0, 0)
        )


        winner_name = "Joueur"

        for player in state[
            "players"
        ]:

            if player[
                "id"
            ] == winner_id:

                winner_name = player[
                    "name"
                ]

                break


        if (
            winner_id
            == state[
                "your_id"
            ]
        ):

            result = "VICTOIRE !"

            color = (
                self.theme["success"]
            )

        else:

            result = (
                f"{winner_name} gagne"
            )

            color = "#ff7285"


        title = self.title_font.render(
            result,
            True,
            color
        )

        screen.blit(
            title,
            title.get_rect(
                center=(
                    640,
                    250
                )
            )
        )


        replay_votes = set(
            state.get(
                "replay_votes",
                []
            )
        )


        votes = self.small_font.render(
            f"Rejouer : "
            f"{len(replay_votes)}"
            f"/"
            f"{state.get('replay_required', 2)}",
            True,
            self.theme["muted"]
        )

        screen.blit(
            votes,
            votes.get_rect(
                center=(
                    640,
                    320
                )
            )
        )


        already_voted = (
            state["your_id"]
            in replay_votes
        )


        # REPLAY
        replay_hover = (
            self.replay_rect
            .collidepoint(
                mouse_pos
            )
        )


        if already_voted:

            replay_color = (
                "#315548"
            )

            replay_label = (
                "EN ATTENTE..."
            )

        else:

            replay_color = (
                "#447b65"
                if not replay_hover
                else "#58a080"
            )

            replay_label = (
                "REJOUER"
            )


        pygame.draw.rect(
            screen,
            replay_color,
            self.replay_rect,
            border_radius=10
        )


        text = self.font.render(
            replay_label,
            True,
            "white"
        )

        screen.blit(
            text,
            text.get_rect(
                center=
                    self.replay_rect.center
            )
        )


        # LOBBY
        lobby_hover = (
            self.lobby_rect
            .collidepoint(
                mouse_pos
            )
        )

        lobby_color = (
            "#343b4e"
            if not lobby_hover
            else "#48536b"
        )

        pygame.draw.rect(
            screen,
            lobby_color,
            self.lobby_rect,
            border_radius=10
        )


        lobby_text = self.font.render(
            "RETOUR AU LOBBY",
            True,
            "white"
        )

        screen.blit(
            lobby_text,
            lobby_text.get_rect(
                center=
                    self.lobby_rect.center
            )
        )
    def draw_color_selector(
        self,
        screen,
        mouse_pos
    ):

        overlay = pygame.Surface(
            (
                1280,
                720
            ),
            pygame.SRCALPHA
        )

        overlay.fill(
            (
                0,
                0,
                0,
                200
            )
        )

        screen.blit(
            overlay,
            (0, 0)
        )


        title = self.title_font.render(
            "CHOISIS UNE COULEUR",
            True,
            "white"
        )

        screen.blit(
            title,
            title.get_rect(
                center=(
                    640,
                    240
                )
            )
        )


        colors = {
            "red": self.theme["red"],
            "blue": self.theme["blue"],
            "green": self.theme["green"],
            "yellow": self.theme["yellow"]
        }


        for color, rect in (
            self.color_rects.items()
        ):

            hovered = (
                rect.collidepoint(
                    mouse_pos
                )
            )

            pygame.draw.rect(
                screen,
                colors[color],
                rect,
                border_radius=14
            )


            if hovered:

                pygame.draw.rect(
                    screen,
                    "white",
                    rect,
                    4,
                    border_radius=14
                )
    def get_avatar(
        self,
        character
    ):
        character = str(
            character or "lucie"
        )

        if (
            Path(character).name != character
            or character in (".", "..")
        ):
            character = "lucie"

        if character in self.avatar_cache:

            return self.avatar_cache[
                character
            ]


        path = asset_path(
            "assets",
            "characters",
            character,
            "pfp.png"
        )


        if not path.is_file():

            path = asset_path(
                "assets",
                "characters",
                "lucie",
                "pfp.png"
            )

        if not path.is_file():

            self.avatar_cache[
                character
            ] = None

            return None


        try:

            image = pygame.image.load(
                path
            ).convert_alpha()

            image = pygame.transform.smoothscale(
                image,
                (
                    52,
                    52
                )
            )

            self.avatar_cache[
                character
            ] = image

            return image

        except pygame.error:

            self.avatar_cache[
                character
            ] = None

            return None
    
    def update(
        self,
        dt
    ):

        state = self.network.uno_state

        if state is None:
            return


        action = state.get(
            "last_action"
        )

        if action is not None:

            action_id = action.get(
                "id"
            )

            if (
                action_id
                != self.last_action_id
            ):

                self.last_action_id = (
                    action_id
                )

                if (
                    action.get("type")
                    == "play_card"
                ):

                    self.start_card_animation(
                        action,
                        state
                    )


        # -----------------------------
        # UPDATE ANIMATION
        # -----------------------------

        if self.card_animation:

            self.card_animation[
                "time"
            ] += dt

            if (
                self.card_animation["time"]
                >= self.card_animation_duration
            ):

                self.card_animation = None
    
    def start_card_animation(
        self,
        action,
        state
    ):

        player_id = action.get(
            "player_id"
        )

        card = action.get(
            "card"
        )

        if card is None:
            return


        # Moi = depuis le bas
        if (
            player_id
            == state["your_id"]
        ):

            start = (
                640,
                600
            )

        # Adversaire = depuis le haut
        else:

            start = (
                640,
                145
            )


        end = (
            640,
            330
        )


        self.card_animation = {
            "card": card,
            "start": start,
            "end": end,
            "time": 0.0
        }
    
    def draw_card_animation(
        self,
        screen
    ):

        animation = (
            self.card_animation
        )

        if animation is None:
            return


        progress = (
            animation["time"]
            / self.card_animation_duration
        )

        progress = max(
            0,
            min(
                1,
                progress
            )
        )


        # Petit easing
        progress = (
            1
            - (1 - progress) ** 3
        )


        start_x, start_y = (
            animation["start"]
        )

        end_x, end_y = (
            animation["end"]
        )


        x = (
            start_x
            + (
                end_x
                - start_x
            )
            * progress
        )

        y = (
            start_y
            + (
                end_y
                - start_y
            )
            * progress
        )


        # La carte grossit légèrement
        scale = (
            0.85
            + 0.15 * progress
        )

        width = int(
            90 * scale
        )

        height = int(
            130 * scale
        )


        rect = pygame.Rect(
            0,
            0,
            width,
            height
        )

        rect.center = (
            int(x),
            int(y)
        )


        self.draw_card(
            screen,
            animation["card"],
            rect,
            playable=True,
            hovered=False
        )