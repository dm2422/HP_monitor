from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List

import jaconv


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
    SCHOOL_NAME: str

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
