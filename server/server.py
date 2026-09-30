import asyncio
import json
import uuid
import os
from websockets.asyncio.server import serve
from server.uno_room import UnoRoom
from server.rooms import RoomManager


HOST = "0.0.0.0"
PORT = int(
    os.environ.get(
        "PORT",
        8765
    )
)


rooms = RoomManager()
uno_games = {}
clients = {}

player_names = {}
player_characters = {}
hub_players = {}
# ---------------------------------
# ENVOI JSON
# ---------------------------------
async def broadcast_hub_state():

    players = []

    for player_id, data in hub_players.items():

        players.append(
            {
                "id": player_id,

                "name": player_names.get(
                    player_id,
                    "Player"
                ),

                "character": player_characters.get(
                    player_id,
                    "lucie"
                ),

                "x": data["x"],
                "y": data["y"],

                "direction": data[
                    "direction"
                ],

                "state": data[
                    "state"
                ]
            }
        )


    message = json.dumps(
        {
            "type": "hub_state",
            "players": players
        }
    )


    disconnected = []


    for player_id in list(
        hub_players.keys()
    ):

        websocket = clients.get(
            player_id
        )

        if websocket is None:
            continue

        try:

            await websocket.send(
                message
            )

        except Exception:

            disconnected.append(
                player_id
            )


    for player_id in disconnected:

        hub_players.pop(
            player_id,
            None
        )

async def send_json(
    websocket,
    data
):

    await websocket.send(
        json.dumps(
            data
        )
    )


# ---------------------------------
# BROADCAST ROOM
# ---------------------------------

async def broadcast_room(
    room
):

    if room is None:
        return

    message = json.dumps(
        {
            "type": "room_state",
            "room": room.serialize()
        }
    )

    disconnected = []

    for player_id in list(
        room.players.keys()
    ):

        websocket = clients.get(
            player_id
        )

        if websocket is None:
            continue

        try:

            await websocket.send(
                message
            )

        except Exception:

            disconnected.append(
                player_id
            )

    for player_id in disconnected:

        rooms.leave_room(
            player_id
        )


# ---------------------------------
# CLIENT
# ---------------------------------

async def handle_client(
    websocket
):

    player_id = (
        uuid.uuid4().hex[:12]
    )

    clients[player_id] = websocket

    player_names[player_id] = (
        "Player"
    )
    player_characters[player_id] = "lucie"
    print(
        f"[+] Connexion : {player_id}"
    )

    await send_json(
        websocket,
        {
            "type": "welcome",
            "client_id": player_id
        }
    )

    try:

        async for raw_message in websocket:

            try:

                data = json.loads(
                    raw_message
                )

            except json.JSONDecodeError:

                continue

            message_type = data.get(
                "type"
            )

            # -------------------------
            # HELLO
            # -------------------------

            if message_type == "hello":
                character = str(
                    data.get(
                        "character",
                        "lucie"
                    )
                ).strip()

                if not character:
                    character = "lucie"

                player_characters[
                    player_id
                ] = character
                name = (
                    str(
                        data.get(
                            "name",
                            "Player"
                        )
                    )
                    .strip()
                )

                if not name:
                    name = "Player"

                player_names[
                    player_id
                ] = name[:20]

                print(
                    f"{player_id} = {name}"
                )
            elif message_type == "hub_leave":

                hub_players.pop(
                    player_id,
                    None
                )

                await broadcast_hub_state()
            elif message_type == "hub_move":

                player = hub_players.get(
                    player_id
                )

                if player is None:
                    continue


                try:

                    x = float(
                        data.get(
                            "x",
                            player["x"]
                        )
                    )

                    y = float(
                        data.get(
                            "y",
                            player["y"]
                        )
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    continue


                direction = data.get(
                    "direction",
                    "down"
                )

                movement_state = data.get(
                    "state",
                    "idle"
                )


                if direction not in [
                    "up",
                    "down",
                    "left",
                    "right"
                ]:

                    direction = "down"


                if movement_state not in [
                    "idle",
                    "walk",
                    "run"
                ]:

                    movement_state = "idle"


                player["x"] = max(
                    0,
                    min(
                        1280,
                        x
                    )
                )

                player["y"] = max(
                    0,
                    min(
                        720,
                        y
                    )
                )

                player["direction"] = (
                    direction
                )

                player["state"] = (
                    movement_state
                )


                await broadcast_hub_state()
            elif message_type == "hub_enter":

                try:

                    x = float(
                        data.get(
                            "x",
                            640
                        )
                    )

                    y = float(
                        data.get(
                            "y",
                            360
                        )
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    x = 640
                    y = 360


                hub_players[
                    player_id
                ] = {
                    "x": max(
                        0,
                        min(
                            1280,
                            x
                        )
                    ),

                    "y": max(
                        0,
                        min(
                            720,
                            y
                        )
                    ),

                    "direction": "down",

                    "state": "idle"
                }


                print(
                    f"[HUB] {player_names[player_id]} entre dans le hub"
                )


                await broadcast_hub_state()
            # -------------------------
            # CREATE ROOM
            
            # -------------------------
            elif message_type == "uno_return_lobby":

                room = rooms.get_player_room(
                    player_id
                )

                if room is None:
                    continue


                uno_game = uno_games.get(
                    room.code
                )

                if uno_game is None:
                    continue


                # On autorise seulement après
                # la fin de partie
                if uno_game.winner_id is None:

                    await send_json(
                        websocket,
                        {
                            "type": "error",
                            "message":
                                "La partie n'est pas terminée."
                        }
                    )

                    continue


                uno_games.pop(
                    room.code,
                    None
                )


                print(
                    f"[UNO] Retour lobby {room.code}"
                )


                for target_id in room.players:

                    target_socket = clients.get(
                        target_id
                    )

                    if target_socket is None:
                        continue


                    await send_json(
                        target_socket,
                        {
                            "type": "game_ended",
                            "game": "uno"
                        }
                    )
            elif message_type == "uno_replay_vote":

                room = rooms.get_player_room(
                    player_id
                )

                if room is None:
                    continue


                uno_game = uno_games.get(
                    room.code
                )

                if uno_game is None:
                    continue


                try:

                    uno_game.vote_replay(
                        player_id
                    )

                except ValueError as error:

                    await send_json(
                        websocket,
                        {
                            "type": "error",
                            "message": str(
                                error
                            )
                        }
                    )

                    continue


                # ---------------------------------
                # LES DEUX VEULENT REJOUER
                # ---------------------------------

                if uno_game.everyone_wants_replay():

                    print(
                        f"[UNO] Replay dans {room.code}"
                    )


                    new_game = UnoRoom(
                        room
                    )


                    uno_games[
                        room.code
                    ] = new_game


                    # On dit aux clients
                    # qu'une nouvelle partie commence
                    for target_id in room.players:

                        target_socket = clients.get(
                            target_id
                        )

                        if target_socket is None:
                            continue


                        await send_json(
                            target_socket,
                            {
                                "type": "uno_restarted"
                            }
                        )


                    await broadcast_uno_state(
                        room,
                        new_game
                    )


                else:

                    # Actualise juste les votes
                    await broadcast_uno_state(
                        room,
                        uno_game
                    )
            elif message_type == "start_uno":

                room = rooms.get_player_room(
                    player_id
                )

                if room is None:

                    await send_json(
                        websocket,
                        {
                            "type": "error",
                            "message": "Tu n'es dans aucune room."
                        }
                    )

                    continue


                # Seul l'hôte peut lancer
                if room.host_id != player_id:

                    await send_json(
                        websocket,
                        {
                            "type": "error",
                            "message": "Seul l'hôte peut lancer la partie."
                        }
                    )

                    continue


                # Pour notre V1 :
                # exactement 2 joueurs
                if len(room.players) != 2:

                    await send_json(
                        websocket,
                        {
                            "type": "error",
                            "message": "UNO nécessite 2 joueurs pour le moment."
                        }
                    )

                    continue


                # Evite de lancer deux parties
                if room.code in uno_games:

                    await send_json(
                        websocket,
                        {
                            "type": "error",
                            "message": "Une partie est déjà lancée."
                        }
                    )

                    continue


                uno_game = UnoRoom(
                    room
                )

                uno_games[
                    room.code
                ] = uno_game


                print(
                    f"[UNO] Partie créée dans {room.code}"
                )


                # Dit aux deux clients
                # de changer d'écran
                for target_id in room.players:

                    target_socket = clients.get(
                        target_id
                    )

                    if target_socket is None:
                        continue

                    await send_json(
                        target_socket,
                        {
                            "type": "game_started",
                            "game": "uno"
                        }
                    )


                # Puis envoie leur état personnalisé
                await broadcast_uno_state(
                    room,
                    uno_game
                )
            elif message_type == "create_room":

                old_room = (
                    rooms.get_player_room(
                        player_id
                    )
                )

                if old_room:

                    rooms.leave_room(
                        player_id
                    )

                    await broadcast_room(
                        old_room
                    )

                room = rooms.create_room(
                    player_id,
                    player_names[player_id],
                    player_characters[player_id]
                )

                print(
                    f"[ROOM] {player_id} "
                    f"crée {room.code}"
                )

                await broadcast_room(
                    room
                )

            # -------------------------
            # JOIN ROOM
            # -------------------------

            elif message_type == "join_room":

                code = str(
                    data.get(
                        "code",
                        ""
                    )
                ).upper().strip()

                old_room = (
                    rooms.get_player_room(
                        player_id
                    )
                )

                try:

                    room = rooms.join_room(
                        player_id,
                        player_names[player_id],
                        code,
                        player_characters[player_id]
                    )

                except ValueError as error:

                    await send_json(
                        websocket,
                        {
                            "type": "error",
                            "message": str(
                                error
                            )
                        }
                    )

                    continue

                if (
                    old_room
                    and old_room.code
                    != room.code
                ):

                    await broadcast_room(
                        old_room
                    )

                print(
                    f"[ROOM] {player_id} "
                    f"rejoint {room.code}"
                )

                await broadcast_room(
                    room
                )

            # -------------------------
            # LEAVE ROOM
            # -------------------------
            elif message_type == "uno_play_card":

                room = rooms.get_player_room(
                    player_id
                )

                if room is None:

                    await send_json(
                        websocket,
                        {
                            "type": "error",
                            "message": "Room introuvable."
                        }
                    )

                    continue


                uno_game = uno_games.get(
                    room.code
                )

                if uno_game is None:

                    await send_json(
                        websocket,
                        {
                            "type": "error",
                            "message": "Aucune partie UNO."
                        }
                    )

                    continue


                try:

                    hand_index = int(
                        data.get(
                            "hand_index"
                        )
                    )

                    chosen_color = (
                        data.get(
                            "chosen_color"
                        )
                    )


                    uno_game.play_card(
                        player_id,
                        hand_index,
                        chosen_color
                    )


                except (
                    ValueError,
                    TypeError
                ) as error:

                    await send_json(
                        websocket,
                        {
                            "type": "error",
                            "message": str(
                                error
                            )
                        }
                    )

                    continue


                await broadcast_uno_state(
                    room,
                    uno_game
                )
            elif message_type == "uno_draw_card":

                room = rooms.get_player_room(
                    player_id
                )

                if room is None:
                    continue


                uno_game = uno_games.get(
                    room.code
                )

                if uno_game is None:
                    continue


                try:

                    uno_game.draw_card(
                        player_id
                    )

                except ValueError as error:

                    await send_json(
                        websocket,
                        {
                            "type": "error",
                            "message": str(
                                error
                            )
                        }
                    )

                    continue


                await broadcast_uno_state(
                    room,
                    uno_game
                )
            elif message_type == "leave_room":

                room = rooms.get_player_room(
                    player_id
                )

                old_code = (
                    room.code
                    if room
                    else None
                )

                rooms.leave_room(
                    player_id
                )

                await send_json(
                    websocket,
                    {
                        "type": "room_left"
                    }
                )

                await broadcast_room(
                    room
                )

                if (
                    old_code
                    and old_code in uno_games
                ):

                    uno_games.pop(
                        old_code,
                        None
                    )
    except Exception as error:

        print(
            "[ERREUR CLIENT]",
            error
        )

    finally:

        room = (
            rooms.get_player_room(
                player_id
            )
        )

        rooms.leave_room(
            player_id
        )
        hub_players.pop(
            player_id,
            None
        )
        clients.pop(
            player_id,
            None
        )

        player_names.pop(
            player_id,
            None
        )
        player_characters.pop(
            player_id,
            None
        )
        print(
            f"[-] Déconnexion : {player_id}"
        )

        await broadcast_room(
            room
        )
        await broadcast_hub_state()

# ---------------------------------
# MAIN
# ---------------------------------

async def main():

    print(
        "=============================="
    )

    print(
        " HUB MULTIPLAYER SERVER"
    )

    print(
        f" ws://127.0.0.1:{PORT}"
    )

    print(
        "=============================="
    )

    async with serve(
        handle_client,
        HOST,
        PORT
    ):

        await asyncio.Future()


async def broadcast_uno_state(
    room,
    uno_game
):

    if room is None:
        return

    for player_id in list(
        room.players.keys()
    ):

        websocket = clients.get(
            player_id
        )

        if websocket is None:
            continue

        state = uno_game.serialize_for(
            player_id,
            room
        )

        try:

            await send_json(
                websocket,
                {
                    "type": "uno_state",
                    "state": state
                }
            )

        except Exception as error:

            print(
                "[UNO SEND ERROR]",
                error
            )


if __name__ == "__main__":

    asyncio.run(
        main()
    )