import json
from functools import lru_cache

from API.structs import tokens_from_dict, Tokens
from const_settings import TOKENS_JSON_PATH


@lru_cache
def load_tokens(tokens_json_path=TOKENS_JSON_PATH) -> Tokens:
    """
    Load tokens from TOKENS_JSON_PATH.
    :param tokens_json_path: The path to the JSON thad the tokens are written.
    :return: Dict[school_name: str, tokens_set: TokensSet]
    """
    with open(tokens_json_path, "r", encoding="utf-8") as rf:
        tokens_ = json.load(rf)

    return tokens_from_dict(tokens_)
