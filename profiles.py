import pygame
from datetime import datetime
from pathlib import Path
from asset_paths import asset_path
from pathlib import Path

from characters import CHARACTERS
profile_path = asset_path("assets", "profile")

class Profile:
    def __init__(self, stats, progression):
        self.character_buttons = []
        self.load_character_assets()
        self.character_changed = None
        self.badge_catalog = {
            "level": {
                "name": "Progression",
                "description": "Atteindre le niveau 5"
            },

            "playtime": {
                "name": "Habitué",
                "description": "Jouer pendant 1 heure"
            },

            "arcade": {
                "name": "Arcade",
                "description": "Lancer 5 parties"
            },

            "social": {
                "name": "Social",
                "description": "Jouer avec un ami"
            }
        }
        self.badge_rects = []
        # -----------------------------
        # ASSETS PROFIL
        # -----------------------------
        self.profile_assets = asset_path(
            "assets",
            "profile"
        )

        self.profile_icons = {
            "time": self.load_profile_image(
                self.profile_assets / "icons/time.png"
            ),

            "games": self.load_profile_image(
                self.profile_assets / "icons/games.png"
            ),

            "xp": self.load_profile_image(
                self.profile_assets / "icons/xp.png"
            ),

            "calendar": self.load_profile_image(
                self.profile_assets / "icons/calendar.png"
            )
        }


        self.badge_images = {
            "level": self.load_profile_image(
                self.profile_assets / "badges/level.png"
            ),

            "playtime": self.load_profile_image(
                self.profile_assets / "badges/playtime.png"
            ),

            "arcade": self.load_profile_image(
                self.profile_assets / "badges/arcade.png"
            ),

            "social": self.load_profile_image(
                self.profile_assets / "badges/social.png"
            )
        }
        # -----------------------------
        # THEME DU PROFIL
        # -----------------------------
        self.theme = {
            "background": "#0d0f17",

            "panel": "#191d29",
            "panel_alt": "#212633",

            "border": "#303747",

            "accent": "#ff78b7",
            "accent_soft": "#ffb5d6",

            "text": "#ffffff",
            "muted": "#9399aa",

            "online": "#57d68d",
            "warning": "#f5c45f"
        }
        self.stats = stats
        # -----------------------------
        # SCROLL
        # -----------------------------

        self.scroll_y = 0
        self.scroll_speed = 55

        # Le contenu commence sous les onglets
        self.content_top = 310

        # Surface virtuelle plus grande que l'écran
        self.content_surface = pygame.Surface(
            (1280, 1600),
            pygame.SRCALPHA
        )

        self.max_scroll = 0
        self.progression = progression
        self.current_tab = "overview"
        self.edit_button = pygame.Rect(
            950,
            245,
            180,
            50
        )
        # -----------------------------
        # ASSETS PROFIL
        # -----------------------------

        self.profile_icon = pygame.image.load(
            asset_path(
                "assets",
                "characters",
                "lucie",
                "pfp.png"
            )
        ).convert_alpha()

        self.profile_icon = pygame.transform.scale(
            self.profile_icon,
            (140, 140)
        )


        # -----------------------------
        # PERSONNAGE PREVIEW
        # -----------------------------

        idle_sheet = pygame.image.load(
            asset_path(
                "assets",
                "characters",
                "lucie",
                "idle.png"
            )
        ).convert_alpha()

        FRAME_SIZE = 340

        # Première frame, direction DOWN
        character_frame = idle_sheet.subsurface(
            pygame.Rect(
                0,
                0,
                FRAME_SIZE,
                FRAME_SIZE
            )
        ).copy()

        self.character_preview = pygame.transform.scale(
            character_frame,
            (180, 180)
        )
        self.editing = False

        self.edit_field = None

        self.edit_values = {
            "display_name": "",
            "username": "",
            "bio": ""
        }
        self.name_input = pygame.Rect(
            350,
            350,
            500,
            50
        )

        self.username_input = pygame.Rect(
            350,
            420,
            500,
            50
        )

        self.bio_input = pygame.Rect(
            350,
            490,
            500,
            50
        )

        self.save_button = pygame.Rect(
            500,
            580,
            280,
            55
        )
        # -----------------------------
        # PROFIL
        # -----------------------------

        self.profile_data = self.stats.data.setdefault(
            "profile",
            {}
        )

        defaults = {
            "display_name": "Player",
            "username": "player",
            "bio": "Bienvenue dans mon hub !",
            "status": "online",

            # Plus tard ça correspondra
            # au vrai sprite du personnage
            "character": "default",
            # Objets équipés
            "title": "default",
            "banner": "default",
            "card_back": "default"
        }

        for key, value in defaults.items():
            self.profile_data.setdefault(
                key,
                value
            )

        self.banner = self.get_banner()

        self.stats.save()

        # -----------------------------
        # COLLECTION
        # -----------------------------

        self.title_catalog = {
            "default": "Aucun titre",
            "arcade_regular": "Arcade Regular",
            "hub_veteran": "Hub Veteran"
        }


        self.banner_catalog = {

            "default": {
                "name": "Default",
                "color": "#4859b8"
            },

            "blue_wave": {
                "name": "Blue Wave",
                "color": "#3159c9"
            }
        }


        self.card_back_catalog = {

            "default": {
                "name": "Default",
                "color": "#292d7a"
            },

            "retro_blue": {
                "name": "Retro Blue",
                "color": "#163b78"
            }
        }


        # Les boutons de collection seront
        # reconstruits à chaque affichage.
        self.collection_buttons = []
        # -----------------------------
        # FONTS
        # -----------------------------

        self.title_font = pygame.font.Font(
            None,
            52
        )

        self.name_font = pygame.font.Font(
            None,
            46
        )

        self.font = pygame.font.Font(
            None,
            32
        )

        self.small_font = pygame.font.Font(
            None,
            25
        )

        self.big_stat_font = pygame.font.Font(
            None,
            55
        )


        # -----------------------------
        # ONGLETS
        # -----------------------------

        self.tabs = {
            "collection": pygame.Rect(
                660,
                245,
                200,
                50
            ),
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
    # DATE
    # -----------------------------
    def draw_characters(
        self,
        screen,
        mouse_pos,
        start_y
    ):
        self.character_buttons = []

        current = self.profile_data.get(
            "character",
            "lucie"
        )

        x = 90
        y = start_y

        for character_id, data in (
            CHARACTERS.items()
        ):

            rect = pygame.Rect(
                x,
                y,
                210,
                250
            )

            hovered = rect.collidepoint(
                mouse_pos
            )

            equipped = (
                current
                == character_id
            )

            color = (
                "#263147"
                if hovered
                else self.theme["panel"]
            )

            pygame.draw.rect(
                screen,
                color,
                rect,
                border_radius=12
            )

            pygame.draw.rect(
                screen,
                (
                    self.theme["accent"]
                    if equipped
                    else self.theme["border"]
                ),
                rect,
                3 if equipped else 2,
                border_radius=12
            )


            # -------------------------
            # AVATAR
            # -------------------------

            path = (
                Path("assets")
                / "characters"
                / data["folder"]
                / "profile_icon.png"
            )

            try:

                image = pygame.image.load(
                    path
                ).convert_alpha()

                image = (
                    pygame.transform.smoothscale(
                        image,
                        (130, 130)
                    )
                )

                image_rect = (
                    image.get_rect(
                        center=(
                            rect.centerx,
                            rect.y + 90
                        )
                    )
                )

                screen.blit(
                    image,
                    image_rect
                )

            except Exception:
                pass


            # -------------------------
            # NOM
            # -------------------------

            name = self.font.render(
                data["name"],
                True,
                self.theme["text"]
            )

            screen.blit(
                name,
                name.get_rect(
                    center=(
                        rect.centerx,
                        rect.y + 175
                    )
                )
            )


            label = (
                "ÉQUIPÉ"
                if equipped
                else "ÉQUIPER"
            )

            label_color = (
                self.theme["success"]
                if equipped
                else self.theme["muted"]
            )

            text = self.small_font.render(
                label,
                True,
                label_color
            )

            screen.blit(
                text,
                text.get_rect(
                    center=(
                        rect.centerx,
                        rect.y + 215
                    )
                )
            )


            self.character_buttons.append(
                {
                    "rect": rect,
                    "character":
                        character_id
                }
            )


            x += 235

            if x > 1000:

                x = 90
                y += 280
    def format_date(self, date_string):

        if not date_string:
            return "Jamais"

        try:

            date = datetime.fromisoformat(
                date_string
            )

            return date.strftime(
                "%d/%m/%Y %H:%M"
            )

        except ValueError:

            return date_string


    # -----------------------------
    # EVENTS
    # -----------------------------

    def handle_event(
        self,
        event,
        mouse_pos
    ):
        content_mouse_pos = (
            mouse_pos[0],
            mouse_pos[1] + self.scroll_y
        )
        if event.type == pygame.MOUSEWHEEL:

            if not self.editing:

                self.scroll_y -= (
                    event.y
                    * self.scroll_speed
                )

                self.update_scroll_limits()

            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.edit_button.collidepoint(
                mouse_pos
            ):

                self.start_editing()

                return
            if self.editing:

                if self.name_input.collidepoint(
                    mouse_pos
                ):

                    self.edit_field = "display_name"


                elif self.username_input.collidepoint(
                    mouse_pos
                ):

                    self.edit_field = "username"


                elif self.bio_input.collidepoint(
                    mouse_pos
                ):

                    self.edit_field = "bio"


                elif self.save_button.collidepoint(
                    mouse_pos
                ):

                    self.save_profile()


                return
            
            if event.button == 1:

                for tab_name, rect in self.tabs.items():

                    if rect.collidepoint(mouse_pos):

                        if self.current_tab != tab_name:

                            self.current_tab = tab_name

                            # Retour en haut du nouvel onglet
                            self.scroll_y = 0

                        return
        if (
                    event.type == pygame.KEYDOWN
                    and self.editing
                ):
                if event.key == pygame.K_ESCAPE:

                    self.editing = False

                    self.edit_field = None

                    return


                if self.edit_field is None:
                    return


                # Effacer
                if event.key == pygame.K_BACKSPACE:

                    self.edit_values[
                        self.edit_field
                    ] = self.edit_values[
                        self.edit_field
                    ][:-1]


                # Entrée
                elif event.key == pygame.K_RETURN:

                    self.save_profile()


                # Texte normal
                else:

                    character = event.unicode

                    if character.isprintable():

                        # Limites simples
                        limits = {
                            "display_name": 20,
                            "username": 20,
                            "bio": 80
                        }

                        current = self.edit_values[
                            self.edit_field
                        ]

                        if len(current) < limits[
                            self.edit_field
                        ]:

                            self.edit_values[
                                self.edit_field
                            ] += character
        # -----------------------------
        # COLLECTION
        # -----------------------------

        if self.current_tab == "collection":
            if (
                event.type
                == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):

                for button in (
                    self.character_buttons
                ):

                    if button[
                        "rect"
                    ].collidepoint(
                        content_mouse_pos
                    ):

                        self.equip_character(
                            button[
                                "character"
                            ]
                        )

                        return
            for button in self.collection_buttons:

                if button["rect"].collidepoint(
                    content_mouse_pos
                ):

                    item_type = button["type"]
                    item_id = button["id"]


                    # -------------------------
                    # TITRE
                    # -------------------------

                    if item_type == "title":

                        self.profile_data[
                            "title"
                        ] = item_id


                    # -------------------------
                    # BANNIERE
                    # -------------------------

                    elif item_type == "banner":

                        self.profile_data[
                            "banner"
                        ] = item_id


                    # -------------------------
                    # DOS DE CARTE
                    # -------------------------

                    elif item_type == "card_back":

                        self.profile_data[
                            "card_back"
                        ] = item_id


                    self.stats.save()

                    return
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

        # Fond du portrait
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


        # -----------------------------
        # FAUX PERSONNAGE PIXEL
        # -----------------------------

        center_x = (
            x + size // 2
        )


        # Tête
        pygame.draw.rect(
            screen,
            "#5f78ff",
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
            "#5f78ff",
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
            "#5f78ff",
            pygame.Rect(
                center_x - 25,
                y + 115,
                18,
                25
            )
        )

        pygame.draw.rect(
            screen,
            "#5f78ff",
            pygame.Rect(
                center_x + 7,
                y + 115,
                18,
                25
            )
        )


    # -----------------------------
    # CARTE STAT
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


        # -----------------------------
        # BANNIERE
        # -----------------------------

        banner_height = 180

        banner = self.scale_cover(
            self.banner,
            (
                1280,
                banner_height
            )
        )

        screen.blit(
            banner,
            (0, 0)
        )
        banner_overlay = pygame.Surface(
            (
                1280,
                banner_height
            ),
            pygame.SRCALPHA
        )

        banner_overlay.fill(
            (
                8,
                10,
                18,
                65
            )
        )

        screen.blit(
            banner_overlay,
            (0, 0)
        )
        title_id = self.profile_data.get(
            "title",
            "default"
        )

        title_name = self.title_catalog.get(
            title_id,
            "Aucun titre"
        )
        if title_id != "default":

            title_text = self.small_font.render(
                title_name,
                True,
                self.theme["accent_soft"]
            )


            title_rect = pygame.Rect(
                430,
                190,
                title_text.get_width() + 30,
                35
            )


            pygame.draw.rect(
                screen,
                "#3a2338",
                title_rect,
                border_radius=18
            )


            screen.blit(
                title_text,
                (
                    title_rect.x + 15,
                    title_rect.y + 8
                )
    )
        # -----------------------------
        # PERSONNAGE
        # -----------------------------

        # -----------------------------
        # PHOTO DE PROFIL
        # -----------------------------

        avatar_rect = pygame.Rect(
            70,
            90,
            140,
            140
        )

        pygame.draw.rect(
            screen,
            "#11141d",
            avatar_rect,
            border_radius=12
        )

        screen.blit(
            self.profile_icon,
            avatar_rect
        )

        pygame.draw.rect(
            screen,
            "white",
            avatar_rect,
            4,
            border_radius=12
        )


        # -----------------------------
        # NOM
        # -----------------------------

        display_name = self.name_font.render(
            self.profile_data[
                "display_name"
            ],
            True,
            "white"
        )

        screen.blit(
            display_name,
            (240, 155)
        )


        username = self.small_font.render(
            f"@{self.profile_data['username']}",
            True,
            "#999999"
        )

        screen.blit(
            username,
            (240, 200)
        )

        # -----------------------------
        # STATUT
        # -----------------------------

        pygame.draw.circle(
            screen,
            "#5fd68a",
            (1030, 180),
            10
        )

        status_text = self.small_font.render(
            "En ligne",
            True,
            "white"
        )

        screen.blit(
            status_text,
            (1050, 168)
        )

        pygame.draw.rect(
            screen,
            "#34394a",
            self.edit_button,
            border_radius=6
        )

        edit_text = self.small_font.render(
            "MODIFIER",
            True,
            "white"
        )

        edit_rect = edit_text.get_rect(
            center=self.edit_button.center
        )

        screen.blit(
            edit_text,
            edit_rect
        )
        # -----------------------------
        # ONGLETS
        # -----------------------------

        tab_titles = {
            "overview": "APERÇU",
            "stats": "STATS",
            "games": "JEUX",
            "collection": "COLLECTION"
        }


        for tab_name, rect in self.tabs.items():

            if tab_name == self.current_tab:

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


            text = self.font.render(
                tab_titles[
                    tab_name
                ],
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


        # -----------------------------
        # CONTENU
        # -----------------------------
        if self.editing:

            self.draw_edit_profile(
                screen
            )

            return
        # -----------------------------
        # SURFACE SCROLLABLE
        # -----------------------------

        self.content_surface.fill(
            (0, 0, 0, 0)
        )

        self.update_scroll_limits()


        # Position virtuelle de la souris
        content_mouse_pos = (
            mouse_pos[0],
            mouse_pos[1] + self.scroll_y
        )
        if self.current_tab == "collection":

            content_mouse_pos = (
                mouse_pos[0],
                mouse_pos[1] + self.scroll_y
            )

            self.draw_badge_tooltip(
                screen,
                content_mouse_pos
            )

        # -----------------------------
        # CONTENU
        # -----------------------------

        if self.current_tab == "overview":

            self.draw_overview(
                self.content_surface
            )


        elif self.current_tab == "stats":

            self.draw_stats(
                self.content_surface
            )


        elif self.current_tab == "games":

            self.draw_games(
                self.content_surface
            )

        elif self.current_tab == "collection":

            self.draw_collection(
                self.content_surface,
                content_mouse_pos
            )


        # -----------------------------
        # AFFICHAGE DU CONTENU
        # -----------------------------

        visible_height = (
            720
            - self.content_top
        )

        source_rect = pygame.Rect(
            0,
            self.content_top + self.scroll_y,
            1280,
            visible_height
        )


        screen.blit(
            self.content_surface,
            (0, self.content_top),
            source_rect
        )


        # -----------------------------
        # RETOUR
        # -----------------------------

        back_text = self.small_font.render(
            "ESC - Retour",
            True,
            "#888888"
        )

        screen.blit(
            back_text,
            (1100, 680)
        )

        self.draw_scrollbar(
            screen
        )
    # -----------------------------
    # APERCU
    # -----------------------------

    def draw_overview(
        self,
        screen
    ):

        # =================================================
        # COLONNE GAUCHE
        # =================================================

        left_x = 70
        left_width = 730

        # =================================================
        # COLONNE DROITE
        # =================================================

        right_x = 830
        right_width = 380


        # =================================================
        # À PROPOS
        # =================================================

        about_rect = pygame.Rect(
            left_x,
            330,
            left_width,
            145
        )

        self.draw_panel(
            screen,
            about_rect,
            "À propos"
        )


        bio = self.profile_data.get(
            "bio",
            "Aucune bio."
        )

        bio_text = self.font.render(
            bio,
            True,
            self.theme["text"]
        )

        screen.blit(
            bio_text,
            (
                about_rect.x + 20,
                about_rect.y + 55
            )
        )


        # -----------------------------
        # LANGUES
        # -----------------------------

        language_label = self.small_font.render(
            "LANGUES",
            True,
            self.theme["muted"]
        )

        screen.blit(
            language_label,
            (
                about_rect.x + 20,
                about_rect.y + 100
            )
        )


        languages = [
            "Français",
            "English"
        ]

        x = about_rect.x + 110

        for language in languages:

            text = self.small_font.render(
                language,
                True,
                self.theme["text"]
            )

            tag_rect = pygame.Rect(
                x,
                about_rect.y + 91,
                text.get_width() + 30,
                35
            )

            pygame.draw.rect(
                screen,
                self.theme["panel_alt"],
                tag_rect,
                border_radius=18
            )

            screen.blit(
                text,
                (
                    tag_rect.x + 15,
                    tag_rect.y + 8
                )
            )

            x += tag_rect.width + 10


        # =================================================
        # PERSONNAGE
        # =================================================

        character_rect = pygame.Rect(
            left_x,
            495,
            300,
            290
        )

        self.draw_panel(
            screen,
            character_rect,
            "Personnage"
        )


        preview_rect = (
            self.character_preview.get_rect(
                center=(
                    character_rect.centerx,
                    character_rect.centery + 20
                )
            )
        )

        screen.blit(
            self.character_preview,
            preview_rect
        )


        # =================================================
        # STATS RAPIDES
        # =================================================

        stats_rect = pygame.Rect(
            390,
            495,
            410,
            290
        )

        self.draw_panel(
            screen,
            stats_rect,
            "Résumé"
        )


        games = self.stats.data.get(
            "games",
            {}
        )


        stat_width = 115

        self.draw_small_stat(
            screen,
            pygame.Rect(
                410,
                550,
                stat_width,
                80
            ),
            self.stats.get_playtime_text(),
            "Temps"
        )


        self.draw_small_stat(
            screen,
            pygame.Rect(
                410,
                550,
                115,
                105
            ),
            self.stats.get_playtime_text(),
            "Temps",
            self.profile_icons["time"]
        )


        self.draw_small_stat(
            screen,
            pygame.Rect(
                535,
                550,
                115,
                105
            ),
            self.stats.data.get(
                "launch_count",
                0
            ),
            "Sessions",
            self.profile_icons["calendar"]
        )


        self.draw_small_stat(
            screen,
            pygame.Rect(
                660,
                550,
                115,
                105
            ),
            len(games),
            "Jeux",
            self.profile_icons["games"]
        )

        # -----------------------------
        # PREMIER LANCEMENT
        # -----------------------------

        first_launch = self.format_date(
            self.stats.data.get(
                "first_launch"
            )
        )


        first_label = self.small_font.render(
            "MEMBRE DEPUIS",
            True,
            self.theme["muted"]
        )

        screen.blit(
            first_label,
            (
                stats_rect.x + 20,
                stats_rect.y + 165
            )
        )


        first_text = self.font.render(
            first_launch,
            True,
            self.theme["text"]
        )

        screen.blit(
            first_text,
            (
                stats_rect.x + 20,
                stats_rect.y + 195
            )
        )


        # =================================================
        # ACTIVITÉ ACTUELLE
        # =================================================

        activity_rect = pygame.Rect(
            right_x,
            330,
            right_width,
            150
        )

        self.draw_panel(
            screen,
            activity_rect,
            "Activité actuelle"
        )


        active_game = getattr(
            self.stats,
            "active_game",
            None
        )


        if active_game:

            activity = (
                "Joue à "
                + self.get_game_name(
                    active_game
                )
            )

            activity_color = (
                self.theme["accent"]
            )

        else:

            activity = "Dans le hub"

            activity_color = (
                self.theme["online"]
            )


        # Petit indicateur
        pygame.draw.circle(
            screen,
            activity_color,
            (
                activity_rect.x + 28,
                activity_rect.y + 72
            ),
            8
        )


        activity_text = self.font.render(
            activity,
            True,
            self.theme["text"]
        )

        screen.blit(
            activity_text,
            (
                activity_rect.x + 50,
                activity_rect.y + 58
            )
        )


        # =================================================
        # PROGRESSION
        # =================================================
        progression_rect = pygame.Rect(
            right_x,
            500,
            right_width,
            175
        )
        progression_content_x = (
            progression_rect.x + 50
        )

        xp_icon = self.profile_icons[
            "xp"
        ]

        if xp_icon is not None:

            xp_icon = pygame.transform.smoothscale(
                xp_icon,
                (
                    36,
                    36
                )
            )

            screen.blit(
                xp_icon,
                (
                    progression_rect.x + 8,
                    progression_rect.y + 50
                )
            )

        self.draw_panel(
            screen,
            progression_rect,
            "Progression"
        )


        level = (
            self.progression.get_level()
        )

        xp = (
            self.progression.get_xp()
        )

        required = (
            self.progression.get_xp_required()
        )


        level_text = self.name_font.render(
            f"Niveau {level}",
            True,
            self.theme["text"]
        )

        screen.blit(
            level_text,
            (
                progression_content_x,
                progression_rect.y + 52
            )
        )


        # -----------------------------
        # BARRE XP
        # -----------------------------

        bar_rect = pygame.Rect(
            progression_content_x,
            progression_rect.y + 110,
            progression_rect.width - 100,
            30
        )


        pygame.draw.rect(
            screen,
            self.theme["panel_alt"],
            bar_rect,
            border_radius=8
        )


        progress = (
            xp / required
            if required > 0
            else 0
        )

        progress = max(
            0,
            min(
                1,
                progress
            )
        )


        fill_rect = pygame.Rect(
            bar_rect.x,
            bar_rect.y,
            int(
                bar_rect.width
                * progress
            ),
            bar_rect.height
        )


        pygame.draw.rect(
            screen,
            self.theme["accent"],
            fill_rect,
            border_radius=8
        )


        xp_text = self.small_font.render(
            f"{xp} / {required} XP",
            True,
            self.theme["text"]
        )

        xp_text_rect = xp_text.get_rect(
            center=bar_rect.center
        )

        screen.blit(
            xp_text,
            xp_text_rect
        )


        # =================================================
        # JEU FAVORI
        # =================================================

        favorite_rect = pygame.Rect(
            right_x,
            695,
            right_width,
            160
        )

        self.draw_panel(
            screen,
            favorite_rect,
            "Jeu favori"
        )


        game_id, game_data = (
            self.get_favorite_game()
        )


        if game_id is None:

            favorite_text = self.font.render(
                "Aucun jeu",
                True,
                self.theme["muted"]
            )

            screen.blit(
                favorite_text,
                (
                    favorite_rect.x + 20,
                    favorite_rect.y + 65
                )
            )

        else:

            name = self.get_game_name(
                game_id
            )

            game_name = self.name_font.render(
                name,
                True,
                self.theme["text"]
            )

            screen.blit(
                game_name,
                (
                    favorite_rect.x + 20,
                    favorite_rect.y + 50
                )
            )


            playtime = (
                self.stats.format_time(
                    game_data.get(
                        "playtime_seconds",
                        0
                    )
                )
            )


            time_text = self.small_font.render(
                playtime,
                True,
                self.theme["accent_soft"]
            )

            screen.blit(
                time_text,
                (
                    favorite_rect.x + 20,
                    favorite_rect.y + 105
                )
            )


        # =================================================
        # ACTIVITÉ RÉCENTE
        # =================================================

        recent_rect = pygame.Rect(
            left_x,
            810,
            left_width,
            250
        )

        self.draw_panel(
            screen,
            recent_rect,
            "Activité récente"
        )


        recent_games = (
            self.get_recent_games()
        )


        if not recent_games:

            empty_text = self.font.render(
                "Aucune activité récente.",
                True,
                self.theme["muted"]
            )

            screen.blit(
                empty_text,
                (
                    recent_rect.x + 20,
                    recent_rect.y + 65
                )
            )

        else:

            y = recent_rect.y + 55


            for game_id, data in recent_games:

                name = self.get_game_name(
                    game_id
                )


                name_text = self.font.render(
                    name,
                    True,
                    self.theme["text"]
                )

                screen.blit(
                    name_text,
                    (
                        recent_rect.x + 20,
                        y
                    )
                )


                last_played = self.format_date(
                    data.get(
                        "last_played"
                    )
                )


                date_text = self.small_font.render(
                    last_played,
                    True,
                    self.theme["muted"]
                )

                screen.blit(
                    date_text,
                    (
                        recent_rect.x + 300,
                        y + 5
                    )
                )


                playtime = (
                    self.stats.format_time(
                        data.get(
                            "playtime_seconds",
                            0
                        )
                    )
                )


                time_text = self.small_font.render(
                    playtime,
                    True,
                    self.theme["accent_soft"]
                )

                screen.blit(
                    time_text,
                    (
                        recent_rect.right - 110,
                        y + 5
                    )
                )


                y += 58


        # =================================================
        # BADGES
        # =================================================

        badge_rect = pygame.Rect(
            right_x,
            875,
            right_width,
            185
        )

        self.draw_panel(
            screen,
            badge_rect,
            "Badges"
        )


        # Pour l'instant placeholders.
        # Plus tard ils viendront du système
        # de succès.

        badges = self.get_profile_badges()


        if not badges:

            empty_text = self.small_font.render(
                "Aucun badge pour le moment",
                True,
                self.theme["muted"]
            )

            screen.blit(
                empty_text,
                (
                    badge_rect.x + 20,
                    badge_rect.y + 75
                )
            )

        else:

            x = badge_rect.x + 55

            for badge in badges[:3]:

                image = self.badge_images.get(
                    badge["id"]
                )

                if image is None:
                    continue


                badge_image = (
                    pygame.transform.smoothscale(
                        image,
                        (
                            72,
                            72
                        )
                    )
                )


                badge_image_rect = (
                    badge_image.get_rect(
                        center=(
                            x,
                            badge_rect.y + 95
                        )
                    )
                )


                screen.blit(
                    badge_image,
                    badge_image_rect
                )


                # Nom
                name_text = self.small_font.render(
                    badge["name"],
                    True,
                    self.theme["text"]
                )

                name_rect = name_text.get_rect(
                    center=(
                        x,
                        badge_rect.y + 145
                    )
                )

                screen.blit(
                    name_text,
                    name_rect
                )


                x += 110
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
            self.stats.get_playtime_text()
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
            self.stats.data[
                "launch_count"
            ]
        )


        first_launch = self.format_date(
            self.stats.data.get(
                "first_launch"
            )
        )


        last_launch = self.format_date(
            self.stats.data.get(
                "last_launch"
            )
        )


        first_text = self.font.render(
            f"Premier lancement : {first_launch}",
            True,
            "white"
        )

        screen.blit(
            first_text,
            (90, 530)
        )


        last_text = self.font.render(
            f"Dernier lancement : {last_launch}",
            True,
            "white"
        )

        screen.blit(
            last_text,
            (90, 575)
        )


    # -----------------------------
    # JEUX
    # -----------------------------

    def draw_games(
    self,
    screen
):

        title = self.title_font.render(
            "Mes jeux",
            True,
            "white"
        )

        screen.blit(
            title,
            (90, 330)
        )


        games = self.stats.data.get(
            "games",
            {}
        )


        if not games:

            empty_text = self.font.render(
                "Aucun jeu joue pour le moment.",
                True,
                "#888888"
            )

            screen.blit(
                empty_text,
                (90, 410)
            )

            return


        # -----------------------------
        # NOMS PROPRES
        # -----------------------------

        game_names = {
            "uno": "UNO",
            "rhythm_game": "Rhythm Game",
            "coffee_game": "Coffee Game"
        }


        y = 400


        for game_id, game_data in games.items():

            card_rect = pygame.Rect(
                90,
                y,
                1000,
                110
            )


            # -------------------------
            # CARTE
            # -------------------------

            pygame.draw.rect(
                screen,
                "#202431",
                card_rect,
                border_radius=8
            )

            pygame.draw.rect(
                screen,
                "#34394a",
                card_rect,
                2,
                border_radius=8
            )


            # -------------------------
            # ICONE PLACEHOLDER
            # -------------------------

            icon_rect = pygame.Rect(
                card_rect.x + 20,
                card_rect.y + 15,
                80,
                80
            )

            pygame.draw.rect(
                screen,
                "#34394a",
                icon_rect,
                border_radius=8
            )

            pygame.draw.circle(
                screen,
                "#5f78ff",
                icon_rect.center,
                20
            )


            # -------------------------
            # NOM
            # -------------------------

            name = game_names.get(
                game_id,
                game_id.replace(
                    "_",
                    " "
                ).title()
            )


            name_text = self.font.render(
                name,
                True,
                "white"
            )

            screen.blit(
                name_text,
                (
                    card_rect.x + 125,
                    card_rect.y + 18
                )
            )


            # -------------------------
            # TEMPS
            # -------------------------

            playtime_seconds = game_data.get(
                "playtime_seconds",
                0
            )

            playtime = self.stats.format_time(
                playtime_seconds
            )


            playtime_text = self.small_font.render(
                f"Temps : {playtime}",
                True,
                "#aaaaaa"
            )

            screen.blit(
                playtime_text,
                (
                    card_rect.x + 125,
                    card_rect.y + 55
                )
            )


            # -------------------------
            # LANCEMENTS
            # -------------------------

            launches = game_data.get(
                "launch_count",
                0
            )


            launches_text = self.small_font.render(
                f"Lancements : {launches}",
                True,
                "#aaaaaa"
            )

            screen.blit(
                launches_text,
                (
                    card_rect.x + 330,
                    card_rect.y + 55
                )
            )


            # -------------------------
            # DERNIERE SESSION
            # -------------------------

            last_played = self.format_date(
                game_data.get(
                    "last_played"
                )
            )


            last_text = self.small_font.render(
                f"Derniere partie : {last_played}",
                True,
                "#aaaaaa"
            )

            screen.blit(
                last_text,
                (
                    card_rect.x + 530,
                    card_rect.y + 55
                )
            )


            y += 125
    def draw_collection(
        self,
        screen,
        mouse_pos
    ):

        # On reconstruit les boutons
        self.collection_buttons = []


        unlocks = self.stats.data.get(
            "unlocks",
            {}
        )


        # -----------------------------
        # TITRE PAGE
        # -----------------------------

        title = self.title_font.render(
            "Collection",
            True,
            "white"
        )

        screen.blit(
            title,
            (90, 330)
        )


        # =================================================
        # TITRES
        # =================================================

        section = self.small_font.render(
            "TITRES",
            True,
            "#888888"
        )

        screen.blit(
            section,
            (90, 390)
        )


        unlocked_titles = unlocks.get(
            "titles",
            []
        )


        x = 90

        for title_id in unlocked_titles:

            title_name = self.title_catalog.get(
                title_id,
                title_id
            )

            rect = pygame.Rect(
                x,
                420,
                190,
                55
            )


            selected = (
                self.profile_data[
                    "title"
                ]
                == title_id
            )


            self.draw_collection_button(
                screen,
                rect,
                title_name,
                selected,
                mouse_pos
            )


            self.collection_buttons.append(
                {
                    "rect": rect,
                    "type": "title",
                    "id": title_id
                }
            )


            x += 205


        # =================================================
        # BANNIERES
        # =================================================

        section = self.small_font.render(
            "BANNIERES",
            True,
            "#888888"
        )
        self.draw_characters(
            screen,
            mouse_pos,
            350
        )
        screen.blit(
            section,
            (90, 500)
        )


        unlocked_banners = unlocks.get(
            "banners",
            []
        )


        x = 90

        for banner_id in unlocked_banners:

            banner_data = self.banner_catalog.get(
                banner_id
            )

            if banner_data is None:
                continue


            rect = pygame.Rect(
                x,
                530,
                190,
                55
            )


            selected = (
                self.profile_data[
                    "banner"
                ]
                == banner_id
            )


            pygame.draw.rect(
                screen,
                banner_data["color"],
                rect,
                border_radius=6
            )


            border_color = (
                "white"
                if selected
                else "#555555"
            )


            pygame.draw.rect(
                screen,
                border_color,
                rect,
                3,
                border_radius=6
            )


            banner_text = self.small_font.render(
                banner_data["name"],
                True,
                "white"
            )


            text_rect = banner_text.get_rect(
                center=rect.center
            )

            screen.blit(
                banner_text,
                text_rect
            )


            self.collection_buttons.append(
                {
                    "rect": rect,
                    "type": "banner",
                    "id": banner_id
                }
            )


            x += 205


        # =================================================
        # DOS DE CARTES
        # =================================================

        section = self.small_font.render(
            "DOS DE CARTES",
            True,
            "#888888"
        )

        screen.blit(
            section,
            (90, 610)
        )


        unlocked_cards = unlocks.get(
            "card_backs",
            []
        )


        x = 90

        for card_id in unlocked_cards:

            card_data = self.card_back_catalog.get(
                card_id
            )

            if card_data is None:
                continue


            rect = pygame.Rect(
                x,
                640,
                190,
                55
            )


            selected = (
                self.profile_data[
                    "card_back"
                ]
                == card_id
            )


            pygame.draw.rect(
                screen,
                card_data["color"],
                rect,
                border_radius=6
            )


            border_color = (
                "white"
                if selected
                else "#555555"
            )


            pygame.draw.rect(
                screen,
                border_color,
                rect,
                3,
                border_radius=6
            )


            text = self.small_font.render(
                card_data["name"],
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


            self.collection_buttons.append(
                {
                    "rect": rect,
                    "type": "card_back",
                    "id": card_id
                }
            )


            x += 205

        self.draw_badges_collection(
            screen,
            mouse_pos,
            730
        )
    def draw_collection_button(
        self,
        screen,
        rect,
        text,
        selected,
        mouse_pos
    ):

        if selected:

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


        pygame.draw.rect(
            screen,
            "white"
            if selected
            else "#444444",
            rect,
            2,
            border_radius=6
        )


        rendered = self.small_font.render(
            text,
            True,
            "white"
        )


        text_rect = rendered.get_rect(
            center=rect.center
        )


        screen.blit(
            rendered,
            text_rect
        )
    def start_editing(self):

        self.editing = True

        self.edit_field = None

        self.edit_values[
            "display_name"
        ] = self.profile_data[
            "display_name"
        ]

        self.edit_values[
            "username"
        ] = self.profile_data[
            "username"
        ]

        self.edit_values[
            "bio"
        ] = self.profile_data[
            "bio"
        ]
    
    def save_profile(self):

        name = self.edit_values[
            "display_name"
        ].strip()

        username = self.edit_values[
            "username"
        ].strip()

        bio = self.edit_values[
            "bio"
        ].strip()


        if name:
            self.profile_data[
                "display_name"
            ] = name


        if username:

            # Pas besoin d'écrire @
            username = username.replace(
                "@",
                ""
            )

            self.profile_data[
                "username"
            ] = username


        self.profile_data[
            "bio"
        ] = bio


        self.stats.save()

        self.editing = False

        self.edit_field = None
    
    def draw_edit_profile(self, screen):

        title = self.title_font.render(
            "Modifier le profil",
            True,
            "white"
        )

        screen.blit(
            title,
            (350, 310)
        )


        fields = [
            (
                "display_name",
                "Nom",
                self.name_input
            ),

            (
                "username",
                "Username",
                self.username_input
            ),

            (
                "bio",
                "Bio",
                self.bio_input
            )
        ]


        for field_name, label, rect in fields:

            # Label
            label_text = self.small_font.render(
                label,
                True,
                "#888888"
            )

            screen.blit(
                label_text,
                (
                    rect.x - 120,
                    rect.y + 15
                )
            )


            # Fond
            if self.edit_field == field_name:

                border = "#5f78ff"

            else:

                border = "#444444"


            pygame.draw.rect(
                screen,
                "#202431",
                rect,
                border_radius=6
            )


            pygame.draw.rect(
                screen,
                border,
                rect,
                3,
                border_radius=6
            )


            # Valeur
            value = self.edit_values[
                field_name
            ]

            value_text = self.font.render(
                value,
                True,
                "white"
            )

            screen.blit(
                value_text,
                (
                    rect.x + 15,
                    rect.y + 12
                )
            )


        # -----------------------------
        # SAUVEGARDER
        # -----------------------------

        pygame.draw.rect(
            screen,
            "#5f78ff",
            self.save_button,
            border_radius=6
        )


        save_text = self.font.render(
            "SAUVEGARDER",
            True,
            "white"
        )

        save_rect = save_text.get_rect(
            center=self.save_button.center
        )

        screen.blit(
            save_text,
            save_rect
        )
    def get_content_bottom(self):
        
        #Retourne la hauteur totale nécessaire
        #selon l'onglet actuel.
        

        if self.current_tab == "overview":
            return 1100

        if self.current_tab == "stats":
            return 700

        if self.current_tab == "collection":

            badge_count = len(
                self.get_profile_badges()
            )

            badge_rows = max(
                1,
                (
                    badge_count + 4
                ) // 5
            )

            return (
                850
                + badge_rows * 145
            )
        if self.current_tab == "games":

            games = self.stats.data.get(
                "games",
                {}
            )

            # Premier jeu vers y=400
            # chaque carte fait environ 125 px
            return max(
                720,
                400 + len(games) * 125 + 40
            )

        return 720


    def update_scroll_limits(self):

        content_bottom = self.get_content_bottom()

        # 720 = bas de l'écran logique
        self.max_scroll = max(
            0,
            content_bottom - 720
        )

        self.scroll_y = max(
            0,
            min(
                self.scroll_y,
                self.max_scroll
            )
        )
    def draw_scrollbar(self, screen):

        if self.max_scroll <= 0:
            return


        # -----------------------------
        # ZONE
        # -----------------------------

        track = pygame.Rect(
            1258,
            self.content_top + 10,
            8,
            720 - self.content_top - 20
        )


        pygame.draw.rect(
            screen,
            "#202431",
            track,
            border_radius=4
        )


        # -----------------------------
        # TAILLE DU CURSEUR
        # -----------------------------

        visible_height = (
            720
            - self.content_top
        )

        total_height = (
            visible_height
            + self.max_scroll
        )


        thumb_height = max(
            40,
            int(
                track.height
                * (
                    visible_height
                    / total_height
                )
            )
        )


        # -----------------------------
        # POSITION
        # -----------------------------

        progress = (
            self.scroll_y
            / self.max_scroll
        )


        thumb_y = (
            track.y
            + int(
                (
                    track.height
                    - thumb_height
                )
                * progress
            )
        )


        thumb = pygame.Rect(
            track.x,
            thumb_y,
            track.width,
            thumb_height
        )


        pygame.draw.rect(
            screen,
            "#5f78ff",
            thumb,
            border_radius=4
        )
    
    def draw_panel(
        self,
        screen,
        rect,
        title=None
    ):
        pygame.draw.rect(
            screen,
            self.theme["panel"],
            rect,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            self.theme["border"],
            rect,
            2,
            border_radius=12
        )

        if title is not None:

            title_text = self.small_font.render(
                title.upper(),
                True,
                self.theme["muted"]
            )

            screen.blit(
                title_text,
                (
                    rect.x + 20,
                    rect.y + 16
                )
            )


    def draw_small_stat(
        self,
        screen,
        rect,
        value,
        label,
        icon=None
    ):

        pygame.draw.rect(
            screen,
            self.theme["panel_alt"],
            rect,
            border_radius=10
        )


        # -------------------------
        # ICONE
        # -------------------------

        if icon is not None:

            icon_image = pygame.transform.smoothscale(
                icon,
                (
                    32,
                    32
                )
            )

            icon_rect = icon_image.get_rect(
                center=(
                    rect.centerx,
                    rect.y + 25
                )
            )

            screen.blit(
                icon_image,
                icon_rect
            )

            value_y = rect.y + 56
            label_y = rect.y + 79

        else:

            value_y = rect.y + 27
            label_y = rect.y + 57


        # -------------------------
        # VALEUR
        # -------------------------

        value_text = self.small_font.render(
            str(value),
            True,
            self.theme["text"]
        )

        value_rect = value_text.get_rect(
            center=(
                rect.centerx,
                value_y
            )
        )

        screen.blit(
            value_text,
            value_rect
        )


        # -------------------------
        # LABEL
        # -------------------------

        label_text = self.small_font.render(
            label,
            True,
            self.theme["muted"]
        )

        label_rect = label_text.get_rect(
            center=(
                rect.centerx,
                label_y
            )
        )

        screen.blit(
            label_text,
            label_rect
        )
    def get_game_name(
        self,
        game_id
    ):

        names = {
            "uno": "UNO",
            "rhythm_game": "Rhythm Game",
            "coffee_game": "Coffee Game"
        }

        return names.get(
            game_id,
            game_id.replace(
                "_",
                " "
            ).title()
        )
        
    def get_favorite_game(self):

        games = self.stats.data.get(
            "games",
            {}
        )

        if not games:
            return None, None


        game_id = max(
            games,
            key=lambda game: games[game].get(
                "playtime_seconds",
                0
            )
        )

        return (
            game_id,
            games[game_id]
        )
    def get_recent_games(
        self,
        limit=3
    ):

        games = self.stats.data.get(
            "games",
            {}
        )

        items = []

        for game_id, data in games.items():

            last_played = data.get(
                "last_played"
            )

            if last_played is None:
                continue

            items.append(
                (
                    game_id,
                    data
                )
            )


        items.sort(
            key=lambda item: item[1].get(
                "last_played",
                ""
            ),
            reverse=True
        )

        return items[:limit]

    def get_profile_badges(self):

        badges = []

        added = set()


        badge_catalog = {

            "level": {
                "id": "level",
                "name": "Progression",
                "description": "Atteindre le niveau 5"
            },

            "playtime": {
                "id": "playtime",
                "name": "Habitué",
                "description": "Jouer pendant 1 heure"
            },

            "arcade": {
                "id": "arcade",
                "name": "Arcade",
                "description": "Lancer 5 parties"
            },

            "social": {
                "id": "social",
                "name": "Social",
                "description": "Jouer avec des amis"
            }
        }


        def add_badge(
            badge_id
        ):

            if badge_id in added:
                return

            badge = badge_catalog.get(
                badge_id
            )

            if badge is None:
                return

            badges.append(
                badge
            )

            added.add(
                badge_id
            )


        # -------------------------
        # BADGES NORMAUX
        # -------------------------

        if (
            self.progression.get_level()
            >= 5
        ):

            add_badge(
                "level"
            )


        if (
            self.stats.get_total_seconds()
            >= 3600
        ):

            add_badge(
                "playtime"
            )


        games = self.stats.data.get(
            "games",
            {}
        )


        total_launches = sum(
            game.get(
                "launch_count",
                0
            )
            for game
            in games.values()
        )


        if total_launches >= 5:

            add_badge(
                "arcade"
            )


        # -------------------------
        # BADGES FORCES PAR ADMIN
        # -------------------------

        forced_badges = (
            self.stats.data
            .get(
                "unlocks",
                {}
            )
            .get(
                "badges",
                []
            )
        )


        for badge_id in forced_badges:

            add_badge(
                badge_id
            )


        return badges

    def load_profile_image(
        self,
        path
    ):

        try:

            return pygame.image.load(
                path
            ).convert_alpha()

        except (
            pygame.error,
            FileNotFoundError
        ):

            print(
                f"Asset introuvable : {path}"
            )

            return None
    def get_banner(self):

        character = self.profile_data.get(
            "character",
            "lucie"
        )

        path = (
            self.profile_assets
            / "banners"
            / f"{character}.png"
        )

        if not path.exists():

            path = (
                self.profile_assets
                / "banners"
                / "lucie.png"
            )

        return pygame.image.load(
            path
        ).convert_alpha()
    
    def scale_cover(
        self,
        image,
        size
    ):

        target_w, target_h = size

        image_w = image.get_width()
        image_h = image.get_height()

        scale = max(
            target_w / image_w,
            target_h / image_h
        )

        new_w = int(
            image_w * scale
        )

        new_h = int(
            image_h * scale
        )

        image = pygame.transform.smoothscale(
            image,
            (
                new_w,
                new_h
            )
        )

        x = (
            new_w - target_w
        ) // 2

        y = (
            new_h - target_h
        ) // 2

        return image.subsurface(
            pygame.Rect(
                x,
                y,
                target_w,
                target_h
            )
        ).copy()
    
    def draw_badges_collection(
        self,
        screen,
        mouse_pos,
        start_y
    ):
        badges = self.get_profile_badges()

        self.badge_rects = []

        title = self.small_font.render(
            "BADGES",
            True,
            self.theme["muted"]
        )

        screen.blit(
            title,
            (90, start_y)
        )

        if not badges:

            empty = self.font.render(
                "Aucun badge débloqué.",
                True,
                self.theme["muted"]
            )

            screen.blit(
                empty,
                (90, start_y + 45)
            )

            return start_y + 100

        # -----------------------------
        # GRILLE
        # -----------------------------

        columns = 5

        badge_size = 100
        spacing_x = 135
        spacing_y = 145

        start_x = 90

        for index, badge in enumerate(badges):

            column = index % columns
            row = index // columns

            x = start_x + column * spacing_x
            y = start_y + 45 + row * spacing_y

            rect = pygame.Rect(
                x,
                y,
                badge_size,
                badge_size
            )

            image = self.badge_images.get(
                badge["id"]
            )

            # -------------------------
            # IMAGE
            # -------------------------

            if image is not None:

                badge_image = pygame.transform.smoothscale(
                    image,
                    (
                        badge_size,
                        badge_size
                    )
                )

                screen.blit(
                    badge_image,
                    rect
                )

            else:

                pygame.draw.rect(
                    screen,
                    self.theme["panel_alt"],
                    rect,
                    border_radius=10
                )

            # -------------------------
            # HOVER
            # -------------------------

            if rect.collidepoint(
                mouse_pos
            ):

                pygame.draw.rect(
                    screen,
                    self.theme["accent"],
                    rect,
                    3,
                    border_radius=10
                )

            # -------------------------
            # NOM
            # -------------------------

            name = self.badge_catalog.get(
                badge["id"],
                {}
            ).get(
                "name",
                badge["name"]
            )

            name_text = self.small_font.render(
                name,
                True,
                self.theme["text"]
            )

            name_rect = name_text.get_rect(
                center=(
                    rect.centerx,
                    rect.bottom + 18
                )
            )

            screen.blit(
                name_text,
                name_rect
            )

            self.badge_rects.append(
                {
                    "rect": rect,
                    "id": badge["id"]
                }
            )

        rows = (
            len(badges)
            + columns
            - 1
        ) // columns

        return (
            start_y
            + 45
            + rows * spacing_y
        )
        
    def draw_badge_tooltip(
        self,
        screen,
        mouse_pos
    ):
        for badge in self.badge_rects:

            if not badge["rect"].collidepoint(
                mouse_pos
            ):
                continue

            badge_data = self.badge_catalog.get(
                badge["id"]
            )

            if badge_data is None:
                return

            name = badge_data["name"]
            description = badge_data[
                "description"
            ]

            width = 300
            height = 90

            x = mouse_pos[0] + 20
            y = mouse_pos[1] + 20

            # Empêche le tooltip
            # de sortir de l'écran
            if x + width > 1260:
                x = mouse_pos[0] - width - 20

            if y + height > 700:
                y = mouse_pos[1] - height - 20

            tooltip = pygame.Rect(
                x,
                y,
                width,
                height
            )

            pygame.draw.rect(
                screen,
                "#10131d",
                tooltip,
                border_radius=8
            )

            pygame.draw.rect(
                screen,
                self.theme["border"],
                tooltip,
                2,
                border_radius=8
            )

            name_text = self.font.render(
                name,
                True,
                self.theme["text"]
            )

            screen.blit(
                name_text,
                (
                    tooltip.x + 15,
                    tooltip.y + 12
                )
            )

            desc_text = self.small_font.render(
                description,
                True,
                self.theme["muted"]
            )

            screen.blit(
                desc_text,
                (
                    tooltip.x + 15,
                    tooltip.y + 52
                )
            )

            return
    def equip_character(
        self,
        character_id
    ):
        if character_id not in CHARACTERS:
            return

        self.profile_data[
            "character"
        ] = character_id

        self.stats.save()

        self.load_character_assets()

        # Signale à main.py que le perso
        # vient de changer
        self.character_changed = (
            character_id
        )
    def load_character_assets(self):

        character_id = (
            self.profile_data.get(
                "character",
                "lucie"
            )
        )

        character = CHARACTERS.get(
            character_id,
            CHARACTERS["lucie"]
        )

        folder = character[
            "folder"
        ]


        # =================================
        # PROFILE ICON
        # =================================

        icon_path = (
            Path("assets")
            / "characters"
            / folder
            / "profile_icon.png"
        )

        try:

            self.profile_icon = (
                pygame.image.load(
                    icon_path
                ).convert_alpha()
            )

            self.profile_icon = (
                pygame.transform.smoothscale(
                    self.profile_icon,
                    (140, 140)
                )
            )

        except (
            pygame.error,
            FileNotFoundError
        ):

            self.profile_icon = None


        # =================================
        # CHARACTER PREVIEW
        # =================================

        idle_path = (
            Path("assets")
            / "characters"
            / folder
            / "idle_aligned.png"
        )

        try:

            sheet = pygame.image.load(
                idle_path
            ).convert_alpha()

            frame_w = (
                sheet.get_width()
                // 4
            )

            frame_h = (
                sheet.get_height()
                // 4
            )

            first_frame = sheet.subsurface(
                pygame.Rect(
                    0,
                    0,
                    frame_w,
                    frame_h
                )
            ).copy()

            self.character_preview = (
                pygame.transform.smoothscale(
                    first_frame,
                    (180, 180)
                )
            )

        except (
            pygame.error,
            FileNotFoundError
        ):

            self.character_preview = None


        # =================================
        # BANNER
        # =================================

        banner_path = (
            Path("assets")
            / "profile"
            / "banners"
            / character["banner"]
        )

        try:

            self.banner = (
                pygame.image.load(
                    banner_path
                ).convert_alpha()
            )

        except (
            pygame.error,
            FileNotFoundError
        ):

            self.banner = None