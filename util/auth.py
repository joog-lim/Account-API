import os

from typing import Any

from google.oauth2 import id_token
from google.auth.transport import requests

CLIENT_ID : str = os.environ["CLIENT_ID"]

def auth_by_google_token(token: str) -> dict[str, Any]:
    try:
        info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
    except ValueError:
        return {"error": "Invalid Token"}
    return info