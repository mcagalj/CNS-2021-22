import uuid
from pathlib import Path
from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Dict, Literal

from Crypto.Random import random

# Important: ws does not work with the prefix set.
# https://github.com/tiangolo/fastapi/issues/98#issuecomment-929047648
router = APIRouter(tags=["WebSocket Chat"])

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / ".." / "templates"))


class Attacks:
    _integrity: Literal[True, False] = False
    _replay: Literal[True, False] = False
    _recorded_data: str = None

    def toggle_integrity(self) -> Literal[True, False]:
        self._integrity = False if self._integrity else True
        return self._integrity

    def _do_integrity(self, data: str) -> str:
        if not self._integrity:
            return data

        data_len = len(data)
        if data_len <= 2:
            return data

        index = random.randint(1, data_len - 1)
        _data = list(data)
        _data[index - 1], _data[index] = _data[index], _data[index - 1]
        return ''.join(_data)

    def toggle_replay(self) -> Literal[True, False]:
        self._replay = False if self._replay else True
        if not self._replay:
            self._recorded_data = None
        return self._replay

    def _do_replay(self, data: str) -> str:
        if not self._recorded_data:
            self._recorded_data = data
            return data

        # Generate an event with odds n in N (n/N)
        n, N = 1, 4
        sample = random.sample("0"*(N-n) + "1"*n, 1)[0]
        if sample == "1":
            return self._recorded_data
        else:
            return data


    def run(self, data):
        if self._integrity:
            return self._do_integrity(data)
        if self._replay:
            return self._do_replay(data)
        return data

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
attacks = Attacks()


@router.get("/ws", response_class=HTMLResponse)
async def message_board(request: Request):
    return templates.TemplateResponse(
        "template.html", {
            "request": request,
            "title": "Public WebSocket Channel",
            "port": 80,
            "client_id": f"attacker_{str(uuid.uuid4())}"
    })


@router.post("/ws/attacks/integrity")
async def toggle_integrity():
    integrity_status = attacks.toggle_integrity()
    return {"status": integrity_status}


@router.post("/ws/attacks/replay")
async def toggle_replay():
    replay_status = attacks.toggle_replay()
    return {"status": replay_status}


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
            data = attacks.run(data)
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast(f"Client #{client_id} left the chat")
