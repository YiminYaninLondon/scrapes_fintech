import scrapy


class FastmarketrisiSpider(scrapy.Spider):
    name = 'FastmarketRISI'
    # allowed_domains = ['www.risiinfo.com']
    start_urls = ['http://www.risiinfo.com/']

    def parse(self, response):
        pass
