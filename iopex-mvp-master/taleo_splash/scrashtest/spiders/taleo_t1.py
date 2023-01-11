# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import json
import w3lib.html
from lxml import html
from .items import JobItem
from urllib.parse import urljoin, urlparse, urlunparse
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule

class TaleoSpider(scrapy.Spider):
    name = "taleo_t1"

    data = {'no_header': ""}
    current_header = 'no_header'
    result = []
    url_list = [

        ##type 1 <table> tag
        "http://mosaic.taleo.net/careersection/cdn_corporate/jobsearch.ftl",
        "https://engie.taleo.net/careersection/10550/jobsearch.ftl",
        "https://icfi.taleo.net/careersection/icf_prof_ext/jobsearch.ftl",
        "https://regalbeloit.taleo.net/careersection/ex/jobsearch.ftl",
        # Gendex
        "https://engie.taleo.net/careersection/10550/jobsearch.ftl?f=ORGANIZATION(276605011584)&a=null&multiline=false&lang=en",

        ##type 2 <ul> tag
        "https://adt.taleo.net/careersection/exmobile/jobsearch.ftl",
        "https://mckesson.taleo.net/careersection/ex/jobsearch.ftl",
        "https://abercrombie.taleo.net/careersection/1.0/jobsearch.ftl",
        "https://xerox.taleo.net/careersection/xerox_shared_external_portal/jobsearch.ftl",
        "https://nordstrom.taleo.net/careersection/2/jobsearch.ftl",
        "https://alliancedata.taleo.net/careersection/alliancedata/jobsearch.ftl"
    ]

    def start_requests(self):

        script = """ 
                    function wait_for_element(splash, css1, css2, maxwait)
                          if maxwait == nil then
                              maxwait = 10
                          end
                          return splash:wait_for_resume(string.format([[
                            function main(splash) {
                              var selector1 = '%s';
                              var selector2 = '%s';
                              var maxwait = %s;
                              var end = Date.now() + maxwait*1000;

                              function check() {
                                if(document.querySelector(selector1)) {
                                  splash.resume('Element found');
                                }else if(document.querySelector(selector2)) {
                                  splash.resume('Element found');
                                } else if(Date.now() >= end) {
                                  var err = 'Timeout waiting for element';
                                  splash.error(err + " " + selector1 + selector1);
                                } else {
                                  setTimeout(check, 200);
                                }
                                      }
                                      check();
                                    }
                                  ]], css1, css2, maxwait))
                            end

                        local treat = require('treat')
                        local hrefs = {}
					    local el
                        function main(splash)
                            splash.images_enabled = false
                            splash.plugins_enabled = true
                            splash:go(splash.args.url)
                            wait_for_element(splash, 'ul#jobList li[id^="job"]','table#jobs tr[id^="job"]',60)
  							hrefs[#hrefs+1] = splash:html()
  							el = splash:select('span.pagerlink a#next')
  							i=1
  							while el do
                            	assert(splash:runjs("$('div#jobPager a#next').click()"))
                            	splash:wait(3)
                                hrefs[#hrefs+1] = splash:html()
    							el = splash:select('span.pagerlink a#next')
    							i=i+1
    						end
                            return { pages=treat.as_array(hrefs),
                            }

                        end
                 """

        for i in self.url_list:
            yield SplashRequest(i, self.form_url, endpoint='execute', args={'lua_source': script, 'timeout': 3600})

    def form_url(self, response2):

        script2 = """ 
                            
                                local treat = require('treat')
                                local hrefs = {}
                                function main(splash)
                                    splash.images_enabled = false
                                    splash.plugins_enabled = true
                                    splash:go(splash.args.url)
                                    splash:wait(3)
          							hrefs[#hrefs+1] = splash:html()
          		                    
                                    return { page=treat.as_array(hrefs),
                                    }
                                end
                         """

        temp = response2.data['pages']
        print("#############", len(temp))
        for page in temp:
            soup = BeautifulSoup(page,'html.parser')
            if soup.find('table', {"id": "jobs"}):
                tree = html.fromstring(str(soup))
                urls = tree.xpath('//table[@id="jobs"]//th//a/@href')
                for i in urls:
                    gen = urljoin(response2.url, i)
                    print("@@@@@@@@@@@@", gen)
                    yield SplashRequest(gen, self.parse_url, endpoint='execute',
                                        args={'lua_source': script2, 'wait': 2.0, 'timeout': 360})

    def parse_url(self, response3):
        temp = response3.data['page']
        l = ItemLoader(item=JobItem(), response=response3)
        l.add_value("url", response3.url)
        data = self.parse_for_data(temp[0])
        l.add_value("content_t1", data)
        yield l.load_item()

    def parse_for_data(self, stri):
        soup = BeautifulSoup(stri,'html.parser')
        if soup.find('div', {"id": "taleoContent"}):
            main_div = soup.find('div', {"id": "taleoContent"})
        elif soup.find('div', {"id": "requisitionDescriptionInterface.descRequisitionContainer"}):
            main_div = soup.find('div', {"id": "requisitionDescriptionInterface.descRequisitionContainer"})

        s = main_div.find_all(['b', 'strong'])
        headers = [a.getText().strip() for a in s]
        main_div_all_elements = main_div.find_all(['font', 'li', 'p'])
        result = {'no_header': ''}
        current_header = 'no_header'

        for tag in main_div_all_elements:
            if tag.getText().strip() in headers:
                if tag.getText().strip() not in result.keys():
                    result[tag.getText().strip()] = ''
                    current_header = tag.getText().strip()
            else:
                result[current_header] = result[current_header] + " " + tag.getText().strip()
        return result


