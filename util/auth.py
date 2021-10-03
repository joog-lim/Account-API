import os

from typing import Any

from google.oauth2 import id_token
from google.auth.transport import requests

CLIENT_ID_WEB: str = os.environ["CLIENT_ID_WEB"]
CLIENT_ID_ANDROID: str = os.environ["CLIENT_ID_ANDROID"]
CLIENT_ID_IOS: str = os.environ["CLIENT_ID_IOS"]


def auth_by_google_token(token: str) -> dict[str, Any]:
    try:
        info = id_token.verify_oauth2_token(token, requests.Request())

        if info["aud"] not in [CLIENT_ID_WEB, CLIENT_ID_ANDROID, CLIENT_ID_IOS]:
            return {"error": "Invaild Client Id"}
    except ValueError:
        return {"error": "Invaild Token"}
    return info
