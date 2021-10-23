import json

from middleware.token import TOKEN_MANAGE
from middleware.mongo import DB_CONNECT

from model.emoji import EmojiModel
from model.token import TokenModel
from model.user import UserModel, UserRegistObject

from util.student import get_generation_from_email, get_is_student_from_email
from util.auth import auth_by_google_token
from util.serverless import createRes, createErrorRes


def hello(event, __):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event,
    }
    print(1)
    return createRes(header={"Content-Type": "application/json"}, body=body)


@DB_CONNECT()
def logout(event, _, DB):
    db = DB

    token: str = event["headers"]["Authorization"]

    if TokenModel(db).delete(token):
        return createRes(header={}, body={})
    else:
        return createErrorRes(header={}, body={"message": "권한이 없습니다."}, statusCode=401)


@DB_CONNECT()
def login_or_regist(event, _, DB):

    decode_token = auth_by_google_token(event["headers"]["Authorization"])
    sub: str = decode_token.get("sub")
    if sub is None:
        return createErrorRes(
            header={"Content-Type": "application/json"}, message=decode_token["error"]
        )

    db = DB
    user_collect = UserModel(db)
    token_collect = TokenModel(db)
    print(user_collect.has_account(sub))
    if user_collect.has_account(sub):  # 계정 있는지 확인
        token: str = token_collect.add(sub)  # 있다면 바로 토큰 발급
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

        user_collect.register(regist_value)
        token: str = token_collect.add(sub)

    return createRes(header={}, body={"token": token})


@DB_CONNECT()
@TOKEN_MANAGE()
def add_emoji(event, _, DB, TOKEN, sub):
    emoji: str = event["pathParameters"]["emoji"]
    algorithem_num: int = json.loads(event["body"])["num"]

    emoji_collect = EmojiModel(DB)

    if emoji not in EmojiModel.reaction_list:
        return createErrorRes(header={}, message="Bad Request", statusCode=400)

    if emoji_collect.add(sub, algorithem_num=algorithem_num, reaction=emoji):
        return createRes(
            header={
                "Set-Cookie": f"token={TOKEN}; Secure; HttpOnly; Domain=server.joog-lim.info; Path=/"
            },
            body={"message": "success"},
        )
    else:
        return createErrorRes(
            header={}, message="Already been processed", statusCode=418
        )


@DB_CONNECT()
@TOKEN_MANAGE()
def remove_emoji(event, _, DB, TOKEN, sub):
    emoji: str = event["pathParameters"]["emoji"]
    algorithem_num: int = json.loads(event["body"])

    emoji_collect = EmojiModel(DB)

    if emoji not in EmojiModel.reaction_list:
        return createErrorRes(header={}, message="Bad Request", statusCode=400)

    if emoji_collect.remove(sub, algorithem_num=algorithem_num, reaction=emoji):
        return createRes(
            header={
                "Set-Cookie": f"token={TOKEN}; Secure; HttpOnly; Domain=server.joog-lim.info; Path=/"
            },
            body={"message": "success"},
        )
    else:
        return createErrorRes(
            header={}, message="Already been processed", statusCode=418
        )


@DB_CONNECT()
def join_emoji(event, _, DB):
    algorithem_num: int = int(event["queryStringParameters"]["num"])
    emoji = EmojiModel(DB).join_emoji(algorithem_num)
    return createRes(header={}, body={i["_id"]: i["count"] for i in emoji})
