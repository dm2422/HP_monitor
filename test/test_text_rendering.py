import unittest

from faker import Faker

from crawlers.common import News
from API.agents.twitter import render_twitter_text

fake = Faker("ja-JP")


class TwitterRenderingTest(unittest.TestCase):

    def test_not_round_max_len(self):
        news = News(
            title=fake.company(),
            content_url=fake.uri(),
            hash=fake.sha1(),
            content=fake.text(10)
        )
        rendered_text = render_twitter_text(
            news=news,
            site_name=fake.company()
        )
        self.assertLessEqual(len(rendered_text), 140)

    def test_round_max_len(self):
        fake_uri = fake.uri() + fake.uri_path(20)
        news = News(
            title=fake.company(),
            content_url=fake_uri,
            hash=fake.sha1(),
            content=fake.text(200)
        )
        rendered_text = render_twitter_text(
            news=news,
            site_name=fake.company()
        )
        self.assertLessEqual(len(rendered_text) - (len(fake_uri) - 24), 140)
