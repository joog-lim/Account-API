from typing import Any
import pymongo


class UserRegistObject:
    sub : str
    email: str
    name: str
    generation: int
    is_student: bool


class UserModel:
    def __init__(self, db: pymongo.database.Database):
        """
        db : pymongo.database.Database

        self.collect : pymongo.collection.Collection
        this collection name is `user`
        """
        self.collect: pymongo.collection.Collection = db["user"]

    async def register(self, args: UserRegistObject) -> bool:
        insert_value: dict[str, Any] = {
            "sub" : args.sub,
            "email": args.email,
            "name": args.name,
            "generation": args.generation,
            "is_student": args.is_student,
        }
        self.collect.insert(insert_value)
        return True

    async def delete_account(self, email: str) -> bool:
        self.collect.remove({"email": email})
        return True

    async def get_user_info(self, email: str):
        return list(
            self.collect.find(
                {"email": email},
                { "_id" : False, "email": True, "name": True, "generation": True, "is_student": True},
            )
        )
