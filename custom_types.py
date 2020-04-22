from dataclasses import dataclass
from typing import Dict, Union, Optional

TokenDict = Dict[str, str]

ApiTokens = Optional[Union[TokenDict, str]]

TokenSet = Dict[str, ApiTokens]

TokenTable = Dict[str, TokenSet]


@dataclass
class NewsHeader:
    content_url: str
    title: str
    hash: str


@dataclass
class News(NewsHeader):
    site_name: str
    content: str


class Singleton(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance
