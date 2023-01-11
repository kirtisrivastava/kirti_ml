from scrapy import Request
from scrapy import Selector
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


from ladders_scrapy.data.icims_data import icims_data
from ladders_scrapy.scrapy_files.items import JobItem
from ladders_scrapy.utils.common_utils import common_utils
from ladders_scrapy.db.db_operations import db_operations
from ladders_scrapy.db.db_connection import db_connection


#from scrapy.loader.processors import MapCompose # may be used later so commenting now;


class IcimsiSpider(CrawlSpider):
    print(" icicicicici starts")
    #download_delay = 3
    name = 'icims_dev'
    ats = 'icims'
 #   url_master = db_operations().read_input_from_master(ats)
#    print(url_master)
    start_urls = icims_data.get_urls() #['https://careers-skywest.icims.com/jobs/search'] #icims_data.get_urls()
        # [
        #     'https://careers-lithia.icims.com/jobs/search',
        # ] #icims_data.get_urls()
    #db = db_operations.db_operations()
    #url_master = db.read_input_from_master()


    def parse(self, response):
        selector = Selector(response)
        print((selector.xpath('//span[@id ="live-results-counter"]')))
        print((selector.xpath('//span[@id ="live-results-counter"]/text()').extract()))
        # for check purpose nissan
        yield Request(url=selector.xpath('//iframe/@src').extract()[0],callback=self.parse_url)

        # below block working to handle base site with out uifram

        # current_iframe = selector.xpath('//iframe/@src').extract()[0]
        # if response.url in current_iframe:
        #     yield Request(url=selector.xpath('//iframe/@src').extract()[0],
        #                    callback=self.parse_url)
        # # for checking purpose
        # elif selector.xpath('//span[@id ="live-results-counter"]/text()').extract():
        #     rules = [
        #         Rule(LinkExtractor(allow=[
        #             'http://www.tiffanycareers.com/job/[\d]+/[\w+-]+/'
        #         ], unique=True),
        #             callback='parse_urls', process_links='process_links')
        #     ]
        # elif selector.xpath('//div[@class ="iCIMS_JobsTablePaging iCIMS_Table"]//div[@class="iCIMS_TableCell"]/text()').extract():
        #     pass
        # else:
        #     pass

    # woking it can used for url in some scnerios
    def parse_urls(self, response):
       pass

    def parse_url(self, response):
        selector = Selector(response)
        pagination = selector.xpath('//div[@class ="iCIMS_JobsTablePaging iCIMS_Table"]//div[@class="iCIMS_TableCell"]/text()').extract()
        page_count = "".join(pagination)
        page_count = common_utils.get_int_from_string(page_count)

        url_to_write = []
        for i in range(0, page_count):
            sub_url = response.url.split('?')[0] + '?pr=' + str(i)
            # if sub_url not in self.url_master:
            #     self.url_master.append(sub_url)
            #     self.db.insert_in_to_master(sub_url)
            yield Request(url=sub_url, callback=self.parse_old)

    def parse_old(self, response):
        selector = Selector(response)
        yield Request(url=selector.xpath('//iframe/@src').extract()[0],callback=self.parse_iframe)


    def parse_iframe(self, response1):
        # print(" parse fram :: ", response1)
        # Rule(LinkExtractor(allow=[], unique=True,restrict_css=['span.iCIMS_JobsTableHeader + a::attr(href)']),callback='parse_item', process_links='process_duplicate_urls')
        #print(type(response1.css('span.iCIMS_JobsTableHeader + a::attr(href)').extract()))
        #print(response1.css('span.iCIMS_JobsTableHeader + a::attr(href)').extract())
        #for posting_url in response1.css('span.iCIMS_JobsTableHeader + a::attr(href)').extract():
        url=response1.css('span.iCIMS_JobsTableHeader + a::attr(href)').extract()
        return(self.process_duplicate_urls(url))
            #yield Request(url=posting_url, callback=self.process_duplicate_urls)


    def process_duplicate_urls(self, new_url_list):
        self.db = db_connection()
        self.db = self.db.get_connection()
        self.cursor = self.db.cursor()
        c_temp = new_url_list[1]
        c_name = c_temp.split('/')[2]
        statement = "select url from crawl_urls where company_name ='" + c_name + "';"
        self.cursor.execute(statement)
        fresh_jobs = []
        old_url_list = [item[0] for item in self.cursor.fetchall()]
        if old_url_list:
            new_jobs = list(set(new_url_list) - set(old_url_list))
            if (new_jobs):
                for url in new_jobs:
                     self.cursor.execute("INSERT INTO crawl_urls (url, flag, company_name,ats) VALUES (%s, %s, %s,%s)",
                                     (url, "LI", c_name,self.ats))
            self.db.commit()
            fresh_jobs = new_jobs
        else:
            fresh_jobs = new_url_list
            for url in fresh_jobs:
                self.cursor.execute("INSERT INTO crawl_urls (url, flag, company_name,ats) VALUES (%s, %s, %s,%s)",
                                (url, "LI", c_name,self.ats))
            self.db.commit()
        self.db.close()

        for url in fresh_jobs:
            yield Request(url=url, callback=self.parse_item)



    def parse_item(self, response2):
        item= JobItem()
        loader = ItemLoader(item, response=response2)
        loader.add_value('url', response2.url)
        tabel_content = response2.xpath('//dl[@class="iCIMS_JobHeaderGroup iCIMS_TableCell"]')

        for content in tabel_content:
            header_value = common_utils.format_string(content.xpath('.//dd[@class="iCIMS_JobHeaderData"]/text()')
                                                             .extract_first(default =" "))
            header_value_opt = content.xpath('.//dd[@class="iCIMS_JobHeaderData"]//span/text()').extract()
            if header_value_opt:
                header_value_opt = common_utils.format_string("".join(header_value_opt))
            else:
                header_value_opt = ''

            header = common_utils.format_string\
                (content.xpath('.//dt[@class="iCIMS_JobHeaderField iCIMS_TableHeader"]/text()')
                 .extract_first(default =" "))
            loader.add_value('table_content', { header : header_value + header_value_opt})
        description_content = response2.xpath('//*[@class="iCIMS_InfoMsg iCIMS_InfoField_Job"]')

        #for content in description_content:
        content = description_content[0]
        heading = common_utils.format_string(content.xpath('.//text()').extract_first(default =" "))
        # common_utils.format_string(
        desc = content.xpath('.//following-sibling::div[@class="iCIMS_InfoMsg iCIMS_InfoMsg_Job"]')[0]\
            .xpath('.//span/text()').extract() #extract_first(default ="")
        desc_opt = content.xpath('.//following-sibling::div[@class="iCIMS_InfoMsg iCIMS_InfoMsg_Job"]')
        #[0] \
            #.xpath('.//p/text()').extract()

        desc_points = content.xpath('.//following-sibling::div[@class="iCIMS_Expandable_Text"]')
        print('==============')
        print(desc_points)

        # if desc:
        #     desc = common_utils.format_string("".join(desc))
        #     desc = desc + ' ' + desc
        # else:
        #     desc = ""

        # if desc_opt:
        #     desc_opt = common_utils.format_string("".join(desc_opt))
        #     desc = desc + ' deedededededededd'+ desc_opt

        # if desc_points:
        #     desc_points = desc_points[0].xpath('.//span/text()').extract()
        #     desc_points = common_utils.format_string("".join(desc_points))
        #     desc = desc + ' pppppppppppppppppppppppppp ' + desc_points

        if desc_opt:
            print("-----------------------------------------------------------------")
            desc_opt = desc_opt.xpath('.//p | .//ul/li | .//h | .//h1 | .//h2 | .//h3 | .//h4 | .//h5 | .//h6') #/text()
            header = "Sub Headers"
            print(desc_opt)
            sub_headers ={'Sub Headers': ''}
            desc_poin = ""
            for point in desc_opt:
                print('==============FOR =======================')
                if point.xpath('./h | ./h1 | ./h2 | ./h3 | ./h4 | .//h5 | ./h6'):
                    print(" =============== HEADER ++++++++")
                    picked_header = point.xpath('./h/text() | ./h1/text() | ./h2/text() | ./h3/text() | ./h4/text() | ./h5/text() | ./h6/text()').extract_first(default ="")
                    if picked_header:
                        header = picked_header
                        desc_poin = ""
                        header_with_desc = point.xpath('./span/text()').extract()
                        sub_headers[header] = " ".join(header_with_desc) if header_with_desc else ''#desc_poin
                        #header_with_desc = point.xpath('./span/text()').extract()
                        #desc_poin = " ".join(header_with_desc)
                        #sub_headers[header] = desc_poin

                elif point.xpath('.//strong/span | .//strong'):
                    print(" =============== HEADER ++++++++")
                    picked_header = point.xpath('./strong/span/text() | ./strong/text() | ./h/text() | ./h1/text() | ./h2/text() | ./h3/text() | ./h4/text() | ./h5/text() | ./h6/text()').extract_first(default ="")
                    if picked_header:
                        header = picked_header
                        desc_poin = ""
                        header_with_desc = point.xpath('./span/text()').extract()
                        sub_headers[header] = " ".join(header_with_desc) if header_with_desc else ''#desc_poin
                        #header_with_desc = point.xpath('./span/text()').extract()
                        #desc_poin = " ".join(header_with_desc)
                        #sub_headers[header] = desc_poin

                elif point.xpath('.//span/text()'):
                    print('______________DESC -----------')
                    desc_poin_list = point.xpath('.//span/text()').extract()
                    desc_poin = common_utils.format_string(", ".join(desc_poin_list))
                    sub_headers[header] = sub_headers[header] + desc_poin

                elif point.xpath('.//br/text()'):
                    print('______________DESC -----------')
                    desc_poin_list = point.xpath('.//br/text()').extract()
                    desc_poin = common_utils.format_string(", ".join(desc_poin_list))
                    sub_headers[header] = sub_headers[header] + desc_poin

                elif point.xpath('.//text()'):
                    print('______________DESC -----------')
                    desc_poin_list = point.xpath('.//text()').extract()
                    desc_poin = common_utils.format_string(", ".join(desc_poin_list))
                    sub_headers[header] = sub_headers[header] + desc_poin



            loader.add_value('sub_headers_details', sub_headers)



                #desc_points = common_utils.format_string("".join(desc_points))
                #desc = desc + ' ' + desc_points

            #loader.add_value('other_details', {heading : desc})

        yield loader.load_item()

