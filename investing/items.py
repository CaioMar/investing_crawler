# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InvestingItem(scrapy.Item):
    article_title = scrapy.Field()
    article_link = scrapy.Field()
    article_text = scrapy.Field()
    article_author = scrapy.Field()
    article_type = scrapy.Field()
    article_date = scrapy.Field()

class NoticiasItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    text = scrapy.Field()
    link = scrapy.Field()