import json
import os
import random
import unittest

from faker import Faker

from API.structs import TokenOptionsEnum
from const_settings import HISTORY_JSON_PATH, TOKENS_JSON_PATH
from loaders import load_tokens
from settings import API_AGENT_CLASSES

fake = Faker("ja-JP")


def generate_fake_twitter_tokens():
    return {
        "consumer_key": fake.password(25),
        "consumer_secret": fake.password(50),
        "access_token": fake.password(50),
        "access_token_secret": fake.password(45)
    }


def generate_fake_line_tokens():
    return {
        "channel_token": fake.password(172)
    }


class FileLoader(unittest.TestCase):
    """
    NOTE:
        These tests depend on some specific outer files.
        So need run in root directory (working dir: HP_monitor/)
    """
    TEST_TOKENS_JSON_PATH = "test_tokens.json"

    def setUp(self) -> None:
        test_tokens = {
            "shared": {
                "twitter": generate_fake_twitter_tokens(),
                "line": generate_fake_line_tokens()
            }
        }
        for _ in range(50):
            test_tokens[fake.company()] = {
                "twitter": random.choice([None, "use_shared", generate_fake_twitter_tokens()]),
                "line": random.choice([None, "use_shared", generate_fake_line_tokens()])
            }
        with open(self.TEST_TOKENS_JSON_PATH, "w", encoding="utf-8") as wf:
            json.dump(test_tokens, wf, indent=4, ensure_ascii=False)

    def tearDown(self) -> None:
        os.remove(self.TEST_TOKENS_JSON_PATH)

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

    def test_tokens_loader(self):
        test_tokens = load_tokens(self.TEST_TOKENS_JSON_PATH)
        shared_tokens = test_tokens["shared"]

        for clazz in API_AGENT_CLASSES:
            for school_name, tokens_set in test_tokens.items():
                if getattr(tokens_set, clazz.KEY_NAME) == TokenOptionsEnum.USE_SHARED:
                    self.assertEqual(clazz().get_tokens(school_name, test_tokens),
                                     getattr(shared_tokens, clazz.KEY_NAME))
                elif getattr(tokens_set, clazz.KEY_NAME) is None:
                    self.assertIsNone(clazz().get_tokens(school_name, test_tokens))
