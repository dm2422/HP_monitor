import json
from dataclasses import dataclass

from settings import TOKENS_JSON_PATH

with open(TOKENS_JSON_PATH, "r", encoding="utf-8") as rf:
    tokens = json.load(rf)


@dataclass
class Line:
    channel_token: str


@dataclass
class Twitter:
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str


line_tokens = Line(**tokens["line"])
twitter_tokens = Twitter(**tokens["twitter"])
