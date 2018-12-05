
"""
This is the main file for scrapping grid blog website
"""

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime

main_url = 'https://blog.griddynamics.com/'
date_format = '%b %d, %Y'


class Crawler(CrawlSpider):
    """
    Inherited class crawling the grid website
    """
    name = "crawler"

    allowed_domains = ['blog.griddynamics.com']
    start_urls = [main_url]
    _articles = []
    _authors = []

    rules = (Rule(LinkExtractor(), callback='parse_page'),)

    def parse_page(self, response):
        """
        Parses the current page
        :param response: current page
        :return: void
        """
        title = response.css('#postcontent > h1::text').extract_first()

        name = response.css('.author-template #authorbox h2 b::text').extract_first()
        if name:
            self.extract_author(response, name)

        if title:
            self.extract_article(response, title)

    def extract_article(self, response, title):
        """
        Extracts article data from loaded page and saves into list
        :param response: loaded page
        :param title: extracted title which is flag that page contains any article
        :return: void
        """
        date_str = response.css('#postcontent > div:nth-child(8) > span::text').extract_first()
        date = datetime.strptime(date_str, date_format)
        timestamp = date.timestamp()
        authors = response.css('a.goauthor > span::text').extract()
        url = response.url
        prompt = response.css('.kg-card-markdown > p::text').extract_first()[:160]
        tags = response.css('.tag.secondary::text').extract()

        article = {'title': title, 'date': timestamp, 'authors': authors, 'url': url, 'prompt': prompt, 'tags': tags}
        self._articles.append(article)

    def extract_author(self, response, name):
        """
        Extracts author data from loaded page and saves into list
        :param response: loaded page
        :param name: extracted name which is flag that page contains any author
        :return: void
        """
        posts = response.css('.postlist a').extract()
        job_title = response.css('.author-template #authorbox h2::text').extract_first()
        linkedin = response.css('.authorsocial a[href*="linkedin.com"]::attr(href)').extract_first()

        url = response.url

        author = {'name': name, 'job_title': job_title, 'linked': linkedin, 'posts': len(posts), 'url': url}
        self._authors.append(author)

    def get_articles(self):
        """
        Sorts and returns extracted list of articles
        :return: articles sorted by date
        """
        self._articles.sort(key=lambda k: k['date'])
        return self._articles

    def get_authors(self):
        """
        Returns extracted list of authors
        :return: authors
        """
        return self._authors
