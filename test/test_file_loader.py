import json
import unittest

from settings import HISTORY_JSON_PATH, TOKENS_JSON_PATH


class FileLoader(unittest.TestCase):
    """
    NOTE:
        These tests depend on some specific outer files.
        So need run in root directory (working dir: HP_monitor/)
    """

    def test_can_load_history(self):
        with open(HISTORY_JSON_PATH, "r", encoding="utf-8") as rf:
            history = json.load(rf)
        self.assertIsNotNone(history)
        self.assertIsInstance(history, dict)

    def test_can_load_tokens(self):
        with open(TOKENS_JSON_PATH, "r", encoding="utf-8") as rf:
            tokens = json.load(rf)
        self.assertIsNotNone(tokens)
        self.assertIsInstance(tokens, dict)
