from typing import Dict, Set
from uuid import uuid4

MAX_MEMBERS = 8

class RoomManager:
    def __init__(self):
        # room_id -> set(user_id)
        self.rooms: Dict[str, Set[str]] = {}

    def create_room(self) -> str:
        room_id = uuid4().hex[:6].upper()
        self.rooms[room_id] = set()
        return room_id

    def join_room(self, room_id: str, user_id: str) -> Dict:
        if room_id not in self.rooms:
            raise ValueError("Room does not exist")

        if len(self.rooms[room_id]) >= MAX_MEMBERS:
            raise ValueError("Room is full")

        self.rooms[room_id].add(user_id)

        return self.get_room_info(room_id)

    def leave_room(self, room_id: str, user_id: str):
        if room_id in self.rooms:
            self.rooms[room_id].discard(user_id)

            # cleanup empty room
            if not self.rooms[room_id]:
                del self.rooms[room_id]

    def get_room_info(self, room_id: str) -> Dict:
        if room_id not in self.rooms:
            raise ValueError("Room does not exist")

        return {
            "room_id": room_id,
            "members": len(self.rooms[room_id]),
            "max_members": MAX_MEMBERS,
            "users": list(self.rooms[room_id]),
        }


room_manager = RoomManager()
