# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = tokens_from_dict(json.loads(json_string))

from dataclasses import dataclass
from enum import Enum
from typing import Any, Union, Dict, TypeVar, Type, cast, Callable

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return {k: f(v) for (k, v) in x.items()}


@dataclass
class Line:
    """LINEのアクセストークンです。指定しなかった場合配信は行われません。"""
    channel_token: str

    @staticmethod
    def from_dict(obj: Any) -> 'Line':
        assert isinstance(obj, dict)
        channel_token = from_str(obj.get("channel_token"))
        return Line(channel_token)

    def to_dict(self) -> dict:
        result: dict = {"channel_token": from_str(self.channel_token)}
        return result


class TokenOptionsEnum(Enum):
    USE_SHARED = "use_shared"


@dataclass
class Twitter:
    """Twitterのアクセストークンです。指定しなかった場合配信は行われません。"""
    access_token: str
    access_token_secret: str
    consumer_key: str
    consumer_secret: str

    @staticmethod
    def from_dict(obj: Any) -> 'Twitter':
        assert isinstance(obj, dict)
        access_token = from_str(obj.get("access_token"))
        access_token_secret = from_str(obj.get("access_token_secret"))
        consumer_key = from_str(obj.get("consumer_key"))
        consumer_secret = from_str(obj.get("consumer_secret"))
        return Twitter(access_token, access_token_secret, consumer_key, consumer_secret)

    def to_dict(self) -> dict:
        result: dict = {"access_token": from_str(self.access_token),
                        "access_token_secret": from_str(self.access_token_secret),
                        "consumer_key": from_str(self.consumer_key), "consumer_secret": from_str(self.consumer_secret)}
        return result


@dataclass
class TokenSet:
    """
    一つの学校のトークンをまとめたものです。各サービスのトークンはすべてここに入ります。
    """
    line: Union[Line, TokenOptionsEnum, None]
    twitter: Union[Twitter, TokenOptionsEnum, None]

    @staticmethod
    def from_dict(obj: Any) -> 'TokenSet':
        assert isinstance(obj, dict)
        line = from_union([Line.from_dict, from_none, TokenOptionsEnum], obj.get("line"))
        twitter = from_union([Twitter.from_dict, from_none, TokenOptionsEnum], obj.get("twitter"))
        return TokenSet(line, twitter)

    def to_dict(self) -> dict:
        result: dict = {
            "line": from_union([lambda x: to_class(Line, x), from_none, lambda x: to_enum(TokenOptionsEnum, x)],
                               self.line),
            "twitter": from_union([lambda x: to_class(Twitter, x), from_none, lambda x: to_enum(TokenOptionsEnum, x)],
                                  self.twitter)}
        return result


Tokens = Dict[str, TokenSet]


def tokens_from_dict(s: Any) -> Tokens:
    """
    辞書型からTokensを生成します。TokensとはDict[学校名, TokenSet]のことです。
    :param s: Target dictionary
    :return:
    """
    return from_dict(TokenSet.from_dict, s)


def tokens_to_dict(x: Dict[str, TokenSet]) -> Any:
    return from_dict(lambda x: to_class(TokenSet, x), x)
