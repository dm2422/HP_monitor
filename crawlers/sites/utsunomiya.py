import hashlib
from typing import List
from crawlers.common import CrawlerBase, NewsHeader
import bs4
import requests


class Utsunomiya(CrawlerBase):
    HP_URL = "http://www.tochigi-edu.ed.jp/utsunomiya/nc2/"
    SITE_NAME = "宇都宮高校"

    def fetch_recent_news_headers(self) -> List[NewsHeader]:
        fetched_news_header: List[NewsHeader] = []
        res = requests.get(self.HP_URL)
        soup = bs4.BeautifulSoup(res.text, features="html.parser")
        news_raw: bs4.ResultSet = soup.select_one("#whatsnew_contents_13").table.find_all("tr")
        for i in range(0, len(news_raw), 2):
            title, _ = news_raw[i: i + 2]
            title_header: str = title.find_all("td")[0].a.text
            origin_url: str = title.find_all("td")[0].a.get("href")
            title_date: str = title.find_all("td")[1].text
            news_hash = hashlib.sha1((title_header + title_date).encode()).hexdigest()
            fetched_news_header.append(NewsHeader(origin_url, title_header, news_hash))
        return fetched_news_header

    def fetch_specific_news_content(self, news_header: NewsHeader) -> str:
        res = requests.get(news_header.origin_url)
        soup = bs4.BeautifulSoup(res.text, features="html.parser")
        detail_raw = soup.select_one(".journal_content")
        detail_raw.br.replace_with("\n")
        return detail_raw.get_text()
