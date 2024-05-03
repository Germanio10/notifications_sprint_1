from fastapi import APIRouter, Depends, WebSocket
from service.websocket_service import WebsoketService, get_websoket_service_service

ws_router = APIRouter()

connected_clients = {}


async def send_notification(message):
    for client in connected_clients:
        await client.send_text(message)


@ws_router.websocket("/notifications")
async def websocket_endpoint(
    websocket: WebSocket,
    ws_service: WebsoketService = Depends(get_websoket_service_service),
):
    await ws_service.connection_accept(websocket=websocket)
