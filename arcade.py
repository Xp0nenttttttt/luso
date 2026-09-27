import pygame


class Arcade:
    def __init__(self, stats):
        self.stats = stats

        # -----------------------------
        # FONTS
        # -----------------------------

        self.title_font = pygame.font.Font(None, 60)
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)

        # -----------------------------
        # CATALOGUE DES JEUX
        # -----------------------------
        #
        # Tu pourras simplement ajouter tes jeux ici plus tard.

        self.games = [
            {
                "id": "rhythm_game",
                "name": "Rhythm Game",
                "description": "Jeu de rythme",
                "status": "available"
            },

            {
                "id": "uno",
                "name": "Uno",
                "description": "Jeu de cartes classique",
                "status": "available"
            },

            {
                "id": "secret_game",
                "name": "Projet Secret",
                "description": "???",
                "status": "development"
            }
        ]

        # -----------------------------
        # CARTES
        # -----------------------------

        self.cards = []

        self.create_cards()

    # -----------------------------
    # CREATION DES CARTES
    # -----------------------------

    def create_cards(self):
        self.cards.clear()

        start_y = 180

        for index, game in enumerate(self.games):

            card_rect = pygame.Rect(
                100,
                start_y + index * 155,
                1080,
                125
            )

            play_button = pygame.Rect(
                970,
                card_rect.y + 40,
                160,
                50
            )

            self.cards.append(
                {
                    "game": game,
                    "rect": card_rect,
                    "play_button": play_button
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

                for card in self.cards:

                    game = card["game"]

                    if card["play_button"].collidepoint(
                        mouse_pos
                    ):

                        # Jeu pas encore disponible
                        if game["status"] != "available":
                            return None

                        return {
                            "action": "launch_game",
                            "game_id": game["id"],
                            "game": game
                        }

        return None

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
            "ARCADE",
            True,
            "white"
        )

        screen.blit(
            title,
            (100, 65)
        )

        subtitle = self.small_font.render(
            "Choisis un jeu",
            True,
            "#888888"
        )

        screen.blit(
            subtitle,
            (100, 120)
        )

        # -----------------------------
        # JEUX
        # -----------------------------

        for card in self.cards:

            game = card["game"]
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
            # ICONE PLACEHOLDER
            # -------------------------

            icon_rect = pygame.Rect(
                rect.x + 20,
                rect.y + 20,
                85,
                85
            )

            pygame.draw.rect(
                screen,
                "#34394a",
                icon_rect,
                border_radius=8
            )

            pygame.draw.rect(
                screen,
                "#777777",
                icon_rect,
                width=2,
                border_radius=8
            )

            # Faux symbole
            pygame.draw.circle(
                screen,
                "#5f78ff",
                icon_rect.center,
                20
            )

            # -------------------------
            # NOM
            # -------------------------

            name_text = self.font.render(
                game["name"],
                True,
                "white"
            )

            screen.blit(
                name_text,
                (
                    rect.x + 130,
                    rect.y + 18
                )
            )

            # -------------------------
            # DESCRIPTION
            # -------------------------

            description_text = self.small_font.render(
                game["description"],
                True,
                "#999999"
            )

            screen.blit(
                description_text,
                (
                    rect.x + 130,
                    rect.y + 52
                )
            )

            # -------------------------
            # STATS
            # -------------------------

            playtime = self.stats.get_game_playtime_text(
                game["id"]
            )

            launches = self.stats.get_game_launch_count(
                game["id"]
            )

            stats_text = self.small_font.render(
                f"{playtime}  |  {launches} lancements",
                True,
                "#cccccc"
            )

            screen.blit(
                stats_text,
                (
                    rect.x + 130,
                    rect.y + 83
                )
            )

            # -------------------------
            # STATUT
            # -------------------------

            if game["status"] == "available":

                status_text = "Disponible"
                status_color = "#5fd68a"

            else:

                status_text = "En developpement"
                status_color = "#f5c45f"

            status = self.small_font.render(
                status_text,
                True,
                status_color
            )

            screen.blit(
                status,
                (
                    rect.x + 690,
                    rect.y + 51
                )
            )

            # -------------------------
            # BOUTON
            # -------------------------

            button = card["play_button"]

            if game["status"] != "available":

                button_color = "#333333"
                text_color = "#777777"

            else:

                if button.collidepoint(
                    mouse_pos
                ):

                    button_color = "#7286ff"

                else:

                    button_color = "#5f78ff"

                text_color = "white"

            pygame.draw.rect(
                screen,
                button_color,
                button,
                border_radius=6
            )

            if game["status"] == "available":
                button_text = "LANCER"
            else:
                button_text = "BIENTOT"

            text = self.small_font.render(
                button_text,
                True,
                text_color
            )

            text_rect = text.get_rect(
                center=button.center
            )

            screen.blit(
                text,
                text_rect
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