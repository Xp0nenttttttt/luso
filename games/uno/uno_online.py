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

        self.network = network

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

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                return "back"

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

            self.draw_card(
                screen,
                card,
                rect
            )