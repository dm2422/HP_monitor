import random
import unittest
from typing import List, Type

from faker import Faker

from API.common import APIBase, get_all_api_classes

fake = Faker("ja-JP")


class Agents(unittest.TestCase):

    def test_tokens(self):
        fake_token_table = {}
        fake_site_names = [fake.company() for _ in range(200)]
        agent_classes = get_all_api_classes()

        for index, site in enumerate(fake_site_names):
            fake_token_set = {}
            fake_using_agent_classes: List[Type[APIBase]] = \
                random.sample(agent_classes, random.randint(0, len(agent_classes)))
            for clazz in fake_using_agent_classes:
                choices = [None, clazz.generate_fake_api_tokens(fake)]
                if index > 0:
                    choices.append(f"use_{random.choice(fake_site_names[:index])}")
                fake_token = random.choice(choices)
                fake_token_set[clazz.JSON_KEY] = fake_token
            fake_token_table[site] = fake_token_set

        for clazz in get_all_api_classes():
            for site_name, tokens_set in fake_token_table.items():
                clazz().get_api_tokens(site_name, fake_token_table)

    def test_raise_circular_reference_error(self):
        fake_token_table = {
            "A": {clazz.JSON_KEY: "use_B" for clazz in get_all_api_classes()},
            "B": {clazz.JSON_KEY: "use_A" for clazz in get_all_api_classes()}
        }
        with self.assertRaises(ValueError):
            for clazz in get_all_api_classes():
                for site_name, tokens_set in fake_token_table.items():
                    clazz().get_api_tokens(site_name, fake_token_table)

    def test_raise_not_existing_token_reference_error(self):
        fake_token_table = {
            "A": {clazz.JSON_KEY: "use_B" for clazz in get_all_api_classes()}
        }
        with self.assertRaises(ValueError):
            for clazz in get_all_api_classes():
                for site_name, tokens_set in fake_token_table.items():
                    clazz().get_api_tokens(site_name, fake_token_table)


if __name__ == '__main__':
    unittest.main()
