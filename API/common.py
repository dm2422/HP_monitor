import glob
import importlib
import inspect
import os
from abc import ABCMeta, abstractmethod
from logging import getLogger
from typing import Callable, List, Type

from API import service
from API.structs import TokenOptionsEnum
from API.tokens import TOKENS
from crawlers.common import News


class APIBase(metaclass=ABCMeta):
    API_NAME: str
    TOKEN_CLASS: type

    def __init__(self):
        self.logger = getLogger(self.API_NAME)

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


def get_all_api_classes() -> List[Type[APIBase]]:
    logger = getLogger(__name__)
    ret: List[Type[APIBase]] = []
    for e in glob.glob(os.path.join(service.__path__[0], "*.py")):
        if "__init__" in e:
            continue
        e = e.replace("\\", "/")
        module_name: str = e[e.rfind("/") + 1: -3]
        crawler_module = importlib.import_module(f"API.service.{module_name}")

        clazz: type
        for clazz in map(lambda x: x[1], inspect.getmembers(crawler_module, inspect.isclass)):
            if APIBase in clazz.__bases__:
                clazz: Type[APIBase]
                ret.append(clazz)
                logger.debug(f"An API agent has installed! - {clazz}")
    return ret
