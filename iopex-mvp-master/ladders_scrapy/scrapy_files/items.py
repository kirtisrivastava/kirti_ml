# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.spiders import CrawlSpider, Rule
class JobItem(scrapy.Item):
    title = scrapy.Field()
    location = scrapy.Field()
    team = scrapy.Field()
    Requirements = scrapy.Field()
    Responsibilities = scrapy.Field()
    url = scrapy.Field()
    content_t2 = scrapy.Field()
    content_t1 = scrapy.Field()
    header = scrapy.Field()
    header_value = scrapy.Field()
    table_content = scrapy.Field()
    other_details = scrapy.Field()
    jobtype = scrapy.Field()
    sub_headers_details = scrapy.Field()
    #pass


