from datetime import datetime, timedelta
import os

import pymongo

from pytz import timezone
from cryptography.fernet import Fernet
from typing import Any


class TokenModel:
    def __init__(self, db: pymongo.database.Database):
        """
        db : pymongo.database.Database

        self.collect : pymongo.collection.Collection
        this collection name is `user`
        """
        self.collect: pymongo.collection.Collection = db["session"]

    fernet: Fernet = Fernet(os.environ["CRYPTO_KEY"])

    @staticmethod
    def decode_token(token: str) -> str:
        """
        TokenModel에서 추가된 각 토큰들을 해석해줍니다.

        return : str
        """
        token_bytes: bytes = token.encode("ascii")

        decode_token: str = TokenModel.fernet.decrypt(token_bytes)
        return decode_token

    @staticmethod
    def encode_token(sub: str, created_at: str) -> str:
        token_byte: bytes = TokenModel.fernet.encrypt(
            (sub + os.environ["DISTINGUISHER"] + created_at).encode("ascii")
        )
        token_str: str = token_byte.decode("ascii")
        return token_str

    async def add(self, sub: str) -> bool:
        insert_value: dict[str, Any] = {
            "sub": sub,
            "created_at": datetime.now(timezone("Asia/Seoul")),
            "renew_able_at": datetime.now(timezone("Asia/Seoul")) + timedelta(days=20),
            "expired_at": datetime.now(timezone("Asia/Seoul")) + timedelta(days=30),
        }

        token_str: str = TokenModel.encode_token(
            sub, str(insert_value["created_at"].timestamp())
        )

        self.collect.insert(dict(insert_value, {"token": token_str}))

        return True

    async def delete(self, token: str) -> bool:
        self.collect.remove({"token": token})
        return True

    async def find(self, token: str):
        return list(
            self.collect.find(
                {"token": token},
                {"_id": False, "sub": True, "renew_able_at": True, "expired_at": True},
            )
        )
