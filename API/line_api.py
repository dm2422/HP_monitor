from typing import Optional

import requests

from API.structs import TokenOptionsEnum, Line
from crawlers.common import News
from settings import TOKENS
from utils import render_text_default


def get_line_tokens(school_name: str) -> Optional[Line]:
    tokens = TOKENS[school_name].line
    if tokens == TokenOptionsEnum.USE_SHARED:
        tokens = TOKENS["shared"].line

    assert not isinstance(tokens, TokenOptionsEnum)
    return tokens


def broadcast(news: News, school_name: str) -> None:
    line_tokens = get_line_tokens(school_name)
    if not line_tokens:
        return
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
        "Authorization": "Bearer " + line_tokens.channel_token,
        "Content-Type": "application/json"
    }

    requests.post(api_url, headers=headers, json=payload)
