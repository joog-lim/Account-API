from datetime import datetime, timedelta
import os

import pymongo

from config import service_timezone
from cryptography.fernet import Fernet


class TokenModel:
    def __init__(self, db: pymongo.database.Database):
        """
        db : pymongo.database.Database

        self.collect : pymongo.collection.Collection
        this collection name is `session`
        """
        self.collect: pymongo.collection.Collection = db["session"]
        self.now = datetime.now(service_timezone)

    fernet: Fernet = Fernet(os.environ["CRYPTO_KEY"])

    @staticmethod
    def decode_token(token: str) -> str:
        """
        TokenModel에서 추가된 각 토큰들을 해석해줍니다.

        return : str
        """
        token_bytes: bytes = token.encode("ascii")

        decode_token: bytes = TokenModel.fernet.decrypt(token_bytes)
        return decode_token.decode("ascii").split(os.environ["DISTINGUISHER"])[0]

    @staticmethod
    def encode_token(sub: str, created_at: str) -> str:
        token_byte: bytes = TokenModel.fernet.encrypt(
            (sub + os.environ["DISTINGUISHER"] + created_at).encode("ascii")
        )
        token_str: str = token_byte.decode("ascii")
        return token_str

    def add(self, sub: str) -> str:
        insert_value: dict = {
            "created_at": datetime.now(service_timezone),
            "renew_able_at": datetime.now(service_timezone) + timedelta(days=20),
            "expired_at": datetime.now(service_timezone) + timedelta(days=30),
        }

        token_str: str = TokenModel.encode_token(
            sub, str(insert_value["created_at"].timestamp())
        )
        insert_value.update(token_str=token_str)
        self.collect.insert(insert_value)

        return token_str

    def delete_by_token(self, token: str) -> bool:
        self.collect.remove({"token_str": token})
        return True

    def find(self, token: str):
        return self.collect.find_one(
            {"token_str": token},
            {"_id": False, "token": token, "renew_able_at": True, "expired_at": True},
        )
