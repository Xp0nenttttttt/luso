import asyncio
import json
import threading
import queue

from websockets.asyncio.client import connect


class NetworkClient:

    def __init__(
        self,
        url,
        player_name
    ):

        self.url = url

        self.player_name = (
            player_name
        )

        self.connected = False

        self.client_id = None

        self.room = None

        self.last_error = None

        self._thread = None

        self._loop = None

        self._websocket = None

        self._outgoing = None

        self._incoming = (
            queue.Queue()
        )

        self._running = False

    # ---------------------------------
    # START
    # ---------------------------------

    def start(self):

        if self._running:
            return

        self._running = True

        self._thread = threading.Thread(
            target=self._thread_main,
            daemon=True
        )

        self._thread.start()

    def _thread_main(self):

        asyncio.run(
            self._network_main()
        )

    # ---------------------------------
    # NETWORK LOOP
    # ---------------------------------

    async def _network_main(self):

        self._loop = (
            asyncio.get_running_loop()
        )

        self._outgoing = (
            asyncio.Queue()
        )

        try:

            async with connect(
                self.url,
                ping_interval=20,
                ping_timeout=20
            ) as websocket:

                self._websocket = (
                    websocket
                )

                self._incoming.put(
                    {
                        "_local":
                        "connected"
                    }
                )

                # Présentation au serveur
                await websocket.send(
                    json.dumps(
                        {
                            "type": "hello",
                            "name":
                            self.player_name
                        }
                    )
                )

                sender_task = (
                    asyncio.create_task(
                        self._sender_loop(
                            websocket
                        )
                    )
                )

                try:

                    async for raw in websocket:

                        try:

                            message = (
                                json.loads(
                                    raw
                                )
                            )

                            self._incoming.put(
                                message
                            )

                        except json.JSONDecodeError:

                            pass

                finally:

                    sender_task.cancel()

        except Exception as error:

            self._incoming.put(
                {
                    "_local":
                    "connection_error",

                    "message":
                    str(error)
                }
            )

        finally:

            self._websocket = None

            self._incoming.put(
                {
                    "_local":
                    "disconnected"
                }
            )

    # ---------------------------------
    # SEND LOOP
    # ---------------------------------

    async def _sender_loop(
        self,
        websocket
    ):

        while True:

            message = (
                await self._outgoing.get()
            )

            if message is None:

                await websocket.close()

                return

            await websocket.send(
                json.dumps(
                    message
                )
            )

    # ---------------------------------
    # SEND
    # ---------------------------------

    def send(
        self,
        message
    ):

        if (
            self._loop is None
            or self._outgoing is None
            or self._loop.is_closed()
        ):
            return

        try:
            self._loop.call_soon_threadsafe(
                self._outgoing.put_nowait,
                message
            )
        except RuntimeError:
            pass

    # ---------------------------------
    # ACTIONS
    # ---------------------------------

    def create_room(self):

        self.last_error = None

        self.send(
            {
                "type": "create_room"
            }
        )

    def join_room(
        self,
        code
    ):

        self.last_error = None

        self.send(
            {
                "type": "join_room",
                "code": (
                    code
                    .upper()
                    .strip()
                )
            }
        )

    def leave_room(self):

        self.send(
            {
                "type": "leave_room"
            }
        )

    # ---------------------------------
    # UPDATE COTE PYGAME
    # ---------------------------------

    def update(self):

        events = []

        while True:

            try:

                message = (
                    self._incoming
                    .get_nowait()
                )

            except queue.Empty:

                break

            local_type = (
                message.get(
                    "_local"
                )
            )

            if (
                local_type
                == "connected"
            ):

                self.connected = True

                self.last_error = None

            elif (
                local_type
                == "disconnected"
            ):

                self.connected = False

                self.room = None

            elif (
                local_type
                == "connection_error"
            ):

                self.connected = False

                self.last_error = (
                    message.get(
                        "message"
                    )
                )

            else:

                message_type = (
                    message.get(
                        "type"
                    )
                )

                if (
                    message_type
                    == "welcome"
                ):

                    self.client_id = (
                        message[
                            "client_id"
                        ]
                    )

                elif (
                    message_type
                    == "room_state"
                ):

                    self.room = (
                        message[
                            "room"
                        ]
                    )

                elif (
                    message_type
                    == "room_left"
                ):

                    self.room = None

                elif (
                    message_type
                    == "error"
                ):

                    self.last_error = (
                        message.get(
                            "message"
                        )
                    )

                events.append(
                    message
                )

        return events

    # ---------------------------------
    # STOP
    # ---------------------------------

    def stop(self):

        self._running = False

        if (
            self._loop is not None
            and self._outgoing
            is not None
            and not self._loop.is_closed()
        ):

            try:
                self._loop.call_soon_threadsafe(
                    self._outgoing.put_nowait,
                    None
                )
            except RuntimeError:
                pass