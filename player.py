import pygame
from asset_paths import asset_path

from characters import CHARACTERS

class Player:
    def __init__(self, x=640, y=360, character_id="pink_girl"):
        # -----------------------------
        # POSITION
        # -----------------------------
        self.x = float(x)
        self.y = float(y)
        self.character_id = None
        # -----------------------------
        # DEPLACEMENT
        # -----------------------------
        self.walk_speed = 170
        self.run_speed = 290

        self.direction = "down"
        self.state = "idle"

        # -----------------------------
        # ANIMATION
        # -----------------------------
        self.frame_index = 0
        self.animation_timer = 0

        self.walk_fps = 7
        self.run_fps = 11
        self.idle_fps = 4

        # Taille affichée dans le jeu
        self.display_width = 96
        self.display_height = 96

        # -----------------------------
        # ANIMATIONS
        # -----------------------------
        self.animations = {
            "idle": {},
            "walk": {},
            "run": {}
        }

        self.set_character(character_id)

    # --------------------------------
    # CHARGER UNE SPRITE SHEET
    # --------------------------------
    
    def load_sheet(self, path, rows=4, cols=4):

        sheet = pygame.image.load(
            path
        ).convert_alpha()

        # --------------------------------
        # TAILLE DIVISIBLE PAR 4
        # --------------------------------

        new_width = (
            sheet.get_width()
            // cols
            * cols
        )

        new_height = (
            sheet.get_height()
            // rows
            * rows
        )

        sheet = pygame.transform.scale(
            sheet,
            (
                new_width,
                new_height
            )
        )

        frame_width = (
            new_width // cols
        )

        frame_height = (
            new_height // rows
        )

        frames = []

        for row in range(rows):

            row_frames = []

            for col in range(cols):

                frame_rect = pygame.Rect(
                    col * frame_width,
                    row * frame_height,
                    frame_width,
                    frame_height
                )

                frame = pygame.Surface(
                    (
                        frame_width,
                        frame_height
                    ),
                    pygame.SRCALPHA
                )

                frame.blit(
                    sheet,
                    (0, 0),
                    frame_rect
                )

                # --------------------------------
                # TROUVE LE PERSONNAGE
                # --------------------------------

                bounds = frame.get_bounding_rect(
                    min_alpha=1
                )

                if bounds.width > 0 and bounds.height > 0:

                    character = frame.subsurface(
                        bounds
                    ).copy()

                    # Nouvelle surface propre
                    normalized = pygame.Surface(
                        (
                            frame_width,
                            frame_height
                        ),
                        pygame.SRCALPHA
                    )

                    # Centre horizontalement
                    x = (
                        frame_width
                        - character.get_width()
                    ) // 2

                    # Aligne les pieds en bas
                    y = (
                        frame_height
                        - character.get_height()
                    )

                    normalized.blit(
                        character,
                        (x, y)
                    )

                    frame = normalized

                # --------------------------------
                # TAILLE DANS LE JEU
                # --------------------------------

                frame = pygame.transform.scale(
                    frame,
                    (
                        self.display_width,
                        self.display_height
                    )
                )

                row_frames.append(
                    frame
                )

            frames.append(
                row_frames
            )

        return frames

    # --------------------------------
    # CHARGER LES ANIMATIONS
    # --------------------------------

    def load_animations(self):
        base_path = asset_path(
            "assets",
            "characters",
            CHARACTERS[self.character_id]["folder"]
        )

        idle_sheet = self.load_sheet(
            base_path / "idle.png"
        )

        walk_sheet = self.load_sheet(
            base_path / "walk.png"
        )

        run_sheet = self.load_sheet(
            base_path / "run.png"
        )

        # Ordre des lignes :
        # 0 = down
        # 1 = left
        # 2 = right
        # 3 = up

        directions = ["down", "left", "right", "up"]

        for i, direction in enumerate(directions):
            self.animations["idle"][direction] = idle_sheet[i]
            self.animations["walk"][direction] = walk_sheet[i]
            self.animations["run"][direction] = run_sheet[i]

    # --------------------------------
    # UPDATE
    # --------------------------------

    def update(self, keys, dt):
        previous_state = self.state
        dx = 0
        dy = 0

        # ZQSD + flèches
        if keys[pygame.K_z] or keys[pygame.K_UP]:
            dy -= 1

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1

        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            dx -= 1

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1

        moving = (dx != 0 or dy != 0)

        # -----------------------------
        # DIRECTION
        # -----------------------------
        if moving:
            if abs(dx) > abs(dy):
                if dx > 0:
                    self.direction = "right"
                else:
                    self.direction = "left"
            else:
                if dy > 0:
                    self.direction = "down"
                else:
                    self.direction = "up"

        # -----------------------------
        # NORMALISATION DIAGONALE
        # -----------------------------
        if dx != 0 and dy != 0:
            length = (dx ** 2 + dy ** 2) ** 0.5
            dx /= length
            dy /= length

        # -----------------------------
        # COURSE
        # -----------------------------
        running = (
            keys[pygame.K_LSHIFT]
            or keys[pygame.K_RSHIFT]
        )

        if moving:
            if running:
                speed = self.run_speed
                self.state = "run"
            else:
                speed = self.walk_speed
                self.state = "walk"

            self.x += dx * speed * dt
            self.y += dy * speed * dt

        else:
            self.state = "idle"

        if self.state != previous_state:
            self.frame_index = 0
            self.animation_timer = 0

        self.update_animation(dt)

    # --------------------------------
    # UPDATE ANIMATION
    # --------------------------------

    def update_animation(self, dt):
        frames = self.animations[self.state][self.direction]

        if self.state == "idle":
            fps = self.idle_fps
        elif self.state == "walk":
            fps = self.walk_fps
        else:
            fps = self.run_fps

        self.animation_timer += dt

        frame_duration = 1 / fps

        if self.animation_timer >= frame_duration:
            self.animation_timer -= frame_duration
            self.frame_index += 1

            if self.frame_index >= len(frames):
                self.frame_index = 0

    # --------------------------------
    # IMAGE ACTUELLE
    # --------------------------------

    def get_current_image(self):
        frames = self.animations[self.state][self.direction]
        return frames[self.frame_index]

    # --------------------------------
    # DRAW
    # --------------------------------

    def draw(self, screen):
        image = self.get_current_image()

        draw_x = int(self.x - image.get_width() / 2)
        draw_y = int(self.y - image.get_height() + 20)

        screen.blit(
            image,
            (draw_x, draw_y)
        )

    # --------------------------------
    # POSITION
    # --------------------------------

    def get_pos(self):
        return int(self.x), int(self.y)
    def set_character(
        self,
        character_id
    ):
        if character_id not in CHARACTERS:
            character_id = "pink_girl"

        self.character_id = character_id

        self.load_animations()

        self.frame_index = 0
        self.animation_timer = 0