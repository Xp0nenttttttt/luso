import asyncio
import json
import uuid

from websockets.asyncio.server import serve

from server.rooms import RoomManager


HOST = "0.0.0.0"
PORT = 8765


rooms = RoomManager()

clients = {}

player_names = {}


# ---------------------------------
# ENVOI JSON
# ---------------------------------

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

            # -------------------------
            # CREATE ROOM
            # -------------------------

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
                    player_names[player_id]
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
                        code
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

            elif message_type == "leave_room":

                room = (
                    rooms.get_player_room(
                        player_id
                    )
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

        clients.pop(
            player_id,
            None
        )

        player_names.pop(
            player_id,
            None
        )

        print(
            f"[-] Déconnexion : {player_id}"
        )

        await broadcast_room(
            room
        )


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


if __name__ == "__main__":

    asyncio.run(
        main()
    )