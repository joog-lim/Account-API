from typing import Any
import pymongo


class UserRegistObject:
    sub: str
    email: str
    name: str
    generation: int
    is_student: bool

    def __init__(
        self, sub: str, email: str, name: str, generation: int, is_student: bool
    ) -> None:
        self.sub = sub
        self.email = email
        self.name = name
        self.generation = generation
        self.is_student = is_student


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
            "sub": args.sub,
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

    async def get_user_info(self, arg: str):
        """
        arg를 토대로 유저 정보를 받아옵니다.
        
        arg_list : list[str] = ["sub", "email"]
        """
        arg_list : list[str] = ["sub", "email"]
        if arg in arg_list:
            return list(
                self.collect.find(
                    {arg: arg},
                    {
                        "_id": False,
                        "email": True,
                        "name": True,
                        "generation": True,
                        "is_student": True,
                    },
                )
            )

    async def has_account(self, sub: str) -> bool:
        return not not (self.collect.find({"sub": sub}, {"_id": True}))
