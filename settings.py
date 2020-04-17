from typing import Type, List

from crawlers.common import CrawlerBase
from importutil import get_all_crawler_classes

HISTORY_JSON_PATH = "history.json"

TOKENS_JSON_PATH = "tokens.json"

MESSAGE_TEMPLATE = '''{name}のホームページが更新されました。

{title}

{content}

記事のURLはこちらです。
{url}'''

CRAWLER_CLASSES: List[Type[CrawlerBase]] = get_all_crawler_classes()
