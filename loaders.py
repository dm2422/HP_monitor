import glob
import importlib
import inspect
import json
import os
from typing import List, Type, Dict

from API.structs import coordinate_from_dict, CoordinateValue
from const_settings import TOKENS_JSON_PATH
from crawlers import schools
from crawlers.common import CrawlerBase


def get_all_crawler_classes() -> List[Type[CrawlerBase]]:
    ret: List[Type[CrawlerBase]] = []
    for e in glob.glob(os.path.join(schools.__path__[0], "*.py")):
        if "__init__" in e:
            continue
        e = e.replace("\\", "/")
        module_name: str = e[e.rfind("/") + 1: -3]
        crawler_module = importlib.import_module(f"crawlers.schools.{module_name}")

        clazz: type
        for clazz in map(lambda x: x[1], inspect.getmembers(crawler_module, inspect.isclass)):
            if CrawlerBase in clazz.__bases__:
                clazz: Type[CrawlerBase]
                ret.append(clazz)
    return ret
