# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = coordinate_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, Optional, Dict, TypeVar, Type, cast, Callable

T = TypeVar("T")


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


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return {k: f(v) for (k, v) in x.items()}


@dataclass
class Line:
    """LINEのアクセストークンです。"""
    channel_token: str

    @staticmethod
    def from_dict(obj: Any) -> 'Line':
        assert isinstance(obj, dict)
        channel_token = from_str(obj.get("channel_token"))
        return Line(channel_token)

    def to_dict(self) -> dict:
        result: dict = {"channel_token": from_str(self.channel_token)}
        return result


@dataclass
class Twitter:
    """Twitterのアクセストークンです。"""
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
        result: dict = {"access_token": from_union([from_str, from_none], self.access_token),
                        "access_token_secret": from_union([from_str, from_none], self.access_token_secret),
                        "consumer_key": from_union([from_str, from_none], self.consumer_key),
                        "consumer_secret": from_union([from_str, from_none], self.consumer_secret)}
        return result


@dataclass
class CoordinateValue:
    """学校名です。クラスで設定した名前と一致させる必要があります。"""
    """LINEのアクセストークンです。"""
    line: Optional[Line] = None
    """Twitterのアクセストークンです。"""
    twitter: Optional[Twitter] = None

    @staticmethod
    def from_dict(obj: Any) -> 'CoordinateValue':
        assert isinstance(obj, dict)
        line = from_union([Line.from_dict, from_none], obj.get("line"))
        twitter = from_union([Twitter.from_dict, from_none], obj.get("twitter"))
        return CoordinateValue(line, twitter)

    def to_dict(self) -> dict:
        result: dict = {"line": from_union([lambda x: to_class(Line, x), from_none], self.line),
                        "twitter": from_union([lambda x: to_class(Twitter, x), from_none], self.twitter)}
        return result


def coordinate_from_dict(s: Any) -> Dict[str, CoordinateValue]:
    return from_dict(CoordinateValue.from_dict, s)


def coordinate_to_dict(x: Dict[str, CoordinateValue]) -> Any:
    return from_dict(lambda x: to_class(CoordinateValue, x), x)
