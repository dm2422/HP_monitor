import json
import os
from sys import argv

from const_settings import HISTORY_JSON_PATH, TOKENS_JSON_PATH

if __name__ == "__main__":
    if "init" in argv:
        if not os.path.exists(TOKENS_JSON_PATH):
            with open(TOKENS_JSON_PATH, "w", encoding="utf-8") as wf:
                json.dump({"shared": {}}, wf, indent=2, ensure_ascii=False)
        if "history" in argv:
            from shortcuts import check_update

            with open(HISTORY_JSON_PATH, "w", encoding="utf-8") as wf:
                json.dump({}, wf, indent=2, ensure_ascii=False)
            check_update()
