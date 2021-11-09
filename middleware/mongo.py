import os

import pymongo


def DB_CONNECT(db_url: str = os.environ["DB_PATH"]):
    def decorator(func):
        def wrap(*args, **kwargs):
            # db setting
            DB_NAME: str = os.environ["DB_NAME"]
            client = pymongo.MongoClient(db_url)
            db = client.get_database(DB_NAME)
            kwargs["DB"] = db

            # get result
            result = func(*args, **kwargs)

            # db disconnect and return values
            client.close()
            return result

        return wrap

    return decorator
