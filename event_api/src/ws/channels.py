from fastapi import APIRouter, Depends, WebSocket
from models.user import User
from service.websocket_service import WebsoketService, get_websoket_service_service
from utils.check_auth import CheckAuth

ws_router = APIRouter()

connected_clients = {}


async def send_notification(message):
    for client in connected_clients:
        await client.send_text(message)


@ws_router.websocket("/notifications")
async def websocket_endpoint(
    websocket: WebSocket,
    ws_service: WebsoketService = Depends(get_websoket_service_service),
    user: User = Depends(CheckAuth()),
):
    await ws_service.connection_accept(websocket=websocket, user_id=user.user_id)
