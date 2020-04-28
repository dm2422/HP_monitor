import os
from sys import argv

from const_settings import HISTORY_JSON_PATH, TOKENS_JSON_PATH
from utils import save_json_default

if __name__ == "__main__":
    if "init" in argv:
        if not os.path.exists(TOKENS_JSON_PATH):
            save_json_default({}, TOKENS_JSON_PATH)
        if "history" in argv:
            from shortcuts import check_update

            save_json_default({}, HISTORY_JSON_PATH)
            check_update()
