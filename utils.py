import json
from logging import getLogger
from typing import List, Dict

from API.common import get_all_api_classes
from const_settings import HISTORY_JSON_PATH, MESSAGE_TEMPLATE
from crawlers.common import News, get_all_crawler_classes

logger = getLogger(__name__)


def check_update() -> Dict[str, List[News]]:
    crawled_news: Dict[str, List[News]] = {}

    with open(HISTORY_JSON_PATH, "r", encoding="utf-8") as rf:
        history: Dict = json.load(rf)
    logger.debug(f"'{HISTORY_JSON_PATH}' has loaded successfully!")

    for crawler_class in get_all_crawler_classes():
        logger.debug(f"Start crawling '{crawler_class.SCHOOL_NAME}' HP.")
        hashes: List[str] = history.get(crawler_class.SCHOOL_NAME, [])
        crawler = crawler_class()
        latest_news = crawler.get_latest_news(hashes)
        logger.info(f"'{crawler_class.SCHOOL_NAME}' has {len(latest_news)} latest news.")
        history[crawler_class.SCHOOL_NAME] = hashes + list(map(lambda x: x.hash, latest_news))
        crawled_news[crawler_class.SCHOOL_NAME] = latest_news
        logger.debug(f"Finished crawling '{crawler_class.SCHOOL_NAME}' HP.")

    with open(HISTORY_JSON_PATH, "w", encoding="utf-8") as wf:
        json.dump(history, wf, indent=4, ensure_ascii=False)
    logger.debug(f"'{HISTORY_JSON_PATH}' has saved successfully!")

    return crawled_news


def broadcast_all(news: News, school_name: str) -> None:
    logger.info(f"Start broadcast - {school_name}:{news}")
    for clazz in get_all_api_classes():
        try:
            clazz().broadcast(news, school_name)
        except Exception as e:
            logger.exception(e)

    logger.info(f"Finish broadcast - {school_name}:{news}")


def render_text_default(news: News, school_name: str) -> str:
    return MESSAGE_TEMPLATE.format(
        name=school_name,
        title=news.title,
        content=news.content,
        url=news.origin_url
    )
