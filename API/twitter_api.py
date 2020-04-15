import json
from dataclasses import dataclass

import tweepy

from crawlers.common import News
from settings import TOKENS_JSON_PATH


@dataclass
class Twitter:
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str


with open(TOKENS_JSON_PATH, "r", encoding="utf-8") as rf:
    twitter_tokens = Twitter(**json.load(rf)["twitter"])

auth = tweepy.OAuthHandler(
    twitter_tokens.consumer_key,
    twitter_tokens.consumer_secret
)
auth.set_access_token(
    twitter_tokens.access_token,
    twitter_tokens.access_token_secret
)

twitter_api = tweepy.API(auth)


def broadcast(news: News, school_name: str):
    pass
