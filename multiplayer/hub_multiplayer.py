from multiplayer.remote_player import RemotePlayer


class HubMultiplayer:

    def __init__(
        self,
        network
    ):

        self.network = network

        self.players = {}


    def update(
        self,
        dt
    ):

        server_players = (
            self.network.hub_players
        )


        visible_ids = set()


        for player_id, data in (
            server_players.items()
        ):

            # Ne dessine jamais
            # notre propre personnage.
            if (
                player_id
                == self.network.client_id
            ):
                continue


            visible_ids.add(
                player_id
            )


            if (
                player_id
                not in self.players
            ):

                self.players[
                    player_id
                ] = RemotePlayer(
                    player_id,
                    data.get(
                        "name",
                        "Player"
                    ),
                    data.get(
                        "character",
                        "pink_girl"
                    ),
                    data.get(
                        "x",
                        640
                    ),
                    data.get(
                        "y",
                        360
                    )
                )


            self.players[
                player_id
            ].set_network_state(
                data
            )


        # Supprime ceux qui ont quitté
        for player_id in list(
            self.players.keys()
        ):

            if (
                player_id
                not in visible_ids
            ):

                self.players.pop(
                    player_id
                )


        for player in (
            self.players.values()
        ):

            player.update(
                dt
            )


    def draw(
        self,
        screen
    ):

        for player in (
            self.players.values()
        ):

            player.draw(
                screen
            )