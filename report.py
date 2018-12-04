"""
Main file for running the project
"""

from scrapy.crawler import CrawlerProcess
from crawler import Crawler
import logging
from storage import read_new, save
from visualizer import visualize

logger = logging.getLogger('report')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.addHandler(ch)


def run(runnable):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        # 'LOG_LEVEL': 'DEBUG'
    })

    process.crawl(runnable)
    process.start()  # the script will block here until the crawling is finished


def crawl():
    crawler = Crawler()
    run(crawler)
    authors, articles = read_new(crawler.get_authors(), crawler.get_articles())
    save(authors, articles)
    visualize(authors, articles)


if __name__ == "__main__":
    crawl()
