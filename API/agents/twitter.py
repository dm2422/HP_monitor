from copy import copy
from typing import Dict

import tweepy
from faker import Faker

from API.common import APIBase
from const_settings import MESSAGE_TEMPLATE
from custom_types import News
from shortcuts import render_text_default


class TwitterAPI(APIBase):
    LOGGING_NAME = __name__
    JSON_KEY = "twitter"

    def broadcast_prod(self, news: News) -> None:
        twitter_tokens = self.get_api_tokens(news.site_name)
        if not twitter_tokens:
            return
        auth = tweepy.OAuthHandler(
            twitter_tokens["consumer_key"],
            twitter_tokens["consumer_secret"]
        )
        auth.set_access_token(
            twitter_tokens["access_token"],
            twitter_tokens["access_token_secret"]
        )

        twitter_api = tweepy.API(auth)
        rendered_text = render_twitter_text(news)
        twitter_api.update_status(rendered_text)

    @classmethod
    def generate_fake_api_tokens(cls, fake: Faker) -> Dict[str, str]:
        return {
            "consumer_key": fake.password(25),
            "consumer_secret": fake.password(50),
            "access_token": fake.password(50),
            "access_token_secret": fake.password(45)
        }


def render_twitter_text(news: News) -> str:
    news = copy(news)
    no_content_len = len(MESSAGE_TEMPLATE.format(
        site_name=news.site_name,
        title=news.title,
        content="",
        content_url=""
    )) + 24  # URL is always counted as 22~24 characters.
    content_max_len = 140 - no_content_len
    if content_max_len < len(news.content):
        news.content = news.content[:content_max_len - 3] + "..."
    return render_text_default(news)
