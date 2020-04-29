import argparse
import time
from typing import Callable, Dict

from const_settings import HISTORY_JSON_PATH
from utils import save_json_default

ACTION_TO_FUNC: Dict[str, Callable] = {}


def command_action(command_name: str) -> Callable[[Callable], Callable]:
    def annotation(func: Callable) -> Callable:
        ACTION_TO_FUNC[command_name] = func
        return func

    return annotation


@command_action("init")
def init():
    from shortcuts import check_update
    save_json_default({}, HISTORY_JSON_PATH)
    news = check_update()
    print(f"{len(news)} news were cached.")
    for n in news:
        print(f"{n.site_name}:{n.hash[:8]}:{n.title}")


@command_action("agents")
def agents():
    from API.common import get_all_api_classes
    classes = get_all_api_classes()
    print(f"There are {len(classes)} agents are available!")
    for clazz in classes:
        print(f"{clazz.JSON_KEY}: logging as {clazz.LOGGING_NAME}")


@command_action("sites")
def sites():
    from crawlers.common import get_all_crawler_classes
    classes = get_all_crawler_classes()
    print(f"There are {len(classes)} sites are available!")
    for clazz in classes:
        print(f"{clazz.SITE_NAME}: Refer to {clazz.HP_URL}")


@command_action("history")
def history():
    from utils import load_history
    cached_history = load_history()
    print(f"There are {len(cached_history)} sites.")
    for site, cache in cached_history.items():
        print(f"{site} has {len(cache)} history.")


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Manage this monitor.")
    parser.add_argument("action", choices=ACTION_TO_FUNC.keys())
    command_args = parser.parse_args()

    start_time = time.time()
    ACTION_TO_FUNC[command_args.action]()
    elapsed = time.time() - start_time

    print(f"The command: {repr(command_args.action)} has finished in {round(elapsed, 2)} seconds.")
