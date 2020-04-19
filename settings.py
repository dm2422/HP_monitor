from typing import Type, List

from API.common import APIBase, get_all_api_classes
from crawlers.common import CrawlerBase, get_all_crawler_classes

CRAWLER_CLASSES: List[Type[CrawlerBase]] = get_all_crawler_classes()

API_AGENT_CLASSES: List[Type[APIBase]] = get_all_api_classes()
