import copy
from typing import Optional

import tweepy

from API.structs import Twitter, LineEnum
from crawlers.common import News
from settings import TOKENS
from utils import render_twitter_text


def get_twitter_tokens(school_name: str) -> Optional[Twitter]:
    tokens = TOKENS[school_name].twitter
    if tokens == LineEnum.USE_SHARED:
        tokens = TOKENS["shared"].twitter

    assert not isinstance(tokens, LineEnum)
    return tokens


def broadcast(news: News, school_name: str) -> None:
    twitter_tokens = get_twitter_tokens(school_name)
    if not twitter_tokens:
        return
    auth = tweepy.OAuthHandler(
        twitter_tokens.consumer_key,
        twitter_tokens.consumer_secret
    )
    auth.set_access_token(
        twitter_tokens.access_token,
        twitter_tokens.access_token_secret
    )

    twitter_api = tweepy.API(auth)
    rendered_text = render_twitter_text(copy.copy(news), school_name)
    twitter_api.update_status(rendered_text)
