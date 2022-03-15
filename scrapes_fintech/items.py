# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class ScrapesFintechItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass
class FintechIndexPriceItem(scrapy.Item):
    source = scrapy.Field()  # What provider was this info sourced from?
    source_url = scrapy.Field()  # What is the specific url it was sourced from?
    original_index_id = scrapy.Field()
    index_specification = scrapy.Field()
    published_date = scrapy.Field()
    price = scrapy.Field()
