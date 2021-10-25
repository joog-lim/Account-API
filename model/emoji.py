import pymongo


class EmojiModel:
    reaction_list = ["leaf"]

    def __init__(self, db: pymongo.database.Database):
        """
        db : pymongo.database.Database

        self.collect : pymongo.collection.Collection
        this collection name is `emoji`
        """
        self.collect: pymongo.collection.Collection = db["emoji"]

    def add(self, sub: str, algorithem_num: int, reaction: str = "leaf"):
        """
        add emoji(leaf)
        """
        if self.collect.find_one(
            {"number": algorithem_num, "sub": sub, "reaction": reaction}
        ):
            return False

        self.collect.insert(
            {"number": algorithem_num, "sub": sub, "reaction": reaction}
        )
        return True

    def remove(self, sub: str, algorithem_num: int, reaction: str = "leaf"):
        """
        remove emoji(leaf)
        """
        if reaction not in EmojiModel.reaction_list:
            return False

        self.collect.remove(
            {"number": algorithem_num, "sub": sub, "reaction": reaction}
        )
        return True

    def join_emoji(self, number: int):
        return list(
            self.collect.aggregate(
                [
                    {"$match": {"number": number}},
                    {
                        "$group": {
                            "_id": "$reaction",
                            "count": {"$sum": 1},
                        }
                    },
                ]
            )
        )
