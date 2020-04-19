import glob
import importlib
import inspect
import os
from abc import ABCMeta, abstractmethod
from functools import lru_cache
from logging import getLogger
from typing import Callable, List, Type, Dict, Optional

from faker import Faker

from API import agents
from crawlers.common import News
from settings import TOKEN_TABLE

AgentTokens = Dict[str, str]


class APIBase(metaclass=ABCMeta):
    LOGGING_NAME: str
    JSON_KEY: str
    SHARED_NAME = "shared"

    def __init__(self):
        self.logger = getLogger(self.LOGGING_NAME)

    def get_agent_tokens(self, school_name: str, token_table=TOKEN_TABLE) -> Optional[AgentTokens]:
        """
        指定した学校名のトークンを取得します。取得するトークンはこのクラスのエージェントのトークンのみです。
        戻り値は辞書型としてアクセスすることができます。
        (例)
        [json]
        "some_service": {
            "bot_token": "abc",
            "bot_token_secret": "123"
        }
        [python]
        self.get_agent_tokens()["bot_token"]
        >> "abc"
        self.get_agent_tokens()["bot_token_secret"]
        >> "123"
        :param school_name: 学校名
        :param token_table: [デバッグ用]使用するトークンテーブルを指定します。
        :return:トークンのdataclassです。トークンが無い場合はNoneです。
        """
        agent_tokens = token_table[school_name].get(self.JSON_KEY, None)
        if agent_tokens == "use_shared":
            agent_tokens = token_table[self.SHARED_NAME].get(self.JSON_KEY, None)

        return agent_tokens

    @abstractmethod
    def broadcast_prod(self, news: News, school_name: str) -> None:
        pass

    def broadcast_debug(self, news: News, school_name: str) -> None:
        self.logger.debug(f"A broadcast has occurred. {self.get_agent_tokens(school_name)=}, {school_name=}, {news=}")

    def get_broadcast_func(self) -> Callable[[News, str], None]:
        return self.broadcast_debug if __debug__ else self.broadcast_prod

    def broadcast(self, news: News, school_name: str):
        self.logger.info("Start broadcast...")
        self.get_broadcast_func()(news, school_name)
        self.logger.info("Finish broadcast.")

    @classmethod
    def generate_fake_tokens(cls, fake: Faker) -> Dict[str, str]:
        return {
            "bot_token": fake.password(8)
        }


@lru_cache
def get_all_api_classes() -> List[Type[APIBase]]:
    logger = getLogger(__name__)
    ret: List[Type[APIBase]] = []
    for e in glob.glob(os.path.join(agents.__path__[0], "*.py")):
        if "__init__" in e:
            continue
        e = e.replace("\\", "/")
        module_name: str = e[e.rfind("/") + 1: -3]
        crawler_module = importlib.import_module(f"API.agents.{module_name}")

        clazz: type
        for clazz in map(lambda x: x[1], inspect.getmembers(crawler_module, inspect.isclass)):
            if APIBase in clazz.__bases__:
                clazz: Type[APIBase]
                ret.append(clazz)
                logger.debug(f"An API agent has installed! - {clazz}")
    return ret
