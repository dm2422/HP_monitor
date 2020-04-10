from crawlers.common import CrawlerBase
from crawlers.schools.utsunomiya import Utsunomiya
from typing import Type, List

HISTORY_JSON_PATH = "history.json"

MESSAGE_TEMPLATE = \
    '''{name}のホームページが更新されました。

    {title}

    {content}

    記事のURLはこちらです。
    {url}'''

CRAWLER_CLASSES: List[Type[CrawlerBase]] = [
    Utsunomiya
]

CHANNEL_TOKEN = "Bearer A826gnrm/xC5fRqoU4e68jq7QTUiFEs9hIgzgfBvn3EXllJvTwbs6guCg/zfhiLvDi/Ry" \
                "+22GepsEx8zYCh5LdCXOlDYHCWsJpm+1qJTCzQ+HSSMuyBhsuZNjhsUTKcEEBhE2MLXZlW2M+djdOat2gdB04t89/1O" \
                "/w1cDnyilFU= "
