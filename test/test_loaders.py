import json
import os
import random
import unittest
from typing import Type

from faker import Faker

from API.common import get_all_api_classes, APIBase
from const_settings import HISTORY_JSON_PATH, TOKENS_JSON_PATH
from settings import load_tokens

fake = Faker("ja-JP")


class FileLoader(unittest.TestCase):
    """
    NOTE:
        These tests depend on some specific outer files.
        So need run in root directory (working dir: HP_monitor/)
    """
    TEST_TOKENS_JSON_PATH = "test_tokens.json"

    def setUp(self) -> None:
        test_tokens = {"shared": {}}
        for clazz in random.choices(get_all_api_classes()):
            clazz: Type[APIBase]
            test_tokens["shared"][clazz.JSON_KEY] = clazz().generate_fake_tokens(fake)
        for _ in range(50):
            test_tokens[fake.company()] = {}
            for clazz in random.choices(get_all_api_classes()):
                clazz: Type[APIBase]
                test_tokens["shared"][clazz.JSON_KEY] = \
                    random.choice([None, "use_shared", clazz().generate_fake_tokens(fake)])
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

        for clazz in get_all_api_classes():
            for site_name, tokens_set in test_tokens.items():
                agent_tokens = tokens_set.get(clazz.JSON_KEY, None)
                if agent_tokens == "use_shared":
                    self.assertEqual(clazz().get_agent_tokens(site_name, test_tokens),
                                     shared_tokens[clazz.JSON_KEY])
                elif agent_tokens is None:
                    self.assertIsNone(clazz().get_agent_tokens(site_name, test_tokens))
