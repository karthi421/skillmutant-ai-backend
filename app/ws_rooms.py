'''
from fastapi import WebSocket, WebSocketDisconnect
from collections import defaultdict
from typing import Dict

MAX_MEMBERS = 8


class RoomSignalingManager:
    def __init__(self):
        # room_id -> { user_id -> WebSocket }
        self.rooms: Dict[str, Dict[str, dict]] = defaultdict(dict)

    async def connect(self, room_id: str, user: dict, websocket: WebSocket):
        if len(self.rooms[room_id]) >= MAX_MEMBERS:
            await websocket.close(code=1008)
            return

        await websocket.accept()

        user_id = str(user.get("id"))

        profile = {
            "id": user.get("id"),
            "name": user.get("name"),
            "profile_pic": user.get("profile_pic")
        }

    # Store websocket + profile
        self.rooms[room_id][user_id] = {
            "ws": websocket,
            "profile": profile
        }

    # 1️⃣ Send full member list (with profiles)
        await websocket.send_json({
            "type": "init",
            "members": [
                member["profile"]
                for member in self.rooms[room_id].values()
            ]
        })

    # 2️⃣ Notify others user joined (with profile)
        await self.broadcast(
            room_id,
            {
                "type": "user-joined",
                "user": profile
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
        """
        Relays offer / answer / ice messages to the target user
        """
        target = payload.get("target")
        if not target:
            return

        target_data = self.rooms.get(room_id, {}).get(target)
        if target_data:
            await target_data["ws"].send_json({
            **payload,
            "from": sender_id
        })
       

room_signaling = RoomSignalingManager()
'''

from fastapi import WebSocket
from collections import defaultdict
from typing import Dict

MAX_MEMBERS = 8


class RoomSignalingManager:
    def __init__(self):
        # room_id -> { user_id -> {"ws": WebSocket, "profile": {...}} }
        self.rooms: Dict[str, Dict[str, dict]] = defaultdict(dict)

    async def connect(self, room_id: str, user: dict, websocket: WebSocket):

        if len(self.rooms[room_id]) >= MAX_MEMBERS:
            await websocket.close(code=1008)
            return

        await websocket.accept()

        user_id = str(user.get("id"))

        profile = {
            "id": user.get("id"),
            "name": user.get("name"),
            "profile_pic": user.get("profile_pic")
        }

        # Store websocket + profile
        self.rooms[room_id][user_id] = {
            "ws": websocket,
            "profile": profile
        }

        # Send full member list (profiles)
        await websocket.send_json({
            "type": "init",
            "members": [
                member["profile"]
                for member in self.rooms[room_id].values()
            ]
        })

        # Notify others user joined
        await self.broadcast(
            room_id,
            {
                "type": "user-joined",
                "user": profile
            },
            exclude=user_id
        )

        await self.broadcast_count(room_id)

    async def disconnect(self, room_id: str, user_id: str):

        if room_id in self.rooms and user_id in self.rooms[room_id]:

            del self.rooms[room_id][user_id]

            await self.broadcast(
                room_id,
                {
                    "type": "user-left",
                    "user_id": user_id
                }
            )

            await self.broadcast_count(room_id)

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

    async def relay(self, room_id: str, sender_id: str, payload: dict):

        target = payload.get("target")
        if not target:
            return

        target_data = self.rooms.get(room_id, {}).get(str(target))

        if target_data:
            await target_data["ws"].send_json({
                **payload,
                "from": sender_id
            })
room_signaling = RoomSignalingManager()
