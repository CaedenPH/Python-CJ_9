from __future__ import annotations

import asyncio
from typing import Any, Dict

from aiohttp import (
    ClientConnectionError, ClientSession, ClientWebSocketResponse, WSMsgType
)


class WebsocketHandler:
    """
    Represents a websocket connection.

    Attributes
    ----------
    MESSAGE
        A message has been sent from a client.
    """

    MESSAGE = 0

    def __init__(
        self,
        *,
        websocket: ClientWebSocketResponse,
        session: ClientSession,
        loop: asyncio.AbstractEventLoop,
    ) -> None:
        self.socket = websocket
        self.session = session
        self.loop = loop

    @classmethod
    async def from_client(
        cls, session: ClientSession, loop: asyncio.AbstractEventLoop
    ) -> WebsocketHandler:
        """Handles the websocket connection.

        :param session: The session used to make the websocket connection.
        :param loop: The event loop used to make the websocket connection.
        """
        websocket = await session.ws_connect("http://127.0.0.1:8080/ws")
        self = cls(websocket=websocket, session=session, loop=loop)
        return self

    async def parse(self, data: Dict[Any, Any]):
        """Parses messages from the websocket connection.

        :param data: The data received in dict format.
        """
        print(data)
        await self.socket.send_json(data)

    async def listen(self):
        """Listens to incoming websocket messages."""
        async for message in self.socket:
            if message.type == WSMsgType.TEXT:
                await self.parse(message.data)


async def main():
    """Main function."""
    loop = asyncio.get_event_loop()
    session = ClientSession()

    try:
        websocket = await WebsocketHandler.from_client(session, loop)
        print("Websocket connected")
        while True:
            await websocket.listen()
    except ClientConnectionError:
        print("Websocket disconnected")
        return


if __name__ == "__main__":
    asyncio.run(main())