from abc import ABCMeta, abstractmethod
from functools import lru_cache
from logging import getLogger
from typing import Callable, List, Type, cast, Optional

from faker import Faker

from custom_types import News, Singleton, TokenDict
from settings import TOKEN_TABLE
from utils import get_all_classes_from_package


class APIBase(Singleton, metaclass=ABCMeta):
    LOGGING_NAME: str
    JSON_KEY: str

    def __init__(self):
        self.logger = getLogger(self.LOGGING_NAME)

    def get_api_tokens(self, site_name: str, token_table=TOKEN_TABLE) -> Optional[TokenDict]:
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
        try:
            api_tokens = token_table[site_name].get(self.JSON_KEY)
        except KeyError:
            raise ValueError(f"'{site_name}' does not exist.")
        except RecursionError:
            raise ValueError(f"It seems that there is a circular reference at '{site_name}'.")
        if isinstance(api_tokens, str):
            if api_tokens[:3] == "use_" or len(api_tokens) < 5:
                raise ValueError(f"'{api_tokens}' is invalid for token.")
            using_site_name = api_tokens[4:]
            api_tokens = self.get_api_tokens(using_site_name, token_table)

        return api_tokens

    @abstractmethod
    def broadcast_prod(self, news: News, token: TokenDict) -> None:
        """
        本番用の配信関数です。本番環境では、こちらの関数が呼ばれます。
        :param news: 配信するべきニュースです。
        :param token: 配信に使うべきトークンです。
        :return:
        """
        pass

    def broadcast_debug(self, news: News, token: TokenDict) -> None:
        """
        テスト用の配信関数です。テスト環境では、こちらの関数が呼ばれます。
        :param news: 配信するべきニュースです。
        :param token: 配信に使うべきトークンです。
        :return:
        """
        self.logger.debug(f"A broadcast has occurred. {token=}, {news=}")

    def get_broadcast_func(self) -> Callable[[News, TokenDict], None]:
        """
        本番用とテスト用の関数を、グローバル変数`__debug__によって返します。`
        :return: 関数
        """
        return self.broadcast_debug if __debug__ else self.broadcast_prod

    def broadcast(self, news: News):
        if token := self.get_api_tokens(news.site_name):
            self.logger.info(f"Start broadcast with token: {token}")
            self.get_broadcast_func()(news, token)

    @classmethod
    def generate_fake_api_tokens(cls, fake: Faker) -> TokenDict:
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
