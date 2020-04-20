import glob
import importlib
import inspect
import os
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from functools import lru_cache
from logging import getLogger
from typing import List, Type

import jaconv

from crawlers import sites


@dataclass
class NewsHeader:
    origin_url: str
    title: str
    hash: str


@dataclass
class News(NewsHeader):
    content: str


class CrawlerBase(metaclass=ABCMeta):
    HP_URL: str
    SITE_NAME: str

    @abstractmethod
    def fetch_recent_news_headers(self) -> List[NewsHeader]:
        pass

    @abstractmethod
    def fetch_specific_news_content(self, news_header: NewsHeader) -> str:
        pass

    def get_latest_news(self, cached_hashes: List[str]) -> List[News]:
        """
        In here, "latest" means "not crawled before". So return type is list of uncrawled news.
        :param cached_hashes: Hashes that crawled before.
        :return: List of before uncrawled news.
        """
        ret: List[News] = []
        for header in filter(lambda x: not x.hash in cached_hashes, self.fetch_recent_news_headers()):
            raw_content = self.fetch_specific_news_content(header)
            news = News(
                title=jaconv.zen2han(header.title, digit=True, ascii=True, kana=False),
                content=jaconv.zen2han(raw_content, digit=True, ascii=True, kana=False),
                origin_url=header.origin_url,
                hash=header.hash
            )
            ret.append(news)
        return ret


@lru_cache
def get_all_crawler_classes() -> List[Type[CrawlerBase]]:
    logger = getLogger(__name__)
    ret: List[Type[CrawlerBase]] = []
    for e in glob.glob(os.path.join(sites.__path__[0], "*.py")):
        if "__init__" in e:
            continue
        e = e.replace("\\", "/")
        module_name: str = e[e.rfind("/") + 1: -3]
        crawler_module = importlib.import_module(f"crawlers.sites.{module_name}")

        clazz: type
        for clazz in map(lambda x: x[1], inspect.getmembers(crawler_module, inspect.isclass)):
            if CrawlerBase in clazz.__bases__:
                clazz: Type[CrawlerBase]
                ret.append(clazz)
                logger.debug(f"A crawler has installed! - {clazz}")
    return ret
