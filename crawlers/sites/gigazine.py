import hashlib
from typing import List

import bs4
import requests

from crawlers.common import CrawlerBase
from custom_types import NewsHeader


class Gigazine(CrawlerBase):
    HP_URL = "https://gigazine.net/"
    SITE_NAME = "GIGAZINE"

    def fetch_recent_news_headers(self) -> List[NewsHeader]:
        fetched_news_header: List[NewsHeader] = []
        res = requests.get("https://gigazine.net/")
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        news_raw = soup.select("section h2 a")
        for news in news_raw:
            content_url = news.get("href")
            title = news.get("title")
            news_hash = hashlib.sha1((content_url + title).encode('utf-8')).hexdigest()
            fetched_news_header.append(NewsHeader(content_url, title, news_hash))
        return fetched_news_header

    def fetch_specific_news_content(self, news_header: NewsHeader) -> str:
        res = requests.get(news_header.content_url)
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        content = soup.select_one("#article .cntimage")
        for br in content.select("br"):
            br.replace_with("\n")
        return "\n".join(filter(lambda x: x, content.get_text().split("\n")))
