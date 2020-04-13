import json
from dataclasses import dataclass

import requests

from settings import TOKENS_JSON_PATH


@dataclass
class Line:
    channel_token: str


with open(TOKENS_JSON_PATH, "r", encoding="utf-8") as rf:
    line_tokens = Line(**json.load(rf)["line"])


def broadcast(text: str) -> None:
    api_url = "https://api.line.me/v2/bot/message/broadcast"

    payload = {
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }

    headers = {
        "Authorization": line_tokens.channel_token,
        "Content-Type": "application/json"
    }

    requests.post(api_url, headers=headers, json=payload)
