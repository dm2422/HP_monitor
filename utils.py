import json
from typing import List, Dict

import jaconv

from const_settings import HISTORY_JSON_PATH, MESSAGE_TEMPLATE
from crawlers.common import News
from settings import CRAWLER_CLASSES


def initialize_logger():
    import logging
    logging.basicConfig(
        level=logging.DEBUG if __debug__ else logging.INFO,
        format="%(asctime)s | %(levelname)s:%(name)s:%(message)s"
    )
    logging.debug("The logger has been initialized.")


def check_update() -> Dict[str, List[News]]:
    crawled_news: Dict[str, List[News]] = {}

    with open(HISTORY_JSON_PATH, "r", encoding="utf-8") as rf:
        history: Dict = json.load(rf)

    for crawler_class in CRAWLER_CLASSES:
        hashes: List[str] = history.get(crawler_class.SCHOOL_NAME, [])
        crawler = crawler_class()
        latest_news = crawler.get_latest_news(hashes)
        history[crawler_class.SCHOOL_NAME] = hashes + list(map(lambda x: x.hash, latest_news))
        crawled_news[crawler_class.SCHOOL_NAME] = latest_news

    with open(HISTORY_JSON_PATH, "w", encoding="utf-8") as wf:
        json.dump(history, wf, indent=4, ensure_ascii=False)

    return crawled_news


def render_text_default(news: News, school_name: str) -> str:
    return MESSAGE_TEMPLATE.format(
        name=school_name,
        title=news.title,
        content=jaconv.zen2han(news.content, digit=True, ascii=True, kana=False),
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
