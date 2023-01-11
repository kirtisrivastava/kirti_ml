# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
import json
from lxml import html
from scrapy.linkextractors import LinkExtractor
from .items import JobItem
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from urllib.parse import urljoin, urlparse, urlunparse
from scrapy.spiders import CrawlSpider, Rule


class TaleoSpider(scrapy.Spider):
    name = "taleo_t3"
    url_list = [

        "http://aflac.taleo.net/careersection/external/jobsearch.ftl",
        "https://kelloggs.taleo.net/careersection/2/jobsearch.ftl",
        "https://pru.taleo.net/careersection/2/jobsearch.ftl",
        "https://caterpillar.taleo.net/careersection/cat+external+cs/jobsearch.ftl",
        "https://humana.taleo.net/careersection/externalus/moresearch.ftl",
        "https://valero.taleo.net/careersection/2/jobsearch.ftl",
        "https://manitowoc.taleo.net/careersection/prof_buyers/jobsearch.ftl",
        "https://hsn.taleo.net/careersection/2/jobsearch.ftl",
        "https://easternbank.taleo.net/careersection/ex/jobsearch.ftl",
        "https://emerson.taleo.net/careersection/ex/jobsearch.ftl",
        # #gendex Iframe
        "https://danaher.taleo.net/careersection/external/jobsearch.ftl?lang=en&radiusType=K&radius=1&organization=801382850&portal=101430233"

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
                                wait_for_element(splash,"div.ftllist",30)
                                splash:select("span.titlelink a").click()
                                splash:wait(5)
                                hrefs[#hrefs+1] = splash:html()

                                local el= splash:select("span.pagerlink a[id*=Next]")
                                local i=1
                                wait_for_element(splash,"span.pagerlink a[id*=Next]",30)
                                while (splash:select("span.pagerlink a[id*=Next]"))  do
                                  splash:select("span.pagerlink a[id*=Next]").click()
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
                                                  ]], 'div.editablesection', 30))
  								  if result then
    								hrefs[#hrefs+1] = splash:html()
                                  end
                                  i=i+1
    															
                                end
                                return {pages=treat.as_array(hrefs)}
                            end


                     """

        for i in self.url_list:
            yield SplashRequest(i, self.parse_url, endpoint='execute', args={'lua_source': script, 'timeout': 3600})

    def parse_url(self, response2):

        temp = response2.data['pages']
        print("length!!!!!!!!!!!!!!!!!", len(temp))
        for i in temp:
            l = ItemLoader(item=JobItem(), response=response2)
            l.add_value("url", response2.url)
            data = self.parse_for_data(i)
            l.add_value("content_t1", data)
            yield l.load_item()

    def parse_for_data(self, stri):
        parsed_result = []
        soup = BeautifulSoup(stri, 'html.parser')
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

            if len(row) == 2:
                result[row[0].getText()] = row[1].getText()

        parsed_result.append(result)

        return parsed_result
