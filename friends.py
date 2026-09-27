import pygame


class FriendsMenu:
    def __init__(self):
        # -----------------------------
        # FONTS
        # -----------------------------

        self.title_font = pygame.font.Font(None, 55)
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)


        # -----------------------------
        # AMIS PLACEHOLDERS
        # -----------------------------

        self.friends = [
    {
        "id": 1,
        "display_name": "Luna",
        "username": "luna",

        "status": "online",
        "activity": "Dans le hub",

        "color": "#ff6f91",

        "bio": "Toujours partante pour jouer.",

        "playtime": "16h 42m",
        "sessions": 38,

        "games": [
            "Rhythm Game",
            "Coffee Game"
        ]
    },

    {
        "id": 2,
        "display_name": "Milo",
        "username": "milo",

        "status": "playing",
        "activity": "Rhythm Game",

        "color": "#5f78ff",

        "bio": "Fan de jeux de rythme.",

        "playtime": "8h 17m",
        "sessions": 21,

        "games": [
            "Rhythm Game"
        ]
    },

    {
        "id": 3,
        "display_name": "Nova",
        "username": "nova",

        "status": "offline",
        "activity": "Hors ligne",

        "color": "#aaaaaa",

        "bio": "zzz...",

        "playtime": "3h 04m",
        "sessions": 9,

        "games": []
    }
]


        # -----------------------------
        # BOUTONS
        # -----------------------------

        self.friend_cards = []

        self.create_cards()


    # -----------------------------
    # CREATION DES CARTES
    # -----------------------------

    def create_cards(self):
        self.friend_cards.clear()

        start_y = 170

        for index, friend in enumerate(self.friends):

            card_rect = pygame.Rect(
                120,
                start_y + index * 150,
                1040,
                120
            )


            profile_button = pygame.Rect(
                850,
                card_rect.y + 35,
                120,
                45
            )


            join_button = pygame.Rect(
                985,
                card_rect.y + 35,
                140,
                45
            )


            self.friend_cards.append(
                {
                    "friend": friend,
                    "rect": card_rect,
                    "profile_button": profile_button,
                    "join_button": join_button
                }
            )


    # -----------------------------
    # EVENTS
    # -----------------------------

    def handle_event(
        self,
        event,
        mouse_pos
    ):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                for card in self.friend_cards:

                    friend = card["friend"]


                    # -------------------------
                    # PROFIL
                    # -------------------------

                    if card["profile_button"].collidepoint(
                        mouse_pos
                    ):

                        return {
                            "action": "friend_profile",
                            "friend": friend
                        }


                    # -------------------------
                    # REJOINDRE
                    # -------------------------

                    if card["join_button"].collidepoint(
                        mouse_pos
                    ):

                        # Hors ligne = impossible
                        if friend["status"] == "offline":
                            return None

                        return {
                            "action": "join_friend",
                            "friend": friend
                        }

        return None


    # -----------------------------
    # AVATAR PLACEHOLDER
    # -----------------------------

    def draw_avatar(
        self,
        screen,
        rect,
        color
    ):

        pygame.draw.rect(
            screen,
            "#171923",
            rect,
            border_radius=8
        )

        pygame.draw.rect(
            screen,
            "white",
            rect,
            width=2,
            border_radius=8
        )


        center_x = rect.centerx


        # Tête
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(
                center_x - 14,
                rect.y + 15,
                28,
                28
            )
        )


        # Corps
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(
                center_x - 20,
                rect.y + 48,
                40,
                32
            )
        )


    # -----------------------------
    # STATUT
    # -----------------------------

    def get_status_color(
        self,
        status
    ):

        if status == "online":
            return "#5fd68a"

        if status == "playing":
            return "#5f78ff"

        return "#666666"


    def get_status_text(
        self,
        status
    ):

        if status == "online":
            return "En ligne"

        if status == "playing":
            return "En jeu"

        return "Hors ligne"


    # -----------------------------
    # DRAW
    # -----------------------------

    def draw(
        self,
        screen,
        mouse_pos
    ):

        screen.fill(
            "#11141d"
        )


        # -----------------------------
        # TITRE
        # -----------------------------

        title = self.title_font.render(
            "AMIS",
            True,
            "white"
        )

        screen.blit(
            title,
            (120, 70)
        )


        subtitle = self.small_font.render(
            f"{len(self.friends)} amis",
            True,
            "#888888"
        )

        screen.blit(
            subtitle,
            (120, 125)
        )


        # -----------------------------
        # LISTE
        # -----------------------------

        for card in self.friend_cards:

            friend = card["friend"]

            rect = card["rect"]


            # -------------------------
            # CARTE
            # -------------------------

            pygame.draw.rect(
                screen,
                "#202431",
                rect,
                border_radius=8
            )

            pygame.draw.rect(
                screen,
                "#34394a",
                rect,
                width=2,
                border_radius=8
            )


            # -------------------------
            # AVATAR
            # -------------------------

            avatar_rect = pygame.Rect(
                rect.x + 20,
                rect.y + 20,
                80,
                80
            )

            self.draw_avatar(
                screen,
                avatar_rect,
                friend["color"]
            )


            # -------------------------
            # NOM
            # -------------------------

            name_text = self.font.render(
                friend["display_name"],
                True,
                "white"
            )

            screen.blit(
                name_text,
                (
                    rect.x + 125,
                    rect.y + 20
                )
            )


            username_text = self.small_font.render(
                f"@{friend['username']}",
                True,
                "#888888"
            )

            screen.blit(
                username_text,
                (
                    rect.x + 125,
                    rect.y + 52
                )
            )


            # -------------------------
            # STATUT
            # -------------------------

            status_color = self.get_status_color(
                friend["status"]
            )

            pygame.draw.circle(
                screen,
                status_color,
                (
                    rect.x + 135,
                    rect.y + 87
                ),
                7
            )


            status_text = self.small_font.render(
                self.get_status_text(
                    friend["status"]
                ),
                True,
                "#cccccc"
            )

            screen.blit(
                status_text,
                (
                    rect.x + 150,
                    rect.y + 76
                )
            )


            # -------------------------
            # ACTIVITE
            # -------------------------

            activity_text = self.small_font.render(
                friend["activity"],
                True,
                "#aaaaaa"
            )

            screen.blit(
                activity_text,
                (
                    rect.x + 330,
                    rect.y + 52
                )
            )


            # -------------------------
            # PROFIL
            # -------------------------

            profile_button = card[
                "profile_button"
            ]


            if profile_button.collidepoint(
                mouse_pos
            ):

                profile_color = "#4f5668"

            else:

                profile_color = "#34394a"


            pygame.draw.rect(
                screen,
                profile_color,
                profile_button,
                border_radius=6
            )


            profile_text = self.small_font.render(
                "Profil",
                True,
                "white"
            )

            profile_text_rect = profile_text.get_rect(
                center=profile_button.center
            )

            screen.blit(
                profile_text,
                profile_text_rect
            )


            # -------------------------
            # REJOINDRE
            # -------------------------

            join_button = card[
                "join_button"
            ]


            # Si ami hors ligne
            if friend["status"] == "offline":

                join_color = "#333333"

                join_text_color = "#777777"

            else:

                if join_button.collidepoint(
                    mouse_pos
                ):

                    join_color = "#7286ff"

                else:

                    join_color = "#5f78ff"

                join_text_color = "white"


            pygame.draw.rect(
                screen,
                join_color,
                join_button,
                border_radius=6
            )


            join_text = self.small_font.render(
                "Rejoindre",
                True,
                join_text_color
            )

            join_text_rect = join_text.get_rect(
                center=join_button.center
            )

            screen.blit(
                join_text,
                join_text_rect
            )


        # -----------------------------
        # RETOUR
        # -----------------------------

        back_text = self.small_font.render(
            "ESC - Retour",
            True,
            "#777777"
        )

        screen.blit(
            back_text,
            (1100, 680)
        )