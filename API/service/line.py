import requests

from API.common import APIBase
from crawlers.common import News
from renderers import render_text_default


class LineAPI(APIBase):
    DEBUG_NAME = __name__
    KEY_NAME = "line"

    def broadcast_prod(self, news: News, school_name: str) -> None:
        line_tokens = self.get_tokens(school_name)
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
