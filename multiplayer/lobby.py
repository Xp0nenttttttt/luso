import pygame


class MultiplayerLobby:

    def __init__(
        self,
        network
    ):

        self.network = network

        self.title_font = (
            pygame.font.Font(
                None,
                58
            )
        )

        self.font = pygame.font.Font(
            None,
            32
        )

        self.small_font = (
            pygame.font.Font(
                None,
                24
            )
        )

        self.code_input = ""

        self.input_active = False

        self.create_rect = (
            pygame.Rect(
                430,
                300,
                420,
                60
            )
        )
        self.start_uno_rect = pygame.Rect(
            480,
            515,
            320,
            55
        )
        self.input_rect = (
            pygame.Rect(
                430,
                395,
                260,
                60
            )
        )

        self.join_rect = (
            pygame.Rect(
                710,
                395,
                140,
                60
            )
        )

        self.leave_rect = (
            pygame.Rect(
                480,
                590,
                320,
                55
            )
        )

    # ---------------------------------
    # EVENT
    # ---------------------------------

    def handle_event(
        self,
        event,
        mouse_pos
    ):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                if self.network.room:

                    self.network.leave_room()

                    return None

                return "back"

            if self.input_active:

                if (
                    event.key
                    == pygame.K_BACKSPACE
                ):

                    self.code_input = (
                        self.code_input[:-1]
                    )

                elif (
                    event.key
                    == pygame.K_RETURN
                ):

                    if self.code_input:

                        self.network.join_room(
                            self.code_input
                        )

                else:

                    char = (
                        event.unicode
                        .upper()
                    )

                    if (
                        char.isalnum()
                        and len(
                            self.code_input
                        ) < 6
                    ):

                        self.code_input += char

        if (
            event.type
            == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):

            if self.network.room:
                if (
                    self.is_host()
                    and self.start_uno_rect.collidepoint(
                        mouse_pos
                    )
                ):

                    self.network.start_uno()

                    return None
                if self.leave_rect.collidepoint(
                    mouse_pos
                ):

                    self.network.leave_room()

                return None

            self.input_active = (
                self.input_rect
                .collidepoint(
                    mouse_pos
                )
            )

            if self.create_rect.collidepoint(
                mouse_pos
            ):

                if self.network.connected:

                    self.network.create_room()

            if self.join_rect.collidepoint(
                mouse_pos
            ):

                if (
                    self.network.connected
                    and self.code_input
                ):

                    self.network.join_room(
                        self.code_input
                    )

        return None

    # ---------------------------------
    # BUTTON
    # ---------------------------------

    def draw_button(
        self,
        screen,
        rect,
        text,
        mouse_pos
    ):

        hovered = (
            rect.collidepoint(
                mouse_pos
            )
        )

        color = (
            "#333b52"
            if not hovered
            else "#46516e"
        )

        pygame.draw.rect(
            screen,
            color,
            rect,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            "#586781",
            rect,
            2,
            border_radius=10
        )

        label = self.font.render(
            text,
            True,
            "white"
        )

        screen.blit(
            label,
            label.get_rect(
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
            "#0e111a"
        )

        title = (
            self.title_font.render(
                "MULTIJOUEUR",
                True,
                "white"
            )
        )

        screen.blit(
            title,
            title.get_rect(
                center=(
                    640,
                    90
                )
            )
        )

        # -------------------------
        # STATUS SERVEUR
        # -------------------------

        if self.network.connected:

            status_color = (
                "#55dc91"
            )

            status_text = (
                "Connecté au serveur"
            )

        else:

            status_color = (
                "#e05b6f"
            )

            status_text = (
                "Serveur hors ligne"
            )

        pygame.draw.circle(
            screen,
            status_color,
            (
                520,
                155
            ),
            8
        )

        status = (
            self.small_font.render(
                status_text,
                True,
                "#aeb6ca"
            )
        )

        screen.blit(
            status,
            (
                540,
                145
            )
        )

        # =========================
        # ROOM OU MENU
        # =========================

        room = self.network.room

        if room is None:

            self.draw_button(
                screen,
                self.create_rect,
                "CRÉER UNE ROOM",
                mouse_pos
            )

            code_label = (
                self.small_font.render(
                    "CODE DE ROOM",
                    True,
                    "#8992a8"
                )
            )

            screen.blit(
                code_label,
                (
                    self.input_rect.x,
                    self.input_rect.y - 30
                )
            )

            input_color = (
                "#252c40"
                if self.input_active
                else "#191e2c"
            )

            pygame.draw.rect(
                screen,
                input_color,
                self.input_rect,
                border_radius=8
            )

            pygame.draw.rect(
                screen,
                "#556078",
                self.input_rect,
                2,
                border_radius=8
            )

            code_text = self.font.render(
                self.code_input,
                True,
                "white"
            )

            screen.blit(
                code_text,
                (
                    self.input_rect.x + 20,
                    self.input_rect.y + 15
                )
            )

            self.draw_button(
                screen,
                self.join_rect,
                "JOIN",
                mouse_pos
            )

        else:

            # -------------------------
            # CODE
            # -------------------------

            label = (
                self.small_font.render(
                    "ROOM",
                    True,
                    "#8992a8"
                )
            )

            screen.blit(
                label,
                (
                    440,
                    240
                )
            )

            room_code = (
                self.title_font.render(
                    room["code"],
                    True,
                    "#6bdcff"
                )
            )

            screen.blit(
                room_code,
                (
                    440,
                    270
                )
            )

            # -------------------------
            # JOUEURS
            # -------------------------

            y = 370

            for player in room[
                "players"
            ]:

                pygame.draw.circle(
                    screen,
                    "#55dc91",
                    (
                        455,
                        y + 12
                    ),
                    7
                )

                name = player[
                    "name"
                ]

                if player[
                    "host"
                ]:

                    name += "  ★"

                text = (
                    self.font.render(
                        name,
                        True,
                        "white"
                    )
                )

                screen.blit(
                    text,
                    (
                        480,
                        y
                    )
                )

                y += 48

            self.draw_button(
                screen,
                self.leave_rect,
                "QUITTER LA ROOM",
                mouse_pos
            )

            player_count = len(
                room["players"]
            )


            if self.is_host():

                self.draw_button(
                    screen,
                    self.start_uno_rect,
                    "LANCER UNO",
                    mouse_pos
                )

                if player_count != 2:

                    info = self.small_font.render(
                        "Il faut 2 joueurs pour lancer UNO.",
                        True,
                        "#8992a8"
                    )

                    screen.blit(
                        info,
                        info.get_rect(
                            center=(
                                640,
                                490
                            )
                        )
                    )

            else:

                waiting = self.small_font.render(
                    "En attente de l'hôte...",
                    True,
                    "#8992a8"
                )

                screen.blit(
                    waiting,
                    waiting.get_rect(
                        center=(
                            640,
                            540
                        )
                    )
                )

        # -------------------------
        # ERREUR
        # -------------------------

        if self.network.last_error:

            error = (
                self.small_font.render(
                    self.network.last_error,
                    True,
                    "#ff7085"
                )
            )

            screen.blit(
                error,
                error.get_rect(
                    center=(
                        640,
                        680
                    )
                )
            )
    def is_host(self):

        room = self.network.room

        if room is None:
            return False

        return (
            room.get(
                "host_id"
            )
            == self.network.client_id
        )