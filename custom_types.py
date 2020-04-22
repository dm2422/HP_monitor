from dataclasses import dataclass
from typing import Dict, Union, Optional

ApiTokens = Optional[Union[Dict[str, str], str]]

TokenSet = Dict[str, ApiTokens]

TokenTable = Dict[str, TokenSet]


@dataclass
class NewsHeader:
    content_url: str
    title: str
    hash: str


@dataclass
class News(NewsHeader):
    content: str
