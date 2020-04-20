from abc import ABCMeta, abstractmethod
from functools import lru_cache
from logging import getLogger
from typing import Callable, List, Type, Dict, Optional, cast

from faker import Faker

from utils import get_all_classes_from_package
from crawlers.common import News
from settings import TOKEN_TABLE


class APIBase(metaclass=ABCMeta):
    LOGGING_NAME: str
    JSON_KEY: str
    SHARED_NAME = "shared"

    def __init__(self):
        self.logger = getLogger(self.LOGGING_NAME)

    def get_agent_tokens(self, site_name: str, token_table=TOKEN_TABLE) -> Optional[Dict[str, str]]:
        """
        指定したサイト名のトークンを取得します。取得するトークンはこのクラスのエージェントのトークンのみです。
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
        :param site_name: サイト名
        :param token_table: [デバッグ用]使用するトークンテーブルを指定します。
        :return:トークンのdataclassです。トークンが無い場合はNoneです。
        """
        agent_tokens = token_table[site_name].get(self.JSON_KEY, None)
        if agent_tokens == "use_shared":
            agent_tokens = token_table[self.SHARED_NAME].get(self.JSON_KEY, None)

        return agent_tokens

    @abstractmethod
    def broadcast_prod(self, news: News, site_name: str) -> None:
        pass

    def broadcast_debug(self, news: News, site_name: str) -> None:
        self.logger.debug(f"A broadcast has occurred. {self.get_agent_tokens(site_name)=}, {site_name=}, {news=}")

    def get_broadcast_func(self) -> Callable[[News, str], None]:
        return self.broadcast_debug if __debug__ else self.broadcast_prod

    def broadcast(self, news: News, site_name: str):
        self.logger.info("Start broadcast...")
        self.get_broadcast_func()(news, site_name)
        self.logger.info("Finish broadcast.")

    @classmethod
    def generate_fake_tokens(cls, fake: Faker) -> Dict[str, str]:
        """
        このメソッドは単体テストのために使用されます。
        :param fake:テスト用のトークンを生成するための、Fakerインスタンスです。
        :return:生成したテスト用トークンです。JSONと構造を一致させる必要があります。
        """
        return {
            "bot_token": fake.password(8)
        }


@lru_cache
def get_all_api_classes() -> List[Type[APIBase]]:
    import API
    import API.agents
    return cast(List[Type[APIBase]], get_all_classes_from_package(
        API.agents.__name__,
        lambda c: API.common.APIBase in c.__bases__
    ))
