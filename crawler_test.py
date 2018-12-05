from storage import read_new, change_storage
import unittest
from crawler import Crawler
from scrapy.crawler import CrawlerProcess
import os

file_name = 'test_storage.txt'


class CrawlerTest(unittest.TestCase):

    def test_crawler(self):
        self.prepare_storage()
        crawler = Crawler()

        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            # 'LOG_LEVEL': 'DEBUG'
        })

        process.crawl(crawler)
        process.start()

        authors, articles = read_new(crawler.get_authors(), crawler.get_articles())
        self.assertTrue(len(authors) > 20)
        self.assertTrue(len(articles) > 20)

    def prepare_storage(self):
        if os.path.exists(file_name):
            os.remove(file_name)
        change_storage(file_name)


if __name__ == '__main__':
    unittest.main()
