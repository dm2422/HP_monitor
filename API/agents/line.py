import requests
from faker import Faker

from API.common import APIBase
from custom_types import News, TokenDict
from shortcuts import render_text_default


class LineAPI(APIBase):
    LOGGING_NAME = __name__
    JSON_KEY = "line"

    def broadcast_prod(self, news: News, tokens: TokenDict) -> None:
        rendered_text = render_text_default(news)
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
            "Authorization": "Bearer " + tokens["channel_token"],
            "Content-Type": "application/json"
        }

        requests.post(api_url, headers=headers, json=payload)

    @classmethod
    def generate_fake_api_tokens(cls, fake: Faker) -> TokenDict:
        return {
            "channel_token": fake.password(172)
        }
