import hashlib
from typing import List

import bs4
import requests

from crawlers.common import CrawlerBase
from custom_types import NewsHeader


class UtsunomiyaJoshi(CrawlerBase):
    HP_URL = "http://www.tochigi-edu.ed.jp/utsunomiyajoshi/nc2/"
    SITE_NAME = "宇都宮女子高校"

    def fetch_recent_news_headers(self) -> List[NewsHeader]:
        fetched_news_header: List[NewsHeader] = []
        res = requests.get(self.HP_URL)
        soup = bs4.BeautifulSoup(res.text, features="html.parser")
        news_date_raw = soup.select("#_theme_top_239 .outerdiv .outerdiv .journal_list_date")
        news_title_raw = soup.select("#_theme_top_239 .outerdiv .outerdiv .journal_list_title")
        for date, title_header in zip(news_date_raw, news_title_raw):
            posted_at = date.text
            content_url = title_header.h4.a.get("href")
            title = title_header.h4.a.text
            news_hash: str = hashlib.sha1(((title + posted_at).encode())).hexdigest()
            fetched_news_header.append(NewsHeader(content_url, title, news_hash))
        return fetched_news_header

    def fetch_specific_news_content(self, news_header: NewsHeader) -> str:
        res = requests.get(news_header.content_url)
        soup = bs4.BeautifulSoup(res.text, features="html.parser")
        detail_raw = soup.select_one(".journal_content")
        for i in detail_raw.select("br"):
            i.replace_with("\n")
        return detail_raw.get_text().strip()
