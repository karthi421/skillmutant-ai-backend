from fastapi import WebSocket, WebSocketDisconnect
from collections import defaultdict
from typing import Dict

MAX_MEMBERS = 8


class RoomSignalingManager:
    def __init__(self):
        # room_id -> { user_id -> WebSocket }
        self.rooms: Dict[str, Dict[str, WebSocket]] = defaultdict(dict)

    async def connect(self, room_id: str, user_id: str, websocket: WebSocket):
        # 🔒 HARD LIMIT CHECK (FIXES 9/8 BUG)
        if len(self.rooms[room_id]) >= MAX_MEMBERS:
            await websocket.close(code=1008)  # Policy Violation
            return

        await websocket.accept()

        # Register user
        self.rooms[room_id][user_id] = websocket

        # 1️⃣ Send full member list to new user
        await websocket.send_json({
            "type": "init",
            "members": list(self.rooms[room_id].keys())
        })

        # 2️⃣ Notify others user joined
        await self.broadcast(
            room_id,
            {
                "type": "user-joined",
                "user_id": user_id
            },
            exclude=user_id
        )

        # 3️⃣ Broadcast updated count
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

        for uid, ws in self.rooms.get(room_id, {}).items():
            if uid == exclude:
                continue
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
        """
        Relays offer / answer / ice messages to the target user
        """
        target = payload.get("target")
        if not target:
            return

        ws = self.rooms.get(room_id, {}).get(target)
        if ws:
            await ws.send_json({
                **payload,
                "from": sender_id
            })


room_signaling = RoomSignalingManager()
