import pygame


class FriendProfile:
    def __init__(self):
        self.friend = None

        # Onglet actif
        self.current_tab = "overview"

        # -----------------------------
        # FONTS
        # -----------------------------

        self.name_font = pygame.font.Font(
            None,
            46
        )

        self.title_font = pygame.font.Font(
            None,
            52
        )

        self.font = pygame.font.Font(
            None,
            32
        )

        self.small_font = pygame.font.Font(
            None,
            24
        )

        self.big_stat_font = pygame.font.Font(
            None,
            52
        )


        # -----------------------------
        # ONGLETS
        # -----------------------------

        self.tabs = {

            "overview": pygame.Rect(
                90,
                245,
                180,
                50
            ),

            "stats": pygame.Rect(
                280,
                245,
                180,
                50
            ),

            "games": pygame.Rect(
                470,
                245,
                180,
                50
            )
        }


    # -----------------------------
    # DEFINIR L'AMI
    # -----------------------------

    def set_friend(self, friend):
        self.friend = friend

        # Quand on ouvre un nouveau profil,
        # on retourne sur Aperçu
        self.current_tab = "overview"


    # -----------------------------
    # EVENTS
    # -----------------------------

    def handle_event(
        self,
        event,
        mouse_pos
    ):

        if self.friend is None:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                for tab_name, rect in self.tabs.items():

                    if rect.collidepoint(
                        mouse_pos
                    ):

                        self.current_tab = tab_name


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
    # PERSONNAGE PLACEHOLDER
    # -----------------------------

    def draw_character(
        self,
        screen,
        x,
        y,
        size
    ):

        color = self.friend.get(
            "color",
            "#5f78ff"
        )

        portrait_rect = pygame.Rect(
            x,
            y,
            size,
            size
        )

        pygame.draw.rect(
            screen,
            "#202431",
            portrait_rect
        )

        pygame.draw.rect(
            screen,
            "white",
            portrait_rect,
            4
        )


        center_x = portrait_rect.centerx


        # Tête
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(
                center_x - 18,
                y + 25,
                36,
                36
            )
        )


        # Corps
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(
                center_x - 28,
                y + 65,
                56,
                55
            )
        )


        # Jambes
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(
                center_x - 25,
                y + 115,
                18,
                25
            )
        )

        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(
                center_x + 7,
                y + 115,
                18,
                25
            )
        )


    # -----------------------------
    # CARTE DE STAT
    # -----------------------------

    def draw_card(
        self,
        screen,
        rect,
        title,
        value
    ):

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
            2,
            border_radius=8
        )


        title_text = self.small_font.render(
            title,
            True,
            "#aaaaaa"
        )

        screen.blit(
            title_text,
            (
                rect.x + 20,
                rect.y + 15
            )
        )


        value_text = self.big_stat_font.render(
            str(value),
            True,
            "white"
        )

        screen.blit(
            value_text,
            (
                rect.x + 20,
                rect.y + 55
            )
        )


    # -----------------------------
    # DRAW PRINCIPAL
    # -----------------------------

    def draw(
        self,
        screen,
        mouse_pos
    ):

        screen.fill(
            "#11141d"
        )


        if self.friend is None:

            error_text = self.font.render(
                "Aucun ami sélectionné.",
                True,
                "white"
            )

            screen.blit(
                error_text,
                (100, 100)
            )

            return


        # -----------------------------
        # BANNIERE
        # -----------------------------

        pygame.draw.rect(
            screen,
            self.friend.get(
                "color",
                "#4859b8"
            ),
            pygame.Rect(
                0,
                0,
                1280,
                150
            )
        )


        # -----------------------------
        # PERSONNAGE
        # -----------------------------

        self.draw_character(
            screen,
            70,
            90,
            140
        )


        # -----------------------------
        # NOM
        # -----------------------------

        name_text = self.name_font.render(
            self.friend[
                "display_name"
            ],
            True,
            "white"
        )

        screen.blit(
            name_text,
            (240, 155)
        )


        username_text = self.small_font.render(
            f"@{self.friend['username']}",
            True,
            "#999999"
        )

        screen.blit(
            username_text,
            (240, 200)
        )


        # -----------------------------
        # STATUT
        # -----------------------------

        status_color = self.get_status_color(
            self.friend["status"]
        )

        pygame.draw.circle(
            screen,
            status_color,
            (1030, 180),
            10
        )


        status_text = self.small_font.render(
            self.get_status_text(
                self.friend["status"]
            ),
            True,
            "white"
        )

        screen.blit(
            status_text,
            (1050, 168)
        )


        # -----------------------------
        # ONGLETS
        # -----------------------------

        titles = {
            "overview": "APERÇU",
            "stats": "STATS",
            "games": "JEUX"
        }


        for tab_name, rect in self.tabs.items():

            if self.current_tab == tab_name:

                color = "#5f78ff"

            elif rect.collidepoint(
                mouse_pos
            ):

                color = "#34394a"

            else:

                color = "#202431"


            pygame.draw.rect(
                screen,
                color,
                rect,
                border_radius=6
            )


            tab_text = self.font.render(
                titles[tab_name],
                True,
                "white"
            )

            tab_text_rect = tab_text.get_rect(
                center=rect.center
            )

            screen.blit(
                tab_text,
                tab_text_rect
            )


        # -----------------------------
        # CONTENU
        # -----------------------------

        if self.current_tab == "overview":

            self.draw_overview(
                screen
            )

        elif self.current_tab == "stats":

            self.draw_stats(
                screen
            )

        elif self.current_tab == "games":

            self.draw_games(
                screen
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


    # -----------------------------
    # APERCU
    # -----------------------------

    def draw_overview(
        self,
        screen
    ):

        bio_title = self.small_font.render(
            "À PROPOS",
            True,
            "#888888"
        )

        screen.blit(
            bio_title,
            (90, 330)
        )


        bio = self.friend.get(
            "bio",
            "Aucune bio."
        )


        bio_text = self.font.render(
            bio,
            True,
            "white"
        )

        screen.blit(
            bio_text,
            (90, 365)
        )


        self.draw_card(
            screen,
            pygame.Rect(
                90,
                430,
                320,
                150
            ),
            "TEMPS TOTAL",
            self.friend.get(
                "playtime",
                "0h 00m"
            )
        )


        self.draw_card(
            screen,
            pygame.Rect(
                430,
                430,
                320,
                150
            ),
            "SESSIONS",
            self.friend.get(
                "sessions",
                0
            )
        )


        self.draw_card(
            screen,
            pygame.Rect(
                770,
                430,
                320,
                150
            ),
            "JEUX",
            len(
                self.friend.get(
                    "games",
                    []
                )
            )
        )


    # -----------------------------
    # STATS
    # -----------------------------

    def draw_stats(
        self,
        screen
    ):

        self.draw_card(
            screen,
            pygame.Rect(
                90,
                340,
                320,
                140
            ),
            "TEMPS TOTAL",
            self.friend.get(
                "playtime",
                "0h 00m"
            )
        )


        self.draw_card(
            screen,
            pygame.Rect(
                430,
                340,
                320,
                140
            ),
            "SESSIONS",
            self.friend.get(
                "sessions",
                0
            )
        )


        activity = self.friend.get(
            "activity",
            "Aucune activité"
        )


        activity_text = self.font.render(
            f"Activité actuelle : {activity}",
            True,
            "white"
        )

        screen.blit(
            activity_text,
            (90, 530)
        )


    # -----------------------------
    # JEUX
    # -----------------------------

    def draw_games(
        self,
        screen
    ):

        title = self.title_font.render(
            "Jeux",
            True,
            "white"
        )

        screen.blit(
            title,
            (90, 340)
        )


        games = self.friend.get(
            "games",
            []
        )


        if not games:

            empty_text = self.font.render(
                "Aucun jeu enregistré.",
                True,
                "#888888"
            )

            screen.blit(
                empty_text,
                (90, 420)
            )

            return


        y = 420

        for game in games:

            game_rect = pygame.Rect(
                90,
                y,
                650,
                70
            )


            pygame.draw.rect(
                screen,
                "#202431",
                game_rect,
                border_radius=6
            )


            game_text = self.font.render(
                game,
                True,
                "white"
            )

            screen.blit(
                game_text,
                (
                    game_rect.x + 20,
                    game_rect.y + 20
                )
            )


            y += 85