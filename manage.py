import argparse
import logging
import sys
import time
from typing import Callable, Dict, Tuple

from const_settings import HISTORY_JSON_PATH
from utils import save_json_default

ACTION_TO_FUNC: Dict[str, Tuple[Callable, Tuple[str]]] = {}


def command_action(command_name: str, *expected_args: str) -> Callable[[Callable], Callable]:
    def annotation(func: Callable) -> Callable:
        ACTION_TO_FUNC[command_name] = (func, expected_args)
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


@command_action("run-once")
def run_once():
    from utils import initialize_logger
    from shortcuts import check_update, broadcast_all

    initialize_logger()
    for news in check_update():
        broadcast_all(news)


@command_action("monitor", "interval")
def monitor(interval: int):
    from utils import initialize_logger
    from shortcuts import check_update, broadcast_all

    initialize_logger()
    while True:
        for news in check_update():
            broadcast_all(news)
        time.sleep(interval)


def execute_command(args: argparse.Namespace) -> int:
    func_args = {}
    target_command = ACTION_TO_FUNC[args.action]
    target_func = target_command[0]
    target_func_args = target_command[1]
    for a in target_func_args:
        func_args[a] = getattr(args, a)
    return target_func(**func_args) or 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Manage this monitor.")
    parser.add_argument("action", choices=ACTION_TO_FUNC.keys())
    parser.add_argument("-d", "--debug", default=False, action="store_true", help="enable debug mode")
    parser.add_argument("-i", "--interval", default=60, help="update interval in seconds", type=int)
    commandline_args = parser.parse_args()

    if getattr(commandline_args, "debug", False):
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Debug mode is enabled!")

    start_time = time.time()
    try:
        exit_code = execute_command(commandline_args)
    except KeyboardInterrupt:
        sys.exit("Interrupted by user")
    elapsed = time.time() - start_time

    print(f"The command: {repr(commandline_args.action)} has finished "
          f"with exit code {exit_code} "
          f"in {round(elapsed, 2)} seconds.")
