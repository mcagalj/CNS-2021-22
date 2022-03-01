import uuid
from pathlib import Path
from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Dict

# Important: ws does not work with the prefix set.
# https://github.com/tiangolo/fastapi/issues/98#issuecomment-929047648
router = APIRouter(tags=["WebSocket Chat"])

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / ".." / "templates"))

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: int | str):
        await websocket.accept()
        await self.broadcast(f"Client #{client_id} joined the chat")
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: int | str):
        del self.active_connections[client_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for client in self.active_connections:
            await self.active_connections[client].send_text(message)


manager = ConnectionManager()

@router.get("/ws", response_class=HTMLResponse)
async def message_board(request: Request):
    return templates.TemplateResponse(
        "template.html", {
            "request": request,
            "title": "Public WebSocket Channel",
            "port": 80,
            "client_id": f"attacker_{str(uuid.uuid4())}"
    })


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int | str):

    if client_id in manager.active_connections.keys():
        await websocket.accept()
        await manager.send_personal_message(f"Name #{client_id} already taken. Please try to reconnect with another name.", websocket)
        await websocket.close()
        return

    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast(f"Client #{client_id} left the chat")
