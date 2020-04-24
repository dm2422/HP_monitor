import json
from collections import deque
from dataclasses import asdict
from logging import getLogger
from typing import List, Dict, Deque

from API.common import get_all_api_classes
from const_settings import HISTORY_JSON_PATH, MESSAGE_TEMPLATE
from crawlers.common import get_all_crawler_classes
from custom_types import News
from settings import TOKEN_TABLE


def check_update() -> Deque[News]:
    logger = getLogger(check_update.__qualname__)
    crawled_news: Deque[News] = deque()

    with open(HISTORY_JSON_PATH, "r", encoding="utf-8") as rf:
        history: Dict = json.load(rf)
    logger.debug(f"'{HISTORY_JSON_PATH}' has loaded successfully!")

    using_crawlers = filter(lambda c: c.SITE_NAME in TOKEN_TABLE.keys(), get_all_crawler_classes())
    for crawler_class in using_crawlers:
        logger.debug(f"Start crawling '{crawler_class.SITE_NAME}' HP.")
        hashes: List[str] = history.get(crawler_class.SITE_NAME, [])
        crawler = crawler_class()
        latest_news = crawler.get_latest_news(hashes)
        logger.info(f"'{crawler_class.SITE_NAME}' has {len(latest_news)} latest news.")
        history[crawler_class.SITE_NAME] = hashes + [x.hash for x in latest_news]
        crawled_news += latest_news
        logger.debug(f"Finished crawling '{crawler_class.SITE_NAME}' HP.")

    with open(HISTORY_JSON_PATH, "w", encoding="utf-8") as wf:
        json.dump(history, wf, indent=2, ensure_ascii=False)
    logger.debug(f"'{HISTORY_JSON_PATH}' has saved successfully!")

    return crawled_news


def broadcast_all(news: News) -> None:
    logger = getLogger(broadcast_all.__qualname__)
    logger.info(f"Start broadcast - {news.hash[:8]}:{news.site_name}:{news.title}")
    for clazz in get_all_api_classes():
        try:
            clazz().broadcast(news)
        except Exception as e:
            logger.exception(e)

    logger.info(f"Finish broadcast - {news.hash[:8]}")


def render_text_default(news: News) -> str:
    return MESSAGE_TEMPLATE.format(**asdict(news))
