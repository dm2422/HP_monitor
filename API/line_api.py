import json
from dataclasses import dataclass

import requests

from crawlers.common import News
from settings import TOKENS_JSON_PATH
from utils import render_text_default


@dataclass
class Line:
    channel_token: str


with open(TOKENS_JSON_PATH, "r", encoding="utf-8") as rf:
    line_tokens = Line(**json.load(rf)["line"])


def broadcast(news: News, school_name: str) -> None:
    rendered_text = render_text_default(news, school_name)
    api_url = "https://api.line.me/v2/bot/message/broadcast"

    payload = {
        "messages": [
            {
                "type": "text",
                "text": rendered_text
            }
        ]
    }

    headers = {
        "Authorization": line_tokens.channel_token,
        "Content-Type": "application/json"
    }

    requests.post(api_url, headers=headers, json=payload)
