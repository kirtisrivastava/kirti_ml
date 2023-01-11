
from scrapy.spiders import CrawlSpider, Rule
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from ladders_scrapy.db.db_operations import db_operations

class icims_crawl_deactive(CrawlSpider):
    name = 'icims_deactive'
    start_urls = db_operations().read_input_from_master('icims')
    deactived_url_list = []

    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):
        print("Resp :: ", response.url)
        tabel_content = response.xpath('//dl[@class="iCIMS_JobHeaderGroup iCIMS_TableCell"]')
        if tabel_content:
            pass
        else:
            self.deactived_url_list.append(response.url)

    def spider_closed(self, spider):
        print(self.deactived_url_list)
        db_operations().update_deactive(self.deactived_url_list)
        print("completed ")

