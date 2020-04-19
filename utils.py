import json
from typing import List, Dict

from API.common import get_all_api_classes
from const_settings import HISTORY_JSON_PATH
from crawlers.common import News, get_all_crawler_classes


def check_update() -> Dict[str, List[News]]:
    crawled_news: Dict[str, List[News]] = {}

    with open(HISTORY_JSON_PATH, "r", encoding="utf-8") as rf:
        history: Dict = json.load(rf)

    for crawler_class in get_all_crawler_classes():
        hashes: List[str] = history.get(crawler_class.SCHOOL_NAME, [])
        crawler = crawler_class()
        latest_news = crawler.get_latest_news(hashes)
        history[crawler_class.SCHOOL_NAME] = hashes + list(map(lambda x: x.hash, latest_news))
        crawled_news[crawler_class.SCHOOL_NAME] = latest_news

    with open(HISTORY_JSON_PATH, "w", encoding="utf-8") as wf:
        json.dump(history, wf, indent=4, ensure_ascii=False)

    return crawled_news


def broadcast_all(news: News, school_name: str) -> None:
    for clazz in get_all_api_classes():
        clazz().broadcast(news, school_name)
