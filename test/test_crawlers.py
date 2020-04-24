import unittest

from crawlers.common import get_all_crawler_classes


class Crawlers(unittest.TestCase):

    def test_crawlers(self):
        for clazz in get_all_crawler_classes():
            crawler = clazz()
            header = crawler.fetch_recent_news_headers()[0]
            self.assertIsNotNone(header)
            self.assertIsNotNone(crawler.fetch_specific_news_content(header))


if __name__ == '__main__':
    unittest.main()
