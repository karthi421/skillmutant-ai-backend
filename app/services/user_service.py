import os
import requests

NODE_BACKEND_URL = os.getenv("MAIN_BACKEND_URL")

if not NODE_BACKEND_URL:
    raise RuntimeError("MAIN_BACKEND_URL is not set")

def fetch_user_profile(token: str):
    response = requests.get(
        f"{NODE_BACKEND_URL}/api/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    if response.status_code != 200:
        return None

    return response.json()