from fastapi import WebSocket, WebSocketDisconnect
from collections import defaultdict
from typing import Dict

MAX_MEMBERS = 8


class RoomSignalingManager:
    def __init__(self):
        # room_id -> { user_id -> WebSocket }
        self.rooms: Dict[str, Dict[str, dict]] = defaultdict(dict)

    async def connect(self, room_id: str, user_id: str, name: str, websocket: WebSocket):
        if len(self.rooms[room_id]) >= MAX_MEMBERS:
            await websocket.close(code=1008)
            return

        await websocket.accept()

        # Store user with name
        self.rooms[room_id][user_id] = {
            "ws": websocket,
            "name": name
        }

        # 1️⃣ Send full member list (with names) to new user
        await websocket.send_json({
            "type": "init",
            "members": [
                {"id": uid, "name": data["name"]}
                for uid, data in self.rooms[room_id].items()
            ]
        })

        # 2️⃣ Notify others
        await self.broadcast(
            room_id,
            {
                "type": "user-joined",
                "user": {
                    "id": user_id,
                    "name": name
                }
            },
            exclude=user_id
        )

        await self.broadcast_count(room_id)

    async def disconnect(self, room_id: str, user_id: str):
        if room_id in self.rooms and user_id in self.rooms[room_id]:
            del self.rooms[room_id][user_id]

            # Notify others user left
            await self.broadcast(
                room_id,
                {
                    "type": "user-left",
                    "user_id": user_id
                }
            )

            await self.broadcast_count(room_id)

            # Cleanup empty room
            if not self.rooms[room_id]:
                del self.rooms[room_id]

    async def broadcast(self, room_id: str, message: dict, exclude: str = None):
        dead_users = []

        for uid, data in self.rooms.get(room_id, {}).items():
            
            if uid == exclude:
                continue
            ws = data["ws"]
            try:
                await ws.send_json(message)
            except Exception:
                dead_users.append(uid)

        # Cleanup dead sockets
        for uid in dead_users:
            del self.rooms[room_id][uid]

    async def broadcast_count(self, room_id: str):
        await self.broadcast(
            room_id,
            {
                "type": "count",
                "members": len(self.rooms.get(room_id, {})),
                "max": MAX_MEMBERS
            }
        )

    # 🔁 PASS-THROUGH SIGNALING (WebRTC ready)
    async def relay(self, room_id: str, sender_id: str, payload: dict):
        target = payload.get("target")
        if not target:
            return

        target_data = self.rooms.get(room_id, {}).get(target)

        if target_data:
            ws = target_data["ws"]
            await ws.send_json({
                **payload,
                "from": sender_id
            })


room_signaling = RoomSignalingManager()
