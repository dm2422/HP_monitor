from typing import Dict

import requests
from faker import Faker

from API.common import APIBase
from crawlers.common import News
from shortcuts import render_text_default


class LineAPI(APIBase):
    LOGGING_NAME = __name__
    JSON_KEY = "line"

    def broadcast_prod(self, news: News, site_name: str) -> None:
        line_tokens = self.get_agent_tokens(site_name)
        if not line_tokens:
            return
        rendered_text = render_text_default(news, site_name)
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
            "Authorization": "Bearer " + line_tokens["channel_token"],
            "Content-Type": "application/json"
        }

        requests.post(api_url, headers=headers, json=payload)

    @classmethod
    def generate_fake_tokens(cls, fake: Faker) -> Dict[str, str]:
        return {
            "channel_token": fake.password(172)
        }
