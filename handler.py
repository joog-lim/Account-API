from util.auth import auth_by_google_token
from util.serverless import createRes, createErrorRes


def hello(_, __):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": _,
    }

    return createRes(header={"Content-Type": "application/json"}, body=body)


def login(event, __):
    sub: str = auth_by_google_token(event.headers.Authorization).get("sub")

    if sub is None:
        return createErrorRes(
            header={"Content-Type": "application/json"}, message="값이 뭔가 이상합니다."
        )

    return createRes(header={}, body={"message": "무야호"})
