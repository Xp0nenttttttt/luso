import pygame


class MainMenu:
    def __init__(self):

        self.title_font = pygame.font.Font(
            None,
            90
        )

        self.button_font = pygame.font.Font(
            None,
            45
        )


        # --------------------------------
        # BOUTONS
        # --------------------------------

        self.buttons = [

            {
                "text": "JOUER",
                "action": "play",
                "rect": pygame.Rect(
                    440,
                    220,
                    400,
                    65
                )
            },
            {
                "text": "MULTIJOUEUR",
                "action": "multiplayer",
                "rect": pygame.Rect(
                    440,
                    300,
                    400,
                    65
                )
            },
            {
                "text": "PROFIL",
                "action": "profile",
                "rect": pygame.Rect(
                    440,
                    300,
                    400,
                    65
                )
            },

            {
                "text": "AMIS",
                "action": "friends",
                "rect": pygame.Rect(
                    440,
                    380,
                    400,
                    65
                )
            },

            {
                "text": "OPTIONS",
                "action": "options",
                "rect": pygame.Rect(
                    440,
                    460,
                    400,
                    65
                )
            },

            {
                "text": "QUITTER",
                "action": "quit",
                "rect": pygame.Rect(
                    440,
                    540,
                    400,
                    65
                )
            }

        ]


    # --------------------------------
    # EVENTS
    # --------------------------------

    def handle_event(
        self,
        event,
        mouse_pos
    ):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                for button in self.buttons:

                    if button["rect"].collidepoint(
                        mouse_pos
                    ):

                        return button["action"]

        return None


    # --------------------------------
    # DRAW
    # --------------------------------

    def draw(
        self,
        screen,
        mouse_pos
    ):

        screen.fill("#171923")


        # --------------------------------
        # TITRE
        # --------------------------------

        title = self.title_font.render(
            "GAME HUB",
            True,
            "white"
        )

        title_rect = title.get_rect(
            center=(640, 120)
        )

        screen.blit(
            title,
            title_rect
        )


        # --------------------------------
        # BOUTONS
        # --------------------------------

        for button in self.buttons:

            rect = button["rect"]

            mouse_hover = (
                rect.collidepoint(
                    mouse_pos
                )
            )


            if mouse_hover:

                color = "#5f78ff"

            else:

                color = "#343746"


            pygame.draw.rect(
                screen,
                color,
                rect,
                border_radius=8
            )

            pygame.draw.rect(
                screen,
                "white",
                rect,
                width=3,
                border_radius=8
            )


            text = self.button_font.render(
                button["text"],
                True,
                "white"
            )

            text_rect = text.get_rect(
                center=rect.center
            )

            screen.blit(
                text,
                text_rect
            )