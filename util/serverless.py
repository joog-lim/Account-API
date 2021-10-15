import json

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://localhost:3000",
    "http://localhost",
    "https://localhost",
    "https://joog-lim.info",
    "https://www.joog-lim.info",
    "https://jooglim.netlify.app",
]

CORS_HEADER = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Credentials": True,
}


def createRes(header, body, statusCode: int = 200):
    header.update(CORS_HEADER)
    return {
        "statusCode": statusCode,
        "headers": header,
        "body": json.dumps(body),
    }


def createErrorRes(header, body, statusCode: int = 401):
    header.update(CORS_HEADER)
    return {
        "statusCode": statusCode,
        "headers": header,
        "body": json.dumps(body),
    }
