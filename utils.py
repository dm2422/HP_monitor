import requests
import json
from typing import List, Dict

from crawlers.common import News
from settings import HISTORY_JSON_PATH, CRAWLER_CLASSES, CHANNEL_TOKEN, MESSAGE_TEMPLATE

UTAKA_URL = "http://www.tochigi-edu.ed.jp/utsunomiya/nc2/"


def broadcast(text: str) -> None:
    api_url = "https://api.line.me/v2/bot/message/broadcast"

    payload = {
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }

    headers = {
        "Authorization": CHANNEL_TOKEN,
        "Content-Type": "application/json"
    }

    requests.post(api_url, headers=headers, json=payload)


def check_update() -> Dict[str, List[News]]:
    crawled_news: Dict[str, List[News]] = {}

    with open(HISTORY_JSON_PATH, "r", encoding="utf-8") as rf:
        history: Dict = json.load(rf)

    for crawler_class in CRAWLER_CLASSES:
        hashes: List[str] = history.get(crawler_class.SCHOOL_NAME, [])
        crawler = crawler_class()
        least_news = crawler.get_least_news(hashes)
        history[crawler_class.SCHOOL_NAME] = hashes + list(map(lambda x: x.hash, least_news))
        crawled_news[crawler_class.SCHOOL_NAME] = least_news

    with open(HISTORY_JSON_PATH, "w", encoding="utf-8") as wf:
        json.dump(history, wf, indent=4, ensure_ascii=False)

    return crawled_news


def render_message_text(news: News, school_name: str) -> str:
    return MESSAGE_TEMPLATE.format(
        name=school_name,
        title=news.title,
        content=news.content,
        url=news.origin_url
    )
