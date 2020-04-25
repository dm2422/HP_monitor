from typing import cast

from const_settings import TOKENS_JSON_PATH
from custom_types import TokenTable
from utils import load_json_default

TOKEN_TABLE = cast(TokenTable, load_json_default(TOKENS_JSON_PATH))
