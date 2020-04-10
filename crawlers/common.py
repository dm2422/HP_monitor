from abc import ABCMeta, abstractmethod
from typing import List


class NewsHeader:
    origin_url: str
    title: str
    hash: str

    def __init__(self, news_url: str, news_title: str, news_hash: str):
        """
        News header should not contain news content
        :param news_url: The URL to news content.
        :param news_title: News title.
        :param news_hash: This is used for checking out uncrawled news.
        """
        self.origin_url = news_url
        self.title = news_title
        self.hash = news_hash


class News(NewsHeader):
    content: str

    def __init__(self, header: NewsHeader, content: str):
        """
        News should contain news content.
        :param header: This news header.
        :param content: News content.
        """
        super().__init__(header.origin_url, header.title, header.hash)
        self.content = content


class CrawlerBase(metaclass=ABCMeta):

    @property
    @abstractmethod
    def HP_URL(self) -> str:
        pass

    @property
    @abstractmethod
    def SCHOOL_NAME(self) -> str:
        pass

    @abstractmethod
    def fetch_recent_news_headers(self) -> List[NewsHeader]:
        pass

    @abstractmethod
    def fetch_specific_news_content(self, news_header: NewsHeader) -> str:
        pass

    def get_least_news(self, cached_hashes: List[str]) -> List[News]:
        """
        In here, "least" means "not crawled before". So return type is list of uncrawled news.
        :param cached_hashes: Hashes that crawled before.
        :return: List of before uncrawled news.
        """
        ret: List[News] = []
        for header in filter(lambda x: not x.hash in cached_hashes, self.fetch_recent_news_headers()):
            ret.append(News(header, self.fetch_specific_news_content(header)))
        return ret
