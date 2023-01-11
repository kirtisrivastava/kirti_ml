# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import json
from lxml import html
import w3lib.html
from .items import JobItem
from urllib.parse import urljoin, urlparse, urlunparse
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule



class TaleoSpider(scrapy.Spider):
    name = "taleo_t5"

    url_list = [

        "https://jobs.msd.com/search/?q=&startrow=1"
    ]

    def start_requests(self):
        script = """            

                          function wait_for_element(splash, css, maxwait)
                              if maxwait == nil then
                                  maxwait = 10
                              end
                              return splash:wait_for_resume(string.format([[
                                function main(splash) {
                                  var selector = '%s';
                                  var maxwait = %s;
                                  var end = Date.now() + maxwait*1000;

                                  function check() {
                                    if(document.querySelector(selector)) {
                                      splash.resume('Element found');
                                    } else if(Date.now() >= end) {
                                      var err = 'Timeout waiting for element';
                                      splash.error(err + " " + selector);
                                    } else {
                                      setTimeout(check, 20);
                                    }
                                  }
                                  check();
                                }
                              ]], css, maxwait))
                            end

                            local treat = require('treat')
                            local hrefs = {}
							local result, error
                            function main(splash)
                                splash.images_enabled = false
                                splash.plugins_enabled = true
                                splash:go(splash.args.url)
                                wait_for_element(splash,".searchResultsShell",30)
                                splash:wait(2)
                                hrefs[#hrefs+1] = splash:html()
                                while(splash:select('.paginationItemSelected + a[title^="Page"]'))  do
                                  splash:select('.paginationItemSelected + a[title^="Page"]').click()
                                  splash:wait(3)							
                                  result,error = splash:wait_for_resume(string.format([[
                                                    function main(splash) {
                                                      var selector = '%s';
                                                      var maxwait = %s;
                                                      var end = Date.now() + maxwait*1000;
                                                      function check() {
                                                        if(document.querySelector(selector)) {
                                                          splash.resume('Element found');
                                                        } else if(Date.now() >= end) {
                                                          var err = 'Timeout waiting for element';
                                                          splash.error(err + " " + selector);
                                                        } else {
                                                          setTimeout(check, 20);
                                                        }
                                                      }
                                                      check();
                                                    }
                                                  ]], '.searchResultsShell', 30))
  								  if result then
    								hrefs[#hrefs+1] = splash:html()
                                  end						
                                end
                                return {pages=treat.as_array(hrefs)}
                            end

                     """

        for i in self.url_list:
            yield SplashRequest(i, self.form_url, endpoint='execute', args={'lua_source': script, 'timeout': 3600})


    def form_url(self, response2):

        script2 = """ 

                                           local treat = require('treat')
                                           local page = {}
                                           function main(splash)
                                               splash.images_enabled = false
                                               splash.plugins_enabled = true
                                               splash:go(splash.args.url)
                                               splash:wait(3)
                     						    

                                               return { splash:html()
                                               }
                                           end
                                    """

        temp = response2.data['pages']
        print("####no of pages", len(temp))
        for page in temp:
            soup = BeautifulSoup(page, 'html.parser')
            tree=html.fromstring(str(soup))
            urls=tree.xpath('//tbody//span[@class="jobTitle"]//a/@href')
            for i in urls:
                gen = urljoin(response2.url, i)
                print("@@@@@@@@@@@@", gen)
                yield SplashRequest(gen, self.parse_url, endpoint='execute',
                                    args={'lua_source': script2, 'wait': 2.0, 'timeout': 360})



    def parse_url(self, response2):
        l = ItemLoader(item=JobItem(), response=response2)
        l.add_value("url", response2.url)
        data = self.parse_for_data(response2.body)
        l.add_value("content_t1", data)
        yield l.load_item()


    def parse_for_data(self, string):
        parsed_result = []
        soup = BeautifulSoup(string, 'html.parser')
        main_div = None
        if soup.find('div', {"id": "taleoContent"}):
            main_div = soup.find('div', {"id": "taleoContent"})
        elif soup.find('div', {"id": "requisitionDescriptionInterface.descRequisitionContainer"}):
            main_div = soup.find('div', {"id": "requisitionDescriptionInterface.descRequisitionContainer"})
        elif soup.find('div', {"class": "main-content"}):
            main_div = soup.find('div', {"class": "main-content"})
        elif soup.find("div", {"class": "sitewrapper"}):
            main_div = soup.find("div", {"class": "sitewrapper"})
        if not main_div or len(main_div):
            main_div = soup.find('body')

        required_tag = ['div', 'span']
        result = {'no_header': ''}
        current_header = 'no_header'
        s = main_div.find_all(['b', 'strong'])
        headers = [a.getText().strip() for a in s]
        tag = 'span'

        main_div_all_elements = main_div.find_all(['font', 'p', 'li'])

        for tag in main_div_all_elements:
            if tag.getText().strip() in headers:
                if tag.getText().strip() not in result.keys():
                    result[tag.getText().strip()] = ''
                    current_header = tag.getText().strip()
            else:
                result[current_header] = result[current_header] + " " + tag.getText().strip()
        table_elements = main_div.find_all('tr')

        table_data = {}
        for elments in table_elements:
            row = elments.find_all('td')
            # print len(row)
            if len(row) == 2:
                result[row[0].getText()] = row[1].getText()

        parsed_result.append(result)
        return parsed_result



    #     #             #"https://jobs.msd.com/search/?q=&startrow=1"
        # "http://careers.antheminc.com/search-jobs/"