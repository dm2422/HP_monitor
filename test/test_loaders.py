import unittest

from faker import Faker

from const_settings import HISTORY_JSON_PATH, TOKENS_JSON_PATH
from utils import load_json_default

fake = Faker("ja-JP")


class FileLoader(unittest.TestCase):
    """
    NOTE:
        These tests depend on some specific outer files.
        So need run in root directory (working dir: HP_monitor/)
    """

    def test_can_load_history(self):
        history = load_json_default(HISTORY_JSON_PATH)
        self.assertIsNotNone(history)
        self.assertIsInstance(history, dict)

    def test_can_load_tokens(self):
        tokens = load_json_default(TOKENS_JSON_PATH)
        self.assertIsNotNone(tokens)
        self.assertIsInstance(tokens, dict)
