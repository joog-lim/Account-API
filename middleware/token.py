from pytz import timezone

from util.serverless import createErrorRes

from model.token import TokenModel
from config import service_timezone


def TOKEN_MANAGE():
    def decorator(func):
        def wrap(*args, **kwargs):
            token: str = args[0]["headers"]["Authorization"]

            token_model = TokenModel(kwargs["DB"])

            token_inform = token_model.find(token)
            if not token_inform:
                return createErrorRes(header={}, message="인가되지않은 토큰입니다.")

            expired_at = token_inform["expired_at"].replace(tzinfo=service_timezone)
            print(token_model.now, expired_at)
            if token_model.now > expired_at:
                token_model.delete(token)
                return createErrorRes(header={}, message="토큰이 만료되었습니다.")

            renew_able_at = token_inform["renew_able_at"].replace(
                tzinfo=service_timezone
            )
            sub = token_model.decode_token(token)

            if renew_able_at < token_model.now:
                token_model.delete(token)
                new_token: str = token_model.add(sub)
                kwargs["TOKEN"] = new_token
            else:
                kwargs["TOKEN"] = token
            kwargs["sub"] = sub
            result = func(*args, **kwargs)
            return result

        return wrap

    return decorator
