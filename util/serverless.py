import json
from typing import Any


def createRes(header : dict[str, Any], body: dict[str, Any], statusCode : int = 200):
  return {
    "statusCode" : statusCode,
    "headers" : header,
    "body" : json.dumps(body) 
  }