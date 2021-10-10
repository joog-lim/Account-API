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

    async def add(self, sub: str) -> bool:
        insert_value: dict[str, Any] = {
            "sub": sub,
            "created_at": datetime.now(timezone("Asia/Seoul")),
            "renew_able_at": datetime.now(timezone("Asia/Seoul")) + timedelta(days=20),
            "expired_at": datetime.now(timezone("Asia/Seoul")) + timedelta(days=30),
        }
        fernet = Fernet(os.environ["CRYPTO_KEY"])
        token_byte: bytes = fernet.encrypt(
            (sub + str(insert_value["created_at"].timestamp()).encode("ascii"))
        )
        token_str: str = token_byte.decode("ascii")

        self.collect.insert(dict(insert_value, {"token": token_str}))

        return token_str

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
