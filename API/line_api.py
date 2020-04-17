import requests

from crawlers.common import News
from settings import TOKENS
from utils import render_text_default


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
        "Authorization": TOKENS[school_name].line.channel_token,
        "Content-Type": "application/json"
    }

    requests.post(api_url, headers=headers, json=payload)
