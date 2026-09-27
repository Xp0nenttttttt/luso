import json
import time

from pathlib import Path
from datetime import datetime


class StatsManager:
    def __init__(self):

        self.file_path = Path(
            "data/stats.json"
        )

        self.file_path.parent.mkdir(
            exist_ok=True
        )

        # -----------------------------
        # DONNEES
        # -----------------------------

        self.data = {
            "total_playtime_seconds": 0,
            "launch_count": 0,
            "first_launch": None,
            "last_launch": None,
            "games": {}
        }

        self.load()

        # -----------------------------
        # SESSION GLOBALE
        # -----------------------------

        self.session_start = (
            time.perf_counter()
        )

        self.last_saved_elapsed = 0

        # -----------------------------
        # JEU ACTUEL
        # -----------------------------

        self.active_game = None

        self.active_game_start = None

        self.last_game_saved_elapsed = 0

        # -----------------------------
        # LANCEMENT DU HUB
        # -----------------------------

        self.data[
            "launch_count"
        ] += 1

        now = datetime.now().isoformat(
            timespec="seconds"
        )

        self.data[
            "last_launch"
        ] = now

        if self.data[
            "first_launch"
        ] is None:

            self.data[
                "first_launch"
            ] = now

        self.save()

    # -----------------------------
    # LOAD
    # -----------------------------

    def load(self):

        if not self.file_path.exists():
            return

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                loaded_data = json.load(
                    file
                )

            self.data.update(
                loaded_data
            )

        except (
            json.JSONDecodeError,
            OSError
        ):

            print(
                "Impossible de charger les statistiques."
            )

    # -----------------------------
    # SAVE
    # -----------------------------

    def save(self):

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.data,
                file,
                indent=4,
                ensure_ascii=False
            )

    # -----------------------------
    # CREER UN JEU DANS LES STATS
    # -----------------------------

    def ensure_game(
        self,
        game_id
    ):

        games = self.data.setdefault(
            "games",
            {}
        )

        if game_id not in games:

            games[game_id] = {
                "playtime_seconds": 0,
                "launch_count": 0,
                "last_played": None
            }

    # -----------------------------
    # COMMENCER UN JEU
    # -----------------------------

    def start_game(
        self,
        game_id
    ):

        # Si un autre jeu tourne
        if self.active_game is not None:
            self.stop_game()

        self.ensure_game(
            game_id
        )

        game_data = self.data[
            "games"
        ][game_id]

        game_data[
            "launch_count"
        ] += 1

        game_data[
            "last_played"
        ] = datetime.now().isoformat(
            timespec="seconds"
        )

        self.active_game = game_id

        self.active_game_start = (
            time.perf_counter()
        )

        self.last_game_saved_elapsed = 0

        self.save()

    # -----------------------------
    # ARRETER LE JEU
    # -----------------------------

    def stop_game(self):

        if self.active_game is None:
            return

        elapsed = int(
            time.perf_counter()
            - self.active_game_start
        )

        delta = (
            elapsed
            - self.last_game_saved_elapsed
        )

        if delta > 0:

            self.data[
                "games"
            ][self.active_game][
                "playtime_seconds"
            ] += delta

        self.active_game = None

        self.active_game_start = None

        self.last_game_saved_elapsed = 0

        self.save()

    # -----------------------------
    # UPDATE
    # -----------------------------

    def update(self):

        # -------------------------
        # TEMPS GLOBAL
        # -------------------------

        elapsed = int(
            time.perf_counter()
            - self.session_start
        )

        if (
            elapsed
            - self.last_saved_elapsed
            >= 30
        ):

            delta = (
                elapsed
                - self.last_saved_elapsed
            )

            self.data[
                "total_playtime_seconds"
            ] += delta

            self.last_saved_elapsed = (
                elapsed
            )

            self.save()

        # -------------------------
        # TEMPS DU JEU ACTUEL
        # -------------------------

        if self.active_game is not None:

            game_elapsed = int(
                time.perf_counter()
                - self.active_game_start
            )

            if (
                game_elapsed
                - self.last_game_saved_elapsed
                >= 30
            ):

                delta = (
                    game_elapsed
                    - self.last_game_saved_elapsed
                )

                self.data[
                    "games"
                ][self.active_game][
                    "playtime_seconds"
                ] += delta

                self.last_game_saved_elapsed = (
                    game_elapsed
                )

                self.save()

    # -----------------------------
    # TEMPS GLOBAL
    # -----------------------------

    def get_total_seconds(self):

        current_session = int(
            time.perf_counter()
            - self.session_start
        )

        unsaved_time = (
            current_session
            - self.last_saved_elapsed
        )

        return (
            self.data[
                "total_playtime_seconds"
            ]
            + unsaved_time
        )

    def get_playtime_text(self):

        return self.format_time(
            self.get_total_seconds()
        )

    # -----------------------------
    # TEMPS D'UN JEU
    # -----------------------------

    def get_game_seconds(
        self,
        game_id
    ):

        self.ensure_game(
            game_id
        )

        seconds = self.data[
            "games"
        ][game_id][
            "playtime_seconds"
        ]

        # Si c'est actuellement le jeu lancé,
        # on ajoute aussi le temps pas encore sauvegardé.

        if self.active_game == game_id:

            current = int(
                time.perf_counter()
                - self.active_game_start
            )

            unsaved = (
                current
                - self.last_game_saved_elapsed
            )

            seconds += unsaved

        return seconds

    def get_game_playtime_text(
        self,
        game_id
    ):

        return self.format_time(
            self.get_game_seconds(
                game_id
            )
        )

    def get_game_launch_count(
        self,
        game_id
    ):

        self.ensure_game(
            game_id
        )

        return self.data[
            "games"
        ][game_id][
            "launch_count"
        ]

    # -----------------------------
    # FORMAT DU TEMPS
    # -----------------------------

    def format_time(
        self,
        total_seconds
    ):

        hours = (
            total_seconds // 3600
        )

        minutes = (
            total_seconds % 3600
        ) // 60

        return (
            f"{hours}h {minutes:02d}min"
        )

    # -----------------------------
    # FERMETURE
    # -----------------------------

    def close(self):

        # Arrête proprement un jeu
        if self.active_game is not None:

            self.stop_game()

        # Dernières secondes du hub
        elapsed = int(
            time.perf_counter()
            - self.session_start
        )

        delta = (
            elapsed
            - self.last_saved_elapsed
        )

        if delta > 0:

            self.data[
                "total_playtime_seconds"
            ] += delta

        self.save()