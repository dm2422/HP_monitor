from sys import argv

from const_settings import HISTORY_JSON_PATH
from utils import check_update


def cmd_init() -> None:
    with open(HISTORY_JSON_PATH, "w", encoding="utf-8") as wf:
        wf.write("{}")
    check_update()


if __name__ == "__main__":
    if argv[0] == "init":
        cmd_init()
