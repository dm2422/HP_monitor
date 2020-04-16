import tweepy

from API.tokens import twitter_tokens
from crawlers.common import News
from utils import render_twitter_text

auth = tweepy.OAuthHandler(
    twitter_tokens.consumer_key,
    twitter_tokens.consumer_secret
)
auth.set_access_token(
    twitter_tokens.access_token,
    twitter_tokens.access_token_secret
)

twitter_api = tweepy.API(auth)


def broadcast(news: News, school_name: str) -> None:
    rendered_text = render_twitter_text(news, school_name)
    twitter_api.update_status(rendered_text)
