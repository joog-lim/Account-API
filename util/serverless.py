import json
from typing import Any

ALLOWED_ORIGINS: list[str] = [
    "http://localhost:3000",
    "https://localhost:3000",
    "http://localhost",
    "https://localhost",
    "https://joog-lim.info",
    "https://www.joog-lim.info",
    "https://jooglim.netlify.app",
]

CORS_HEADER: dict[str, Any] = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Credentials": True,
}


def createRes(header: dict[str, Any], body: dict[str, Any], statusCode: int = 200):
    return {"statusCode": statusCode, "headers": header, "body": json.dumps(body)}


def createErrorRes(header: dict[str, Any], body: dict[str, Any], statusCode: int = 401):
    return {"statusCode": statusCode, "headers": header, "body": json.dumps(body)}
