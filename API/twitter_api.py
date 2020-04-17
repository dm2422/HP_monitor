import copy

import tweepy

from crawlers.common import News
from settings import TOKENS
from utils import render_twitter_text


def broadcast(news: News, school_name: str) -> None:
    twitter_tokens = TOKENS[school_name].twitter
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
