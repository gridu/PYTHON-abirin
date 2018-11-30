"""
This is the main file for scrapping grid blog website
"""

import scrapy

main_url = 'https://blog.griddynamics.com/'


class Scrapper(scrapy.Spider):
    name = "scrapper"

    def start_requests(self):
        urls = [main_url]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        articles = response.css('span.ellip').extract()
        print('results:\n')
        print(articles)

