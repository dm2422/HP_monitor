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
from typing import List, Type, Optional, Callable, cast

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


def initialize_logger() -> None:
    import logging
    logging.basicConfig(
        level=logging.DEBUG if __debug__ else logging.INFO,
        format="%(asctime)s | %(levelname)s:%(name)s:%(message)s"
    )
    logging.debug("The logger has been initialized.")


def validate_history(path=HISTORY_JSON_PATH) -> None:
    """
    Validate history.json. Raise ValueError if there is no caches.
    :param path: Path to history.json
    :return: None
    :raises ValueError
    """
    with open(path, "r", encoding="utf-8") as rf:
        history: History = json.load(rf)
    for caches in history.values():
        if len(caches) == 0:
            raise ValueError("A suspicious history has been detected.")
