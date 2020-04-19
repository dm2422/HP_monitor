import copy
from typing import Optional
from logging import getLogger
from typing import Callable

import tweepy

from API.structs import Twitter, TokenOptionsEnum
from crawlers.common import News
from settings import TOKENS
from utils import render_twitter_text

logger = getLogger(__name__)


def get_twitter_tokens(school_name: str, tokens=TOKENS) -> Optional[Twitter]:
    twitter_tokens = tokens[school_name].twitter
    if twitter_tokens == TokenOptionsEnum.USE_SHARED:
        twitter_tokens = tokens["shared"].twitter

    assert not isinstance(twitter_tokens, TokenOptionsEnum)
    return twitter_tokens


def broadcast_prod(news: News, school_name: str) -> None:
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


def broadcast_debug(news: News, school_name: str) -> None:
    logger.debug(f"A broadcast has occurred. {school_name=}, {news=}")


broadcast: Callable[[News, str], None] = broadcast_debug if __debug__ else broadcast_prod
