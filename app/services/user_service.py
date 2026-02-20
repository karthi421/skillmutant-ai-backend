import requests

NODE_BACKEND_URL = "http://localhost:5000"

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
