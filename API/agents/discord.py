from typing import Dict

import requests
from faker import Faker

from API.common import APIBase
from custom_types import News, TokenDict
from shortcuts import render_text_default


class DiscordAPI(APIBase):
    LOGGING_NAME = __name__
    JSON_KEY = "discord"

    def broadcast_prod(self, news: News, tokens: TokenDict) -> None:
        rendered_text = render_text_default(news)
        api_base_url = "https://discordapp.com/api/webhooks/"

        payload = {
            "content": rendered_text
        }

        api_uri = api_base_url + tokens["webhook_token"]

        requests.post(api_uri, json=payload)

    @classmethod
    def generate_fake_api_tokens(cls, fake: Faker) -> Dict[str, str]:
        return {
            "webhook_token": fake.password(18) + "/" + fake.password(68)
        }
