from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ladders_scrapy.scrapy_files import items
from ladders_scrapy.db.db_connection import db_connection
from ladders_scrapy.db.db_operations import db_operations
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.loader import ItemLoader


class LeverSpider(CrawlSpider):



    name = 'lever'
    ats='lever'
    current_run_url_list = []
    allowed_domains = ['jobs.lever.co']
    start_urls = [
        # Start url links

        'https://jobs.lever.co/yelp?commitment=Full-time',
        'https://jobs.lever.co/looker?commitment=Full-time',
        'https://jobs.lever.co/counsyl?commitment=Full-time',
        'https://jobs.lever.co/counsyl?commitment=Hourly%20Full-time',
        'https://jobs.lever.co/gametime?commitment=Full%20Time',
        'https://jobs.lever.co/gametime/?commitment=Full%20Time%2FHourly',
        'https://jobs.lever.co/gametime/?commitment=Full-time',
        'https://jobs.lever.co/clearcapital?commitment=Full-time',
        'https://jobs.lever.co/clearcapital?commitment=Full%20Time',
        'https://jobs.lever.co/carbon?commitment=Full-time',
        'https://jobs.lever.co/theaudience?commitment=Full-time',
        'https://jobs.lever.co/lastline?commitment=Full-time',
        'https://jobs.lever.co/whisper?commitment=Full-time',
        'https://jobs.lever.co/retentionscience?commitment=Full-time',
        'https://jobs.lever.co/reputation?commitment=Full-time',
        'https://jobs.lever.co/squaretrade?commitment=Full-time',
        'https://jobs.lever.co/clearslide?commitment=Full%20Time',
        'https://jobs.lever.co/addepar?commitment=Full-time',
        'https://jobs.lever.co/kickstarter?commitment=Full-time',
        'https://jobs.lever.co/instructure?commitment=Full-time',
        'https://jobs.lever.co/faradayfuture?commitment=Full-time',
        'https://jobs.lever.co/tapfwd?commitment=Full%20Time',
        'https://jobs.lever.co/contrastsecurity?commitment=Full-time',
        'https://jobs.lever.co/augmedix?commitment=Full-time',
        'https://jobs.lever.co/jawbone?commitment=Full-time',
        'https://jobs.lever.co/upserve?commitment=Full-time',
        'https://jobs.lever.co/upserve?commitment=Full-time',
        'https://jobs.lever.co/sevone?commitment=Full-time',
        'https://jobs.lever.co/chariot?commitment=Full-time',
        'https://jobs.lever.co/zirmed?commitment=Full-time',
        'https://jobs.lever.co/adaptly?commitment=Full%20time',
        'https://jobs.lever.co/efront/?commitment=Full-time',
        'https://jobs.lever.co/contently?commitment=Full-time',
        'https://jobs.lever.co/thinkhr?commitment=Full-time',
        'https://jobs.lever.co/luxe?commitment=Full-time',
        'https://jobs.lever.co/luxe?commitment=full-time',
        'https://jobs.lever.co/tileapp?commitment=Full-time',
        'https://jobs.lever.co/lumosity?commitment=Full-time',
        'https://jobs.lever.co/ifttt/?commitment=Full-time',
        'https://jobs.lever.co/ShyftAnalytics?commitment=Full-time',
        'https://jobs.lever.co/activecampaign?commitment=Full-time',
        'https://jobs.lever.co/adaptly?commitment=Full%20time',
        'https://jobs.lever.co/addepar?commitment=Full-time',
        'https://jobs.lever.co/affirm?commitment=Full-time',
        'https://jobs.lever.co/ahalogy?commitment=Full-time',
        'https://jobs.lever.co/alicetechnologies?commitment=Full-time',
        'https://jobs.lever.co/alittledata?commitment=Full-time',
        'https://jobs.lever.co/animoto?commitment=Full-time',
        'https://jobs.lever.co/anomali?commitment=Full-time',
        'https://jobs.lever.co/augmedix?commitment=Full-time',
        'https://jobs.lever.co/biodigital?commitment=Full-time',
        'https://jobs.lever.co/blend?commitment=Full-time',
        'https://jobs.lever.co/bloc?commitment=Full-time',
        'https://jobs.lever.co/bluecore?commitment=Full-time',
        'https://jobs.lever.co/bondstreet?commitment=Full-time',
        'https://jobs.lever.co/bpmcpa?commitment=Full-time',
        'https://jobs.lever.co/brigade?commitment=Full-time',
        'https://jobs.lever.co/carbon?commitment=Full-time',
        'https://jobs.lever.co/chariot?commitment=Full-time',
        'https://jobs.lever.co/chownow?commitment=Full-time',
        'https://jobs.lever.co/circleci?commitment=Full-time',
        'https://jobs.lever.co/clearcapital?commitment=Full-time',
        'https://jobs.lever.co/clearcapital?commitment=Full%20Time',
        'https://jobs.lever.co/clearcapital?commitment=Full-time',
        'https://jobs.lever.co/clearpoolgroup?commitment=Full-time',
        'https://jobs.lever.co/clearslide?commitment=Full-time',
        'https://jobs.lever.co/clearslide?commitment=Full%20Time',
        'https://jobs.lever.co/clever?commitment=Full-time',
        'https://jobs.lever.co/close.io?commitment=Full-time',
        'https://jobs.lever.co/cloudhealthtech?commitment=Full-time',
        'https://jobs.lever.co/codecademy?commitment=Full-time',
        'https://jobs.lever.co/contently?commitment=Full-time',
        'https://jobs.lever.co/contrastsecurity?commitment=Full-time',
        'https://jobs.lever.co/counsyl?commitment=Full-time',
        'https://jobs.lever.co/coverhound?commitment=Full-time',
        'https://jobs.lever.co/daqri?commitment=Full-time',
        'https://jobs.lever.co/degreed?commitment=Full-time',
        'https://jobs.lever.co/drawbridge?commitment=Full-time',
        'https://jobs.lever.co/drizly?commitment=Full-time',
        'https://jobs.lever.co/efront?commitment=Full-time',
        'https://jobs.lever.co/endlessos?commitment=Full-time',
        'https://jobs.lever.co/equityzen?commitment=Full-time',
        'https://jobs.lever.co/esharesinc?commitment=Full-time',
        'https://jobs.lever.co/exabeam?commitment=Full-time',
        'https://jobs.lever.co/faradayfuture?commitment=Full-time',
        'https://jobs.lever.co/ff?commitment=Full-time',
        'https://jobs.lever.co/fiscalnote?commitment=Full-time',
        'https://jobs.lever.co/flipagram?commitment=Full-time',
        'https://jobs.lever.co/frame.io?commitment=Full-time',
        'https://jobs.lever.co/freebalance?commitment=Full-time',
        'https://jobs.lever.co/freshly?commitment=Full-time',
        'https://jobs.lever.co/fundera?commitment=Full-time',
        'https://jobs.lever.co/galvanize?commitment=Full-time',
        'https://jobs.lever.co/gametime?commitment=Full-time',
        'https://jobs.lever.co/gametime?commitment=Full%20Time',
        'https://jobs.lever.co/getaround?commitment=Full-time',
        'https://jobs.lever.co/getbellhops?commitment=Full-time',
        'https://jobs.lever.co/gigya?commitment=Full-time',
        'https://jobs.lever.co/greenchef?commitment=Full-time',
        'https://jobs.lever.co/helpshift?commitment=Full-time',
        'https://jobs.lever.co/hive_url_tld?commitment=Full-time',
        'https://jobs.lever.co/honestbuildings?commitment=Full-time',
        'https://jobs.lever.co/howden?commitment=Full-time',
        'https://jobs.lever.co/ifttt?commitment=Full-time',
        'https://jobs.lever.co/ingenu?commitment=Full-time',
        'https://jobs.lever.co/instructure?commitment=Full-time',
        'https://jobs.lever.co/internetmarketinginc?commitment=Full-time',
        'https://jobs.lever.co/isl.co?commitment=Full-time',
        'https://jobs.lever.co/jawbone?commitment=Full-time',
        'https://jobs.lever.co/jawbone?commitment=Full-time',
        'https://jobs.lever.co/kickstarter?commitment=Full-time',
        'https://jobs.lever.co/lastline?commitment=Full-time',
        'https://jobs.lever.co/launchdarkly?commitment=Full-time',
        'https://jobs.lever.co/lever?commitment=Full-time',
        'https://jobs.lever.co/looker?commitment=Full-time',
        'https://jobs.lever.co/lotlinx?commitment=Full-time',
        'https://jobs.lever.co/lumosity?commitment=Full-time',
        'https://jobs.lever.co/luxe?commitment=Full-time',
        'https://jobs.lever.co/lyft?commitment=Full-time',
        'https://jobs.lever.co/myemma?commitment=Full-time',
        'https://jobs.lever.co/nimasensor?commitment=Full-time',
        'https://jobs.lever.co/onrampwireless?commitment=Full-time',
        'https://jobs.lever.co/parkwhiz?commitment=Full-time',
        'https://jobs.lever.co/penumbrainc?commitment=Full-time',
        'https://jobs.lever.co/pillpack?commitment=Full-time',
        'https://jobs.lever.co/plangrid?commitment=Full-time',
        'https://jobs.lever.co/pond5?commitment=Full-time',
        'https://jobs.lever.co/poynt?commitment=Full-time',
        'https://jobs.lever.co/public.zirmed?commitment=Full-time',
        'https://jobs.lever.co/radialpoint?commitment=Full-time',
        'https://jobs.lever.co/reputation?commitment=Full-time',
        'https://jobs.lever.co/retentionscience?commitment=Full-time',
        'https://jobs.lever.co/retentionscience?commitment=Full-time',
        'https://jobs.lever.co/revzilla?commitment=Full-time',
        'https://jobs.lever.co/rocana?commitment=Full-time',
        'https://jobs.lever.co/rocketlawyer?commitment=Full-time',
        'https://jobs.lever.co/schoolzilla?commitment=Full-time',
        'https://jobs.lever.co/scienceexchange?commitment=Full-time',
        'https://jobs.lever.co/sevone?commitment=Full-time',
        'https://jobs.lever.co/sevone?commitment=Full-time',
        'https://jobs.lever.co/shapesecurity?commitment=Full-time',
        'https://jobs.lever.co/sharethis?commitment=Full-time',
        'https://jobs.lever.co/skillshare?commitment=Full-time',
        'https://jobs.lever.co/socialtables?commitment=Full-time',
        'https://jobs.lever.co/sonomapartners?commitment=Full-time',
        'https://jobs.lever.co/spreemo?commitment=Full-time',
        'https://jobs.lever.co/sprig?commitment=Full-time',
        'https://jobs.lever.co/squaretrade?commitment=Full-time',
        'https://jobs.lever.co/squaretrade?commitment=Full-time',
        'https://jobs.lever.co/stevenstransport?commitment=Full-time',
        'https://jobs.lever.co/symphonmerce?commitment=Full-time',
        'https://jobs.lever.co/tallwave?commitment=Full-time',
        'https://jobs.lever.co/tapfwd?commitment=Full%20Time',
        'https://jobs.lever.co/tempalert?commitment=Full-time',
        'https://jobs.lever.co/theaudience?commitment=Full-time',
        'https://jobs.lever.co/thelevelup?commitment=Full-time',
        'https://jobs.lever.co/thetileapp?commitment=Full-time',
        'https://jobs.lever.co/thinkhr?commitment=Full-time',
        'https://jobs.lever.co/tileapp?commitment=Full-time',
        'https://jobs.lever.co/timehop?commitment=Full-time',
        'https://jobs.lever.co/tune?commitment=Full-time',
        'https://jobs.lever.co/udacity?commitment=Full-time',
        'https://jobs.lever.co/upserve?commitment=Full-time',
        'https://jobs.lever.co/upserve?commitment=Full-time',
        'https://jobs.lever.co/usebutton?commitment=Full-time',
        'https://jobs.lever.co/victorious?commitment=Full-time',
        'https://jobs.lever.co/whisper?commitment=Full-time',
        'https://jobs.lever.co/yelp?commitment=Full-time',
        'https://jobs.lever.co/yelp?commitment=Full-time',
        'https://jobs.lever.co/yprime?commitment=Full-time',
        'https://jobs.lever.co/zenreach?commitment=Full-time',
        'https://jobs.lever.co/zerocater?commitment=Full-time',
        'https://jobs.lever.co/zignallabs?commitment=Full-time',
        'https://jobs.lever.co/zirmed?commitment=Full-time'
    ]

    rules = [
        Rule(LinkExtractor(allow=[
            # Job url regex
            'https://jobs.lever.co/[a-zA-Z]+/[\w+-]+'
        ], unique=True),
            callback='parse_item',process_links='process_urls') #
    ]


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(LeverSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def process_urls(self, url_list):
        db = db_connection()
        db = db.get_connection()
        cursor = db.cursor()
        c_temp = url_list[1].url
        c_name = c_temp.split('/')[-2].strip()
        crawled_url_list = []

        for i in url_list:
            crawled_url_list.append(i.url)
        self.current_run_url_list.extend(crawled_url_list)
        print("===================",len(self.current_run_url_list))
        statement = "select url from crawl_urls where company_name ='"+ c_name +"';"
        cursor.execute(statement)
        fresh_jobs = []

        old_url_from_DB = [item[0].strip() for item in cursor.fetchall()]

        if old_url_from_DB:
            print("Job count in DB ----------------",len(old_url_from_DB))
            new_jobs = list(set(crawled_url_list) - set(old_url_from_DB))
            if new_jobs:
                for i in new_jobs:
                    cursor.execute("INSERT INTO crawl_urls (url, flag, company_name,ats) VALUES (%s, %s, %s,%s)",
                                   (i, "ACTIVE", c_name, self.ats))
            db.commit()
            temp = []
            for i in url_list:
                if i.url in new_jobs:
                    temp.append(i)
            fresh_jobs = temp
        else:
            fresh_jobs = url_list
            for i in fresh_jobs:
                cursor.execute("INSERT INTO crawl_urls (url, flag, company_name,ats) VALUES (%s, %s, %s,%s)",
                               (i.url, "ACTIVE", c_name, self.ats))
            db.commit()
        db.close()
        return fresh_jobs

    def parse_item(self, response):

        l = ItemLoader(item=items.JobItem(), response=response)
        l.add_value('url', response.url)
        l.add_xpath('location', '//div[@class="content"]//*[@class="posting-categories"]/div[1]/text()')
        l.add_xpath('title', '//div[@class="content"]//*[@class="posting-headline"]/h2/text()')
        l.add_xpath('team', '//div[@class="content"]//*[@class="posting-categories"]/div[2]/text()')
        l.add_xpath('jobtype', '//div[@class="content"]//*[@class="posting-categories"]/div[3]/text()')

        # nested loader
        content_loader_type1 = response.xpath(
            '//div[@class="content"]//*[@class ="posting-requirements plain-list"]//preceding-sibling::h3')

        # Type 1 page handler
        for i, sel1 in enumerate(content_loader_type1):
            header = sel1.xpath('./text()').extract_first()
            if (header and not isinstance(header, type(None))) or str(header) != "None":
                header = header.replace('\\u2013', '\\u0020')
                header = header.replace('\\u00a0', '\\u0020')  # nbsp
                header = header.replace('\\u2013', '\\u0020')  # hypen
                header = header.replace('\\u2026', '\\u0020')  # ...
                header = header.replace('\\u2019', '\\u0020')  # quotes
                header = header.replace('\\u201c', '\\u0020')  # Left double quotes
                header = header.replace('\\u201d', '\\u0020')
                header = header.strip(':')
                if len(str(header)) < 30 and len(str(header)) > 1 and not isinstance(header, type(None)):
                    value = response.xpath(
                        '(//div[@class="content"]//ul[@class ="posting-requirements plain-list"])[$val]//li/text()',
                        val=i + 1).extract()
                    value = [r.replace('\\u2013', '\\u2010') for r in value]
                    value = [r.replace('\\u00a0', '\\u0020') for r in value]
                    value = [r.replace('\\u2026', '\\u002E') for r in value]
                    value = [r.replace('\\u2019', '\\u0027') for r in value]
                    value = [r.replace('\\u201c', '\\u0020') for r in value]
                    value = [r.replace('\\u201d', '\\u0020') for r in value]
                    l.add_value('content_t1', {header: value})

        test = {'no_header': []}
        current_header = 'no_header'
        content_loader_type2 = response.xpath(
            '//div[@class="content"]//div[@class="section section page-centered"]//div')

        # Type 2 page handler
        for sel2 in content_loader_type2:
            div = sel2.xpath('./b/u/text() |./u/b/text() |./b/text() ').extract_first()
            if (div and not isinstance(div, type(None))) or str(div) != "None":
                div = div.replace('\\u2013', '\\u0020')
                div = div.replace('\\u00a0', '\\u0020')  # nbsp
                div = div.replace('\\u2013', '\\u0020')  # hypen
                div = div.replace('\\u2026', '\\u0020')  # ...
                div = div.replace('\\u2019', '\\u0020')  # quotes
                div = div.replace('\\u201c', '\\u0020')  # Left double quotes
                div = div.replace('\\u201d', '\\u0020')
                if str(div) != ':' and div and len(str(div)) < 30:
                    current_header = div.strip()
                    current_header = current_header.strip(':')
                    if current_header not in test:
                        test[current_header] = []

            value = sel2.xpath('.//span/text() | ./text()').extract()
            if (value and not isinstance(value, type(None))) or str(value) != "None":
                value = [r.replace('\\u2013', '\\u0020') for r in value]
                value = [r.replace('\\u00a0', '\\u0020') for r in value]
                value = [r.replace('\\u2026', '\\u0020') for r in value]
                value = [r.replace('\\u2019', '\\u0020') for r in value]
                value = [r.replace('\\u201c', '\\u0020') for r in value]
                value = [r.replace('\\u201d', '\\u0020') for r in value]
                value = [r.replace('\xb7', ' ') for r in value]
                value = [r.replace('\\u00b7', ' ') for r in value]
                value = [r.replace('\\u2022', '\\u0020') for r in value]
                value = [r.strip() for r in value]
                value = [r.strip(':') for r in value]
                temp_value = []
                for r in value:
                    if str(r) != "None" and not isinstance(r, type(None)) and len(str(r.strip())) > 1:
                        temp_value.append(r.strip())
                if temp_value:
                    test[current_header] = test[current_header] + temp_value
        l.add_value('content_t2', test)
        return l.load_item()

    def spider_closed(self, spider):
        db_operations().deactive_lever(self.current_run_url_list, self.ats)
        print("completed ")




