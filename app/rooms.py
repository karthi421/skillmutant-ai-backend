# app/rooms.py
from fastapi import APIRouter, HTTPException
from app.room_manager import room_manager

router = APIRouter(prefix="/rooms", tags=["Collaborative Rooms"])

@router.post("/create")
def create_room():
    room_id = room_manager.create_room()
    return {
        "room_id": room_id,
        "max_members": 8
    }

@router.post("/join")
def join_room(data: dict):
    room_id = data.get("room_id")
    user_id = data.get("user_id")

    if not room_id or not user_id:
        raise HTTPException(status_code=400, detail="room_id and user_id required")

    try:
        room_manager.join_room(room_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return room_manager.get_room_info(room_id)

@router.post("/leave")
def leave_room(data: dict):
    room_id = data.get("room_id")
    user_id = data.get("user_id")

    if not room_id or not user_id:
        raise HTTPException(status_code=400, detail="room_id and user_id required")

    room_manager.leave_room(room_id, user_id)
    return { "status": "left" }

@router.get("/{room_id}")
def room_info(room_id: str):
    try:
        return room_manager.get_room_info(room_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
