import secrets
import string

from dataclasses import dataclass, field


ROOM_CHARACTERS = (
    string.ascii_uppercase
    + string.digits
)

# On retire les caractères ambigus
ROOM_CHARACTERS = (
    ROOM_CHARACTERS
    .replace("0", "")
    .replace("O", "")
    .replace("1", "")
    .replace("I", "")
)


@dataclass
class Room:
    code: str

    host_id: str

    players: dict = field(
        default_factory=dict
    )

    def serialize(self):
        
        player_list = []

        for player_id, data in self.players.items():

            player_list.append(
                {
                    "id": player_id,
                    "name": data["name"],
                    "host": (
                        player_id
                        == self.host_id
                    ),
                    "character": data.get(
                        "character",
                        "lucie"
                    ),
                }
            )

        return {
            "code": self.code,
            "host_id": self.host_id,
            "players": player_list
        }


class RoomManager:

    def __init__(self):

        self.rooms = {}

        self.player_rooms = {}

    # ---------------------------------
    # CODE DE ROOM
    # ---------------------------------

    def generate_code(self):

        while True:

            code = "".join(
                secrets.choice(
                    ROOM_CHARACTERS
                )
                for _ in range(6)
            )

            if code not in self.rooms:
                return code

    # ---------------------------------
    # CREER
    # ---------------------------------

    def create_room(
        self,
        player_id,
        player_name,
        player_character="lucie"
    ):

        self.leave_room(
            player_id
        )

        code = self.generate_code()

        room = Room(
            code=code,
            host_id=player_id
        )

        room.players[player_id] = {
            "name": player_name,
            "character": player_character
        }

        self.rooms[code] = room

        self.player_rooms[
            player_id
        ] = code

        return room

    # ---------------------------------
    # REJOINDRE
    # ---------------------------------

    def join_room(
        self,
        player_id,
        player_name,
        code,
        player_character="lucie"
    ):

        code = code.upper()

        room = self.rooms.get(
            code
        )

        if room is None:

            raise ValueError(
                "Room introuvable."
            )

        # V1 : maximum 4 joueurs
        if len(room.players) >= 4:

            raise ValueError(
                "La room est pleine."
            )

        self.leave_room(
            player_id
        )

        room.players[player_id] = {
            "name": player_name,
            "character": player_character
        }

        self.player_rooms[
            player_id
        ] = code

        return room

    # ---------------------------------
    # QUITTER
    # ---------------------------------

    def leave_room(
        self,
        player_id
    ):

        code = self.player_rooms.pop(
            player_id,
            None
        )

        if code is None:
            return None

        room = self.rooms.get(
            code
        )

        if room is None:
            return None

        room.players.pop(
            player_id,
            None
        )

        # Room vide
        if not room.players:

            self.rooms.pop(
                code,
                None
            )

            return None

        # Si l'hôte quitte,
        # le prochain joueur devient hôte.
        if room.host_id == player_id:

            room.host_id = next(
                iter(
                    room.players
                )
            )

        return room

    # ---------------------------------
    # ROOM DU JOUEUR
    # ---------------------------------

    def get_player_room(
        self,
        player_id
    ):

        code = self.player_rooms.get(
            player_id
        )

        if code is None:
            return None

        return self.rooms.get(
            code
        )