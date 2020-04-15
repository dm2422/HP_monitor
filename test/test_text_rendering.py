import unittest

from faker import Faker

from crawlers.common import News
from utils import render_twitter_text

fake = Faker("ja-JP")


class TwitterRenderingTest(unittest.TestCase):

    def test_not_round_max_len(self):
        news = News(
            title=fake.company(),
            origin_url=fake.uri(),
            hash=fake.sha1(),
            content=fake.text(10)
        )
        rendered_text = render_twitter_text(
            news=news,
            school_name=fake.company()
        )
        self.assertLessEqual(len(rendered_text), 140)

    def test_round_max_len(self):
        news = News(
            title=fake.company(),
            origin_url=fake.uri(),
            hash=fake.sha1(),
            content=fake.text(200)
        )
        rendered_text = render_twitter_text(
            news=news,
            school_name=fake.company()
        )
        self.assertEqual(len(rendered_text), 140)
