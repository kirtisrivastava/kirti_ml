from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider

from ladders_scrapy.scrapy_files.items import JobItem


#from utils import common_utils
#from data import taleo_data

#from scrapy.loader.processors import MapCompose # may be used later so commenting now;


class TaleoSpider(CrawlSpider):
    name = 'taleo'
    start_urls = ['http://mosaic.taleo.net/careersection/cdn_corporate/jobdetail.ftl?job=ACOSTACMCAL0117'] #taleo_data.mosaic_data().get_start_urls()
    HEADER_TAG = ['b']
    DESCRIPTION_TAG = ['p', 'li', 'span.text']



    def parse(self, response):
        item=JobItem()
        loader = ItemLoader(item, response=response)
        loader.add_value('url', response.url)
        print((response.url))

        # form = response.xpath('//form[@id="ftlform"]//div[@class="masterbody"]')
        list = response.xpath('//div//span[@class="subtitle"]/text()').extract()

        #loader.add_value('title', list)
        title = response.xpath('//div//span[@class="titlepage"]/text()').extract()
        print("title-----",title)
        yield loader.load_item()
        #form = response.xpath('//form[@id="ftlform"]//div[@class="masterbody"]')
        #print((form.xpath('.//div[@class="editablesection"]//div//span[@class="titlepage"]/text()').extract()))
        #print 'paragrapgh', response.xpath('//span[@class="blockpanel"]//following-sibling::span//child::p[@class="MsoNormal"]/text()')

        #content_list = tabel_content.xpath('.//child::p[@class="MsoNormal"]').extract()
        #print 'content---', content_list
        #for content in content_list:
           # print content.xpath('/text').extract()


        #tabel_content = response.xpath('//dl[@class="iCIMS_JobHeaderGroup iCIMS_TableCell"]')

        # for content in tabel_content:
        #     header_value = common_utils.common_utils.format_string(content.xpath('.//dd[@class="iCIMS_JobHeaderData"]/text()')
        #                                                      .extract_first(default =" "))
        #     header_value_opt = content.xpath('.//dd[@class="iCIMS_JobHeaderData"]//span/text()').extract()
        #     if header_value_opt:
        #         header_value_opt = common_utils.common_utils.format_string("".join(header_value_opt))
        #     else:
        #         header_value_opt = ''
        #
        #     header = common_utils.common_utils.format_string\
        #         (content.xpath('.//dt[@class="iCIMS_JobHeaderField iCIMS_TableHeader"]/text()')
        #          .extract_first(default =" "))
        #     loader.add_value('table_content', { header : header_value + header_value_opt})
        # description_content = response.xpath('//*[@class="iCIMS_InfoMsg iCIMS_InfoField_Job"]')
        #
        # for content in description_content:
        #     heading = common_utils.common_utils.format_string(content.xpath('.//text()').extract_first(default =" "))
        #     desc = common_utils.common_utils.format_string(content.xpath('.//following-sibling::div[@class="iCIMS_InfoMsg iCIMS_InfoMsg_Job"]')[0]\
        #         .xpath('.//span/text()').extract_first(default =""))
        #     desc_opt = content.xpath('.//following-sibling::div[@class="iCIMS_InfoMsg iCIMS_InfoMsg_Job"]')[0] \
        #         .xpath('.//p/text()').extract()
        #
        #     if desc_opt:
        #         desc_opt = common_utils.common_utils.format_string("".join(desc_opt))
        #         desc = desc + ' '+ desc_opt
        #     else:
        #         desc_opt = ''
        #     loader.add_value('other_details', {heading : desc})

