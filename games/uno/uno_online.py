import pygame


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
        rect
    ):

        color = self.COLORS.get(
            card.get(
                "color"
            ),
            "#252936"
        )

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
            3,
            border_radius=10
        )

        value = str(
            card.get(
                "value",
                "?"
            )
        )

        text = self.font.render(
            value,
            True,
            "white"
        )

        screen.blit(
            text,
            text.get_rect(
                center=rect.center
            )
        )

    def draw_game_over(
        self,
        screen,
        state,
        mouse_pos
    ):

        overlay = pygame.Surface(
            (1280, 720),
            pygame.SRCALPHA
        )
        overlay.fill((5, 7, 13, 220))
        screen.blit(overlay, (0, 0))

        winner_id = state["winner_id"]
        winner_name = next(
            (
                player["name"]
                for player in state["players"]
                if player["id"] == winner_id
            ),
            "Joueur"
        )
        result = (
            "VICTOIRE !"
            if winner_id == state["your_id"]
            else f"{winner_name} gagne"
        )
        result_color = (
            "#62e6a2"
            if winner_id == state["your_id"]
            else "#f07b8d"
        )

        result_text = self.title_font.render(
            result,
            True,
            result_color
        )
        screen.blit(
            result_text,
            result_text.get_rect(center=(640, 240))
        )

        replay_votes = set(
            state.get("replay_votes", [])
        )
        votes_text = self.small_font.render(
            f"Rejouer : {len(replay_votes)}/{state.get('replay_required', 2)}",
            True,
            "#aab1c1"
        )
        screen.blit(
            votes_text,
            votes_text.get_rect(center=(640, 330))
        )

        for index, player in enumerate(state["players"]):
            status = (
                "PRÊT"
                if player["id"] in replay_votes
                else "..."
            )
            line = self.small_font.render(
                f"{player['name']} : {status}",
                True,
                "#d8dce6"
            )
            screen.blit(
                line,
                line.get_rect(
                    center=(640, 360 + index * 27)
                )
            )

        already_voted = state["your_id"] in replay_votes
        replay_hover = self.replay_rect.collidepoint(mouse_pos)
        replay_color = (
            "#365e54"
            if already_voted
            else "#4c9679"
            if replay_hover
            else "#39755e"
        )
        replay_label = (
            "EN ATTENTE..."
            if already_voted
            else "REJOUER"
        )

        pygame.draw.rect(
            screen,
            replay_color,
            self.replay_rect,
            border_radius=10
        )
        replay_text = self.font.render(
            replay_label,
            True,
            "white"
        )
        screen.blit(
            replay_text,
            replay_text.get_rect(center=self.replay_rect.center)
        )

        lobby_color = (
            "#4a546d"
            if self.lobby_rect.collidepoint(mouse_pos)
            else "#373e52"
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
            lobby_text.get_rect(center=self.lobby_rect.center)
        )

    # ---------------------------------
    # DRAW
    # ---------------------------------

    def draw(
        self,
        screen,
        mouse_pos
    ):

        screen.fill(
            "#10131b"
        )

        state = (
            self.network.uno_state
        )
        self.card_rects = []
        if state is None:

            loading = self.title_font.render(
                "Chargement de la partie...",
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

        if state.get("winner_id") is not None:
            self.draw_game_over(
                screen,
                state,
                mouse_pos
            )
            return


        # ---------------------------------
        # ROOM
        # ---------------------------------

        room_text = self.small_font.render(
            f"ROOM {state['room_code']}",
            True,
            "#8f98ad"
        )

        screen.blit(
            room_text,
            (
                30,
                25
            )
        )


        # ---------------------------------
        # TOUR
        # ---------------------------------

        my_turn = (
            state[
                "current_player_id"
            ]
            == state[
                "your_id"
            ]
        )

        turn_text = (
            "À TON TOUR"
            if my_turn
            else "Tour de l'adversaire"
        )

        turn_color = (
            "#57e09b"
            if my_turn
            else "#a2a9ba"
        )

        rendered_turn = (
            self.title_font.render(
                turn_text,
                True,
                turn_color
            )
        )

        screen.blit(
            rendered_turn,
            rendered_turn.get_rect(
                center=(
                    640,
                    65
                )
            )
        )


        # ---------------------------------
        # JOUEURS
        # ---------------------------------

        y = 125

        for player in state[
            "players"
        ]:

            if (
                player["id"]
                == state["your_id"]
            ):
                continue

            player_text = (
                self.font.render(
                    f"{player['name']}  "
                    f"({player['card_count']} cartes)",
                    True,
                    "white"
                )
            )

            screen.blit(
                player_text,
                player_text.get_rect(
                    center=(
                        640,
                        y
                    )
                )
            )

            y += 40


        # ---------------------------------
        # CARTE CENTRALE
        # ---------------------------------

        top_card_rect = pygame.Rect(
            595,
            250,
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


        color_text = (
            self.small_font.render(
                "Couleur : "
                + str(
                    state[
                        "active_color"
                    ]
                ),
                True,
                "#a7afc0"
            )
        )

        screen.blit(
            color_text,
            color_text.get_rect(
                center=(
                    640,
                    410
                )
            )
        )


        # ---------------------------------
        # TA MAIN
        # ---------------------------------
        hovered = (
            my_turn
            and self.draw_rect.collidepoint(
                mouse_pos
            )
        )

        draw_color = (
            "#586681"
            if hovered
            else "#404a64"
            if my_turn
            else "#252936"
        )

        pygame.draw.rect(
            screen,
            draw_color,
            self.draw_rect,
            border_radius=10
        )

        draw_label = (
            "PIOCHER"
            if my_turn
            else "ATTENDS"
        )
        draw_font = (
            self.font
            if my_turn
            else self.small_font
        )
        text = draw_font.render(
            draw_label,
            True,
            "white"
        )

        screen.blit(
            text,
            text.get_rect(
                center=self.draw_rect.center
            )
        )
        hand = state[
            "your_hand"
        ]

        card_width = 80
        card_height = 115

        spacing = 65

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

        y = 550


        for index, card in enumerate(
            hand
        ):

            x = (
                start_x
                + index * spacing
            )

            rect = pygame.Rect(
                x,
                y,
                card_width,
                card_height
            )
            self.card_rects.append(
                {
                    "index": index,
                    "rect": rect
                }
            )

            self.draw_card(
                screen,
                card,
                rect
            )
            playable_indices = state.get(
                "playable_indices",
                []
            )


            if index not in playable_indices:

                dark_overlay = pygame.Surface(
                    (
                        rect.width,
                        rect.height
                    ),
                    pygame.SRCALPHA
                )

                dark_overlay.fill(
                    (
                        0,
                        0,
                        0,
                        125
                    )
                )

                screen.blit(
                    dark_overlay,
                    rect.topleft
                )
            if (
                self.pending_wild_index
                is not None
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
                        185
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
                            250
                        )
                    )
                )


                colors = {
                    "red": "#e74c3c",
                    "blue": "#3498db",
                    "green": "#2ecc71",
                    "yellow": "#f1c40f"
                }


                for color, rect in (
                    self.color_rects.items()
                ):

                    pygame.draw.rect(
                        screen,
                        colors[color],
                        rect,
                        border_radius=15
                    )

                    if rect.collidepoint(
                        mouse_pos
                    ):

                        pygame.draw.rect(
                            screen,
                            "white",
                            rect,
                            4,
                            border_radius=15
                        )