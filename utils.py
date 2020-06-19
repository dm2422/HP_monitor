"""
This module should not depend on anything other than standard modules.
このモジュールは、標準モジュール以外に依存してはいけません。
"""
import functools
import importlib
import inspect
import json
import pkgutil
from collections import deque
from itertools import accumulate
from logging import getLogger
from typing import List, Type, Optional, Callable, cast, TextIO

import jaconv

from const_settings import HISTORY_JSON_PATH
from custom_types import History


def get_all_classes_from_package(pkg_path: str, filter_func: Optional[Callable[[Type], bool]] = None) -> List[Type]:
    ret = deque()
    module = importlib.import_module(pkg_path)
    for info in pkgutil.iter_modules(module.__path__, f"{module.__name__}."):
        if info.ispkg:
            ret += get_all_classes_from_package(info.name, filter_func)
            continue

        child_module = importlib.import_module(info.name)
        for clazz in (x[1] for x in inspect.getmembers(child_module, inspect.isclass)):
            if filter_func and not filter_func(clazz):
                continue
            ret.append(clazz)
    return list(ret)


pretty_text = cast(
    Callable[[str], str],
    functools.partial(jaconv.zen2han, digit=True, ascii=True, kana=False)
)

open_utf_8 = functools.partial(open, encoding="utf-8")
r_open_utf_8 = cast(Callable[[str], TextIO], functools.partial(open_utf_8, mode="r"))
w_open_utf_8 = cast(Callable[[str], TextIO], functools.partial(open_utf_8, mode="w"))


def load_json_default(path: str) -> object:
    with r_open_utf_8(path) as rf:
        loaded = json.load(rf)
    return loaded


def save_json_default(obj: object, path: str) -> None:
    with w_open_utf_8(path) as wf:
        json.dump(obj, wf, ensure_ascii=False, indent=2)


def initialize_logger() -> None:
    import logging
    logging.basicConfig(
        level=logging.DEBUG if __debug__ else logging.INFO,
        format="%(asctime)s | %(levelname)s:%(name)s:%(message)s"
    )


def load_history(path=HISTORY_JSON_PATH) -> History:
    logger = getLogger(load_history.__qualname__)
    history = cast(History, load_json_default(path))
    for caches in history.values():
        if len(caches) == 0:
            raise ValueError("A suspicious history has been detected.")
    logger.debug(f"'{HISTORY_JSON_PATH}' has loaded successfully!")
    return history


def save_history(obj: History, path=HISTORY_JSON_PATH) -> None:
    logger = getLogger(save_history.__qualname__)
    save_json_default(obj, path)
    logger.debug(f"'{HISTORY_JSON_PATH}' has saved successfully!")


def wrap_one_arg(func: Callable) -> Callable:
    def inner(p):
        return func(*p)

    return inner


def str_clamp(value: str, max_length: int) -> str:
    return value if len(value) <= max_length else value[:max_length - 3] + "..."


def str_clamp_bytes(value: str, max_bytes: int) -> str:
    byte_count = list(map(lambda s: len(s.encode('utf-8')), value))
    try:
        end_slice = next(i for i, v in enumerate(accumulate(byte_count)) if v > max_bytes)
    except StopIteration:
        return value
    return value[:end_slice - 3] + "..."
