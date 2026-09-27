class ProgressionManager:
    def __init__(self, stats):
        self.stats = stats

        # -----------------------------
        # DONNEES PAR DEFAUT
        # -----------------------------

        progression = self.stats.data.setdefault(
            "progression",
            {}
        )

        progression.setdefault(
            "level",
            1
        )

        progression.setdefault(
            "xp",
            0
        )

        progression.setdefault(
            "total_xp",
            0
        )


        # -----------------------------
        # RECOMPENSES DEBLOQUEES
        # -----------------------------

        unlocks = self.stats.data.setdefault(
            "unlocks",
            {}
        )

        unlocks.setdefault(
            "titles",
            ["default"]
        )

        unlocks.setdefault(
            "banners",
            ["default"]
        )

        unlocks.setdefault(
            "card_backs",
            ["default"]
        )

        self.stats.save()


    # -----------------------------
    # XP NECESSAIRE
    # -----------------------------

    def get_xp_required(self, level=None):

        if level is None:
            level = self.get_level()

        # Exemple :
        #
        # Niveau 1 -> 100 XP
        # Niveau 2 -> 150 XP
        # Niveau 3 -> 200 XP
        # Niveau 4 -> 250 XP

        return 100 + (
            (level - 1) * 50
        )


    # -----------------------------
    # GETTERS
    # -----------------------------

    def get_level(self):

        return self.stats.data[
            "progression"
        ][
            "level"
        ]


    def get_xp(self):

        return self.stats.data[
            "progression"
        ][
            "xp"
        ]


    def get_total_xp(self):

        return self.stats.data[
            "progression"
        ][
            "total_xp"
        ]


    # -----------------------------
    # AJOUTER XP
    # -----------------------------

    def add_xp(self, amount):

        if amount <= 0:
            return []

        progression = self.stats.data[
            "progression"
        ]

        progression["xp"] += amount

        progression["total_xp"] += amount


        unlocked_rewards = []


        # -------------------------
        # LEVEL UP
        # -------------------------

        while (
            progression["xp"]
            >= self.get_xp_required(
                progression["level"]
            )
        ):

            required = self.get_xp_required(
                progression["level"]
            )

            progression["xp"] -= required

            progression["level"] += 1


            # Vérifie les récompenses
            new_rewards = (
                self.check_level_rewards(
                    progression["level"]
                )
            )

            unlocked_rewards.extend(
                new_rewards
            )


        self.stats.save()

        return unlocked_rewards


    # -----------------------------
    # RECOMPENSES DE NIVEAU
    # -----------------------------

    def check_level_rewards(
        self,
        level
    ):

        rewards = []

        # Niveau 5
        if level == 5:

            if self.unlock_title(
                "arcade_regular"
            ):

                rewards.append(
                    "Titre : Arcade Regular"
                )


        # Niveau 10
        if level == 10:

            if self.unlock_banner(
                "blue_wave"
            ):

                rewards.append(
                    "Banniere : Blue Wave"
                )


        # Niveau 15
        if level == 15:

            if self.unlock_card_back(
                "retro_blue"
            ):

                rewards.append(
                    "Dos de carte : Retro Blue"
                )


        # Niveau 20
        if level == 20:

            if self.unlock_title(
                "hub_veteran"
            ):

                rewards.append(
                    "Titre : Hub Veteran"
                )


        return rewards


    # -----------------------------
    # DEBLOCAGES
    # -----------------------------

    def unlock_title(
        self,
        title_id
    ):

        titles = self.stats.data[
            "unlocks"
        ][
            "titles"
        ]

        if title_id in titles:
            return False

        titles.append(
            title_id
        )

        return True


    def unlock_banner(
        self,
        banner_id
    ):

        banners = self.stats.data[
            "unlocks"
        ][
            "banners"
        ]

        if banner_id in banners:
            return False

        banners.append(
            banner_id
        )

        return True


    def unlock_card_back(
        self,
        card_back_id
    ):

        card_backs = self.stats.data[
            "unlocks"
        ][
            "card_backs"
        ]

        if card_back_id in card_backs:
            return False

        card_backs.append(
            card_back_id
        )

        return True