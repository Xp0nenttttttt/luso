import pygame


class Hub:
    def __init__(self, player):
        self.player = player

        # Taille logique du jeu
        self.width = 1280
        self.height = 720

        self.world_rect = pygame.Rect(
            0,
            0,
            self.width,
            self.height
        )

        self.player_rect = pygame.Rect(
            0,
            0,
            32,
            32
        )

        self.font = pygame.font.Font(None, 35)
        self.small_font = pygame.font.Font(None, 28)


        # --------------------------------
        # BATIMENTS
        # --------------------------------

        self.buildings = [

            {
                "name": "ARCADE",
                "action": "arcade",
                "rect": pygame.Rect(
                    100,
                    80,
                    250,
                    160
                ),
                "color": "royalblue"
            },

            {
                "name": "MAISON",
                "action": "profile",
                "rect": pygame.Rect(
                    930,
                    80,
                    250,
                    160
                ),
                "color": "orange"
            },

            {
                "name": "AMIS",
                "action": "friends",
                "rect": pygame.Rect(
                    100,
                    480,
                    250,
                    160
                ),
                "color": "purple"
            },

            {
                "name": "STATS",
                "action": "profile",
                "rect": pygame.Rect(
                    930,
                    480,
                    250,
                    160
                ),
                "color": "dodgerblue"
            }

        ]


        # Position de départ du joueur
        self.player.x = 615
        self.player.y = 335

        self.sync_player_rect()


    def sync_player_rect(self):
        self.player_rect.center = (
            round(self.player.x),
            round(self.player.y)
        )


    # --------------------------------
    # UPDATE
    # --------------------------------

    def update(self, keys, dt):

        # On sauvegarde la position avant déplacement
        old_position = (
            self.player.x,
            self.player.y
        )

        # Déplacement normal du joueur
        self.player.update(keys, dt)

        self.sync_player_rect()


        # --------------------------------
        # COLLISIONS BATIMENTS
        # --------------------------------

        for building in self.buildings:

            if self.player_rect.colliderect(
                building["rect"]
            ):

                # Collision :
                # retour à l'ancienne position
                self.player.x, self.player.y = old_position

                self.sync_player_rect()

                break


        # --------------------------------
        # LIMITES DE LA MAP
        # --------------------------------

        self.player_rect.clamp_ip(
            self.world_rect
        )

        self.player.x = float(self.player_rect.centerx)
        self.player.y = float(self.player_rect.centery)


    # --------------------------------
    # BATIMENT PROCHE
    # --------------------------------

    def get_nearby_building(self):

        for building in self.buildings:

            # Zone légèrement plus grande
            # que le bâtiment
            interaction_zone = (
                building["rect"].inflate(
                    70,
                    70
                )
            )

            if self.player_rect.colliderect(
                interaction_zone
            ):

                return building

        return None


    # --------------------------------
    # EVENTS
    # --------------------------------

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            # Interaction
            if event.key == pygame.K_e:

                building = (
                    self.get_nearby_building()
                )

                if building is not None:

                    return building["action"]

        return None


    # --------------------------------
    # DRAW
    # --------------------------------

    def draw(self, screen):

        # Herbe
        screen.fill("#6ea34a")


        # --------------------------------
        # ROUTES
        # --------------------------------

        pygame.draw.rect(
            screen,
            "#9a9a9a",
            pygame.Rect(
                0,
                300,
                1280,
                120
            )
        )

        pygame.draw.rect(
            screen,
            "#9a9a9a",
            pygame.Rect(
                580,
                0,
                120,
                720
            )
        )


        # --------------------------------
        # PLACE CENTRALE
        # --------------------------------

        pygame.draw.circle(
            screen,
            "#75b9df",
            (640, 360),
            55
        )

        pygame.draw.circle(
            screen,
            "white",
            (640, 360),
            55,
            5
        )


        # --------------------------------
        # BATIMENTS
        # --------------------------------

        for building in self.buildings:

            rect = building["rect"]

            pygame.draw.rect(
                screen,
                building["color"],
                rect,
                border_radius=8
            )

            pygame.draw.rect(
                screen,
                "white",
                rect,
                width=4,
                border_radius=8
            )


            # Nom du bâtiment
            text = self.font.render(
                building["name"],
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


        # --------------------------------
        # JOUEUR
        # --------------------------------

        self.player.draw(screen)


        # --------------------------------
        # INTERACTION
        # --------------------------------

        building = self.get_nearby_building()

        if building is not None:

            message = self.small_font.render(
                f"E - Entrer dans {building['name']}",
                True,
                "white"
            )

            message_rect = message.get_rect(
                center=(640, 675)
            )


            # Fond noir derrière le texte
            background_rect = (
                message_rect.inflate(
                    30,
                    15
                )
            )

            pygame.draw.rect(
                screen,
                "black",
                background_rect,
                border_radius=5
            )

            screen.blit(
                message,
                message_rect
            )