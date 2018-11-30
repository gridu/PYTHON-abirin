"""
Main file for running the project
"""

from scrapy.crawler import CrawlerProcess
from scrapper import Scrapper
from crawler import Crawler
import json

storage_name = 'articles.txt'


def run(runner):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(runner)
    process.start()  # the script will block here until the crawling is finished


def read_new(_authors, _articles):
    authors, articles = read()
    last_article = articles[-1]
    # last_index = _articles.index[last_article]

    last_index = 0
    index = 0
    while index < len(_articles):
        article = _articles[index]
        if article == last_article:
            last_index = index
            break
        index += 1

    if last_index + 1 == len(_articles):
        print('no new articles')
        return authors, articles

    return _authors, _articles


def crawl():
    crawler = Crawler()
    run(crawler)
    authors, articles = read_new(crawler.get_authors(), crawler.get_articles())
    save(authors, articles)


def scrap():
    run(Scrapper)


def save(authors, articles):
    with open(storage_name, 'w') as f:
        f.write(json.dumps({'authors': authors, 'articles': articles}, indent=2))


def read():
    with open(storage_name, 'r') as f:
        data = json.loads(f.read())

    return data['authors'], data['articles']


if __name__ == "__main__":
    crawl()
