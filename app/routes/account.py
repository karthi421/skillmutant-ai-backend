from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/account", tags=["Account"])


@router.get("/me")
def get_my_account(user=Depends(get_current_user)):
    """
    user comes DIRECTLY from JWT payload created in Node backend
    """
    return {
        "id": user.get("id"),
        "email": user.get("email"),
        "username": user.get("username"),
        "name": user.get("name"),
        "college": user.get("college"),
        "bio": user.get("bio"),
        "profile_pic": user.get("profile_pic"),
    }

