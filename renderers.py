from const_settings import MESSAGE_TEMPLATE
from crawlers.common import News


def render_text_default(news: News, school_name: str) -> str:
    return MESSAGE_TEMPLATE.format(
        name=school_name,
        title=news.title,
        content=news.content,
        url=news.origin_url
    )


def render_twitter_text(news: News, school_name: str) -> str:
    no_content_len = len(MESSAGE_TEMPLATE.format(
        name=school_name,
        title=news.title,
        content="",
        url=""
    )) + 24  # URL is always counted as 22~24 characters.
    content_max_len = 140 - no_content_len
    if content_max_len < len(news.content):
        news.content = news.content[:content_max_len - 3] + "..."
    return render_text_default(news, school_name)
