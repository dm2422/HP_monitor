import logging
from abc import ABCMeta, abstractmethod
from typing import Callable

from API.structs import TokenOptionsEnum
from crawlers.common import News
from settings import TOKENS


class APIBase(metaclass=ABCMeta):
    API_NAME: str
    TOKEN_CLASS: type

    def __init__(self):
        self.logger = logging.getLogger(self.API_NAME)

    def get_tokens(self, tokens=TOKENS):
        api_tokens = getattr(tokens[self.API_NAME], self.API_NAME)
        if api_tokens == TokenOptionsEnum.USE_SHARED:
            api_tokens = getattr(tokens["shared"], self.API_NAME)

        assert not isinstance(api_tokens, TokenOptionsEnum)
        return api_tokens

    @abstractmethod
    def broadcast_prod(self, news: News, school_name: str) -> None:
        pass

    def broadcast_debug(self, news: News, school_name: str) -> None:
        self.logger.debug(f"A broadcast has occurred. {school_name=}, {news=}")

    def get_broadcast_func(self) -> Callable[[News, str], None]:
        return self.broadcast_debug if __debug__ else self.broadcast_prod

    def broadcast(self, news: News, school_name: str):
        self.get_broadcast_func()(news, school_name)
