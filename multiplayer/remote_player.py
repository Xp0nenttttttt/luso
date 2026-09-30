from pathlib import Path

import math
import pygame


class RemotePlayer:

    DIRECTION_ROWS = {
        "down": 0,
        "left": 1,
        "right": 2,
        "up": 3
    }


    def __init__(
        self,
        player_id,
        name,
        character,
        x,
        y
    ):

        self.player_id = player_id

        self.name = name

        self.character = character

        self.x = x
        self.y = y

        self.target_x = x
        self.target_y = y

        self.direction = "down"
        self.state = "idle"

        self.frame = 0.0

        self.display_size = (
            96,
            96
        )

        self.font = pygame.font.Font(
            None,
            22
        )

        self.frames = {}

        self.load_character()


    # =================================================
    # LOAD SHEET
    # =================================================

    def load_sheet(
        self,
        path
    ):

        if not path.exists():
            return None

        image = pygame.image.load(
            path
        ).convert_alpha()


        frame_w = (
            image.get_width()
            // 4
        )

        frame_h = (
            image.get_height()
            // 4
        )


        rows = []


        for row in range(4):

            row_frames = []

            for column in range(4):

                rect = pygame.Rect(
                    column * frame_w,
                    row * frame_h,
                    frame_w,
                    frame_h
                )


                frame = image.subsurface(
                    rect
                ).copy()


                frame = (
                    pygame.transform.smoothscale(
                        frame,
                        self.display_size
                    )
                )


                row_frames.append(
                    frame
                )


            rows.append(
                row_frames
            )


        return rows


    def load_character(self):

        base = (
            Path("assets")
            / "characters"
            / self.character
        )


        self.frames["idle"] = (
            self.load_sheet(
                base
                / "idle_aligned.png"
            )
        )

        self.frames["walk"] = (
            self.load_sheet(
                base
                / "walk_aligned.png"
            )
        )

        self.frames["run"] = (
            self.load_sheet(
                base
                / "run_aligned.png"
            )
        )


    # =================================================
    # NETWORK STATE
    # =================================================

    def set_network_state(
        self,
        data
    ):

        self.target_x = data[
            "x"
        ]

        self.target_y = data[
            "y"
        ]

        self.direction = data.get(
            "direction",
            "down"
        )

        self.state = data.get(
            "state",
            "idle"
        )


    # =================================================
    # UPDATE
    # =================================================

    def update(
        self,
        dt
    ):

        # Interpolation réseau
        smoothing = (
            1
            - math.exp(
                -12 * dt
            )
        )

        self.x += (
            self.target_x
            - self.x
        ) * smoothing

        self.y += (
            self.target_y
            - self.y
        ) * smoothing


        if self.state == "run":

            fps = 11

        elif self.state == "walk":

            fps = 7

        else:

            fps = 2


        self.frame += (
            fps * dt
        )


    # =================================================
    # DRAW
    # =================================================

    def draw(
        self,
        screen
    ):

        direction_row = (
            self.DIRECTION_ROWS.get(
                self.direction,
                0
            )
        )


        animation = (
            self.frames.get(
                self.state
            )
        )


        if animation is None:

            animation = (
                self.frames.get(
                    "idle"
                )
            )


        if animation is not None:

            frames = animation[
                direction_row
            ]


            if self.state == "idle":

                frame_index = 0

            else:

                frame_index = (
                    int(
                        self.frame
                    )
                    % len(frames)
                )


            image = frames[
                frame_index
            ]


            rect = (
                image.get_rect(
                    midbottom=(
                        int(self.x),
                        int(self.y)
                    )
                )
            )


            screen.blit(
                image,
                rect
            )

        else:

            pygame.draw.circle(
                screen,
                "#58bfe8",
                (
                    int(self.x),
                    int(self.y)
                ),
                20
            )


        # -----------------------------
        # NOM
        # -----------------------------

        name = self.font.render(
            self.name,
            True,
            "white"
        )


        name_rect = (
            name.get_rect(
                center=(
                    int(self.x),
                    int(self.y) - 110
                )
            )
        )


        background = (
            name_rect.inflate(
                14,
                8
            )
        )


        pygame.draw.rect(
            screen,
            "#111522",
            background,
            border_radius=8
        )


        screen.blit(
            name,
            name_rect
        )