import json

from account.util.serverless import createRes


def hello(_, __):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
    }

    return createRes(header={
            "Content-Type": "application/json"
        }, body=body)