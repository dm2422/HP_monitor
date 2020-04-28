import time
from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import asdict
from logging import getLogger
from typing import List, Type, Dict

from API.common import get_all_api_classes
from const_settings import MESSAGE_TEMPLATE, MAX_WORKERS
from crawlers.common import get_all_crawler_classes, CrawlerBase
from custom_types import News
from settings import TOKEN_TABLE
from utils import load_history, save_history, initialize_logger, wrap_one_arg


@wrap_one_arg
def crawl_news_with_class(clazz: Type[CrawlerBase], history: Dict[str, List[str]]) -> List[News]:
    initialize_logger()
    logger = getLogger(clazz.__qualname__)
    hashes = history.get(clazz.SITE_NAME, [])

    logger.debug(f"Start crawling news at {clazz.SITE_NAME}.")
    start_time = time.time()
    try:
        latest_news = clazz().get_latest_news(hashes)
    except Exception as e:
        logger.exception(e)
        latest_news = []
    elapsed = time.time() - start_time
    logger.info(f"Crawled {len(latest_news)} news in {round(elapsed, 2)} seconds.")

    history[clazz.SITE_NAME] = hashes + [x.hash for x in latest_news]
    return latest_news


def check_update() -> List[News]:
    history = load_history()

    using_crawlers = filter(lambda c: c.SITE_NAME in TOKEN_TABLE.keys(), get_all_crawler_classes())
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        params = [(clazz, history) for clazz in using_crawlers]
        result = executor.map(crawl_news_with_class, params)

    save_history(history)
    return sum(list(result), [])


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
