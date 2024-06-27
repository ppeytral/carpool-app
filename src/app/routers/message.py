import json
from dataclasses import dataclass
from datetime import datetime

import sqlalchemy as sa
from config.database import get_session
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from models.message import Message
from models.school import School
from models.student import Student
from schemas.message import MessageOut
from sqlalchemy.orm import joinedload

message_router = APIRouter(
    prefix="/message",
    tags=["Message"],
)


@dataclass
class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict = {}

    async def connect(self, websocket: WebSocket, id: int):
        await websocket.accept()
        self.active_connections[id] = websocket
        connection_message = {
            "sender": 0,
            "destination": id,
            "message": "Connected",
        }
        await websocket.send_text(json.dumps(connection_message))

    def disconnect(self, websocket: WebSocket):
        id = self.find_connection_id(websocket)
        del self.active_connections[id]
        return id

    def find_connection_id(self, websocket: WebSocket):
        val_list = list(self.active_connections.values())
        key_list = list(self.active_connections.keys())
        id = val_list.index(websocket)
        return key_list[id]

    async def send_message_to(self, id: int, message: str):
        ws = self.active_connections[id]
        await ws.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)


connection_manager = ConnectionManager()


@message_router.websocket("/{sender_id}")
async def websocket_endpoint(websocket: WebSocket, sender_id: int):
    await connection_manager.connect(websocket=websocket, id=sender_id)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)

            json_data = json.loads(data)
            sender = json_data["sender"]
            dest = json_data["destination"]
            message = json_data["message"]
            with get_session() as s:
                stmt = sa.insert(Message).values(
                    sender_id=sender,
                    recipient_id=dest,
                    message=message,
                    created_at=datetime.now(),
                )
                s.execute(stmt)
                s.commit()

            await connection_manager.send_message_to(sender, data)
            if dest in connection_manager.active_connections:
                await connection_manager.send_message_to(dest, data)
    except WebSocketDisconnect:
        id = connection_manager.disconnect(websocket)
        await connection_manager.broadcast(
            json.dumps({"type": "disconnected", "id": id})
        )
    except KeyError:
        print("recipient not connected")


@message_router.get(
    "/sender/{sender_id}/recipient/{recipient_id}",
    summary="Get all messages for a conversation",
    # response_model=list[MessageOut],
)
def get_conversation(sender_id: int, recipient_id: int):
    with get_session() as s:
        stmt = (
            sa.select(Message)
            .options(joinedload(Message.sender).joinedload(Student.address))
            .options(
                joinedload(Message.sender)
                .joinedload(Student.school)
                .joinedload(School.address)
            )
            .options(joinedload(Message.recipient))
            .where(
                sa.or_(
                    sa.and_(
                        Message.recipient_id == sender_id,
                        Message.sender_id == recipient_id,
                    ),
                    sa.and_(
                        Message.recipient_id == recipient_id,
                        Message.sender_id == sender_id,
                    ),
                )
            )
            .order_by(Message.created_at)
        )

        res = s.scalars(stmt).all()
        return res
