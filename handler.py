from typing import Any
from account.model.token import TokenModel
from account.model.user import UserModel, UserRegistObject
from account.util.student import get_generation_from_email, get_is_student_from_email
from util.auth import auth_by_google_token
from util.serverless import createRes, createErrorRes
from util.db import get_mongo_db


def hello(_, __):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": _,
    }

    return createRes(header={"Content-Type": "application/json"}, body=body)


def logout(event, _):
    db = get_mongo_db()

    token : str = event.headers.Authorization

    if (TokenModel(db).delete(token)):
        return createRes(header={}, body={})
    else:
        return createErrorRes(header={}, body={"message" : "권한이 없습니다."}, statusCode=401)
        

def login_or_regist(event, _):
    decode_token: dict[str, Any] = auth_by_google_token(event.headers.Authorization)
    sub: str = decode_token.get("sub")

    if sub is None:
        return createErrorRes(
            header={"Content-Type": "application/json"}, message="값이 뭔가 이상합니다."
        )

    db = get_mongo_db()
    userCollect = UserModel(db)
    tokenCollect = TokenModel(db)

    if userCollect.has_account():  # 계정 있는지 확인
        token: str = tokenCollect.add(sub)  # 있다면 바로 토큰 발급
    else:  # 없다면 회원가입 진행
        email: str = decode_token.get("email")
        name: str = decode_token.get("name")
        is_student: bool = get_is_student_from_email(email)

        if is_student:
            generation: int = get_generation_from_email(email)
        else:
            generation: int = 0

        regist_value: UserRegistObject = UserRegistObject(
            sub=sub,
            email=email,
            name=name,
            generation=generation,
            is_student=is_student,
        )

        userCollect.register(regist_value)
        token: str = tokenCollect.add(sub)

    return createRes(header={}, body={"token": token})
