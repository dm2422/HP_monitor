import tweepy

from API.tokens import twitter_tokens
from crawlers.common import News
from settings import MESSAGE_TEMPLATE
from utils import render_text_default

auth = tweepy.OAuthHandler(
    twitter_tokens.consumer_key,
    twitter_tokens.consumer_secret
)
auth.set_access_token(
    twitter_tokens.access_token,
    twitter_tokens.access_token_secret
)

twitter_api = tweepy.API(auth)


def render_twitter_text(news: News, school_name: str):
    no_content_len = len(MESSAGE_TEMPLATE.format(
        name=school_name,
        title=news.title,
        content="",
        url=news.origin_url
    ))
    content_max_len = 140 - no_content_len
    if content_max_len < len(news.content):
        news.content = news.content[:content_max_len - 3] + "..."
    return render_text_default(news, school_name)


def broadcast(news: News, school_name: str):
    rendered_text = render_twitter_text(news, school_name)
    twitter_api.update_status(rendered_text)
