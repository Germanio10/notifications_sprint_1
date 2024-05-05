from functools import lru_cache

from fastapi import WebSocket, WebSocketDisconnect
from models.notifications import WsMessage


class WebsoketService:
    def __init__(self) -> None:
        self.connected_clients = {}

    async def connection_accept(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        try:
            while True:
                receive_data = await websocket.receive_json()

                ws_message = WsMessage(**receive_data)
                if ws_message.type == 'client':
                    self.connected_clients[user_id] = websocket
                if ws_message.type == 'worker':
                    await self.worker_handler(ws_message.message)
        except WebSocketDisconnect:
            self.connected_clients.pop(user_id, None)

    async def worker_handler(self, message: dict):
        users_ids = message['users_ids']

        for user_id in users_ids:
            client: WebSocket = self.connected_clients.get(user_id)
            await client.send_text(message['content_data'])


@lru_cache
def get_websoket_service_service() -> WebsoketService:
    return WebsoketService()
