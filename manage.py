from sys import argv

from const_settings import HISTORY_JSON_PATH, TOKENS_JSON_PATH


def init_json_file(path: str):
    with open(path, "w", encoding="utf-8") as wf:
        wf.write("{}")


def cmd_init() -> None:
    init_json_file(HISTORY_JSON_PATH)
    init_json_file(TOKENS_JSON_PATH)
    from utils import check_update
    check_update()


if __name__ == "__main__":
    if "init" in argv:
        cmd_init()
