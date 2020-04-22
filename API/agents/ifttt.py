from typing import Dict

import requests
from faker import Faker

from API.common import APIBase
from custom_types import News
from shortcuts import render_text_default


class IftttAPI(APIBase):
    LOGGING_NAME = __name__
    JSON_KEY = "ifttt"

    def broadcast_prod(self, news: News) -> None:
        ifttt_settings = self.get_api_tokens(news.site_name)
        if not ifttt_settings:
            return
        rendered_text = render_text_default(news)
        api_url = "https://maker.ifttt.com/trigger/{event}/with/key/{key}".format(
            event=ifttt_settings["event"],
            key=ifttt_settings["key"]
        )

        payload = {
            "value1": rendered_text
        }

        requests.post(api_url, json=payload)

    @classmethod
    def generate_fake_api_tokens(cls, fake: Faker) -> Dict[str, str]:
        return {
            "event": fake.user_name(),
            "key": fake.password(22)
        }
