import pymongo

import os


def get_mongo_db() -> pymongo.database.Database:
    return pymongo.MongoClient(os.environ["DB_PATH"])
