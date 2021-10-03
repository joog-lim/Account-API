import json

from util.serverless import createRes


def hello(_, __):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input" : _
    }

    return createRes(header={
            "Content-Type": "application/json"
        }, body=body)