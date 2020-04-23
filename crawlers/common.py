from abc import ABCMeta, abstractmethod
from functools import lru_cache
from typing import List, Type, cast

import jaconv

from custom_types import NewsHeader, News
from utils import get_all_classes_from_package


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
        for header in filter(lambda x: x.hash not in cached_hashes, self.fetch_recent_news_headers()):
            raw_content = self.fetch_specific_news_content(header)
            news = News(
                site_name=self.SITE_NAME,
                title=jaconv.zen2han(header.title, digit=True, ascii=True, kana=False),
                content=jaconv.zen2han(raw_content, digit=True, ascii=True, kana=False),
                content_url=header.content_url,
                hash=header.hash
            )
            ret.append(news)
        return ret


@lru_cache
def get_all_crawler_classes() -> List[Type[CrawlerBase]]:
    import crawlers
    import crawlers.sites
    return cast(List[Type[CrawlerBase]], get_all_classes_from_package(
        crawlers.sites.__name__,
        lambda c: crawlers.common.CrawlerBase in c.__bases__
    ))
