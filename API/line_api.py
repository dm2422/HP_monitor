import requests

from API.tokens import line_tokens
from crawlers.common import News
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
        "Authorization": line_tokens.channel_token,
        "Content-Type": "application/json"
    }

    requests.post(api_url, headers=headers, json=payload)
