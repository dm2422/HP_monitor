from typing import Type, List

from crawlers.common import CrawlerBase
from loaders import get_all_crawler_classes, load_tokens

CRAWLER_CLASSES: List[Type[CrawlerBase]] = get_all_crawler_classes()

TOKENS = load_tokens()
