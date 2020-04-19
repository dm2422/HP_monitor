from logging import getLogger
from typing import Callable

import requests

from crawlers.common import News
from settings import TOKENS
from utils import render_text_default

logger = getLogger(__name__)


def broadcast_prod(news: News, school_name: str) -> None:
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
        "Authorization": "Bearer " + TOKENS[school_name].line.channel_token,
        "Content-Type": "application/json"
    }

    requests.post(api_url, headers=headers, json=payload)


def broadcast_debug(news: News, school_name: str) -> None:
    logger.debug(f"A broadcast has occurred. {school_name=}, {news=}")


broadcast: Callable[[News, str], None] = broadcast_debug if __debug__ else broadcast_prod
