from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Dict, List
import uuid

app = FastAPI(title="Distributed Secure Messaging API", version="0.1.0")


class Message(BaseModel):
    id: str
    sender: str
    recipient: str
    body: str
    created_at: datetime


class CreateMessage(BaseModel):
    sender: str
    recipient: str
    body: str


messages: List[Message] = []


class ConnectionManager:
    def __init__(self) -> None:
        self.connections: Dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections[user_id] = websocket

    def disconnect(self, user_id: str) -> None:
        self.connections.pop(user_id, None)

    async def deliver(self, user_id: str, payload: dict) -> bool:
        websocket = self.connections.get(user_id)
        if websocket is None:
            return False
        await websocket.send_json(payload)
        return True


manager = ConnectionManager()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "active_connections": len(manager.connections)}


@app.post("/api/v1/messages", response_model=Message)
async def create_message(request: CreateMessage) -> Message:
    message = Message(
        id=str(uuid.uuid4()),
        sender=request.sender,
        recipient=request.recipient,
        body=request.body,
        created_at=datetime.now(timezone.utc),
    )
    messages.append(message)
    await manager.deliver(request.recipient, {"type": "message", "data": message.model_dump(mode="json")})
    return message


@app.get("/api/v1/messages/{user_id}", response_model=List[Message])
def get_messages(user_id: str) -> List[Message]:
    return [m for m in messages if m.sender == user_id or m.recipient == user_id]


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str) -> None:
    await manager.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id)
