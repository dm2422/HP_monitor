import requests
import bs4
import json
import hashlib
from typing import List, Dict


UTAKA_URL = "http://www.tochigi-edu.ed.jp/utsunomiya/nc2/"


def broadcast(content: str) -> None:
    api_url = "https://api.line.me/v2/bot/message/broadcast"

    payload = {
        "messages": [
            {
                "type": "text",
                "text": content
            }
        ]
    }
    headers = {
        'Authorization': 'Bearer A826gnrm/xC5fRqoU4e68jq7QTUiFEs9hIgzgfBvn3EXllJvTwbs6guCg/zfhiLvDi \
            /Ry+22GepsEx8zYCh5LdCXOlDYHCWsJpm+1qJTCzQ+HSSMuyBhsuZNjhsUTKcEEBhE2MLXZlW2M+djdOat2gdB04t89/1O/w1cDnyilFU=',
        'Content-Type': 'application/json'
    }

    requests.post(api_url, headers=headers, json=payload)


def getNews() -> List[Dict]:
    news: List[Dict] = []

    with open("history.json", "r") as rf:
        history = json.load(rf)

    res = requests.get(UTAKA_URL)
    soup = bs4.BeautifulSoup(res.text, features="html.parser")
    news_raw: bs4.ResultSet = soup.select_one(
        "#whatsnew_contents_13").table.find_all("tr")
    for i in range(0, len(news_raw), 2):
        title, _ = news_raw[i: i + 2]
        title_header: str = title.find_all("td")[0].a.text
        page_url: str = title.find_all("td")[0].a.get("href")
        title_date: str = title.find_all("td")[1].text
        hash_id = hashlib.sha1(
            (title_header + title_date).encode()).hexdigest()
        if not hash_id in history["hashes"]:
            history["hashes"].append(hash_id)
            news.append({
                "title": title_header,
                "url": page_url
            })
    with open("history.json", "w") as wf:
        json.dump(history, wf, indent=4)
    return news


def getNewsDetail(page_url: str) -> str:
    res = requests.get(page_url)
    soup = bs4.BeautifulSoup(res.text, features="html.parser")
    detail_raw = soup.select_one(".journal_content")
    detail_raw.br.replace_with("\n")
    return detail_raw.get_text()
