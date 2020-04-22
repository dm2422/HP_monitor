import json
from functools import lru_cache

import custom_types
from const_settings import TOKENS_JSON_PATH


@lru_cache
def load_token_table(tokens_json_path=TOKENS_JSON_PATH) -> custom_types.TokenTable:
    """
    Load tokens from TOKENS_JSON_PATH.
    :param tokens_json_path: The path to the JSON thad the tokens are written.
    :return: Dict[site_name: str, tokens_set: TokensSet]
    """
    with open(tokens_json_path, "r", encoding="utf-8") as rf:
        tokens_ = json.load(rf)

    return tokens_


TOKEN_TABLE = load_token_table()
