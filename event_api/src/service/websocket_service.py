from functools import lru_cache

from fastapi import WebSocket, WebSocketDisconnect
from models.notifications import WsMessage


class WebsoketService:
    def __init__(self) -> None:
        self.connected_clients = {}

    async def connection_accept(self, websocket: WebSocket):
        await websocket.accept()

        try:
            while True:
                receive_data = await websocket.receive_json()

                ws_message = WsMessage(**receive_data)
                if ws_message.type == 'client':
                    self.connected_clients[websocket] = ws_message.message['uuid']
                if ws_message.type == 'worker':
                    await self.worker_handler(ws_message.message)
        except WebSocketDisconnect:
            self.connected_clients.pop(websocket, None)

    async def worker_handler(self, message: dict):
        users_ids = message['users_ids']
        receivers = [k for k, v in self.connected_clients.items() if v in users_ids]
        await self.send_notification(message['content_data'], receivers)

    async def send_notification(self, content_data: str, receivers: list[WebSocket]):
        for client in receivers:
            await client.send_text(content_data)


@lru_cache
def get_websoket_service_service() -> WebsoketService:
    return WebsoketService()
