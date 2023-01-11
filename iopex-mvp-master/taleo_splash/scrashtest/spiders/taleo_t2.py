# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from lxml import html
import json
import w3lib.html
from .items import JobItem
from lxml import html
from urllib.parse import urljoin, urlparse, urlunparse
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule


class TaleoSpider(scrapy.Spider):
    name = "taleo_t2"
    url_list = [
        # type 1
        "http://chc.tbe.taleo.net/chc01/ats/careers/searchResults.jsp?org=APRIVA&cws=1",
        "http://chk.tbe.taleo.net/chk06/ats/careers/searchResults.jsp?org=MOBITV&cws=1",
        "http://chm.tbe.taleo.net/chm01/ats/careers/searchResults.jsp?org=HELIXESG&cws=1",
        "https://chk.tbe.taleo.net/chk05/ats/careers/searchResults.jsp?org=CMEGROUP&cws=1",
        "http://chp.tbe.taleo.net/chp03/ats/careers/searchResults.jsp?org=DREAMBOX&cws=1",
        "http://chk.tbe.taleo.net/chk01/ats/careers/searchResults.jsp?org=JBSSWIFT&cws=1",
        "https://chp.tbe.taleo.net/chp01/ats/careers/searchResults.jsp?org=QUENCH&cws=1",
        # #hartz
        "http://chc.tbe.taleo.net/chc01/ats/careers/searchResults.jsp?org=HARTZMOUNTAIN&cws=1"

    ]

    def start_requests(self):
        script = """            
                            
                            local treat = require('treat')
                            local hrefs = {}
    					    local el
							local t1
							local t2
                            function main(splash)
                                splash:go(splash.args.url)
  								splash:wait(3)
      							hrefs[#hrefs+1] = splash:html()
                                local b1=splash:select("td.nowrapRegular b:nth-child(1)").node.innerHTML
                                local b2=splash:select("td.nowrapRegular b:nth-child(2)").node.innerHTML
  								i = string.find(b1, b2)
                                if i==nil then
    								i=999
    								end
  								while i == 999 do

    								if splash:select("input[title='Next Page']") then
                                        splash:select("input[title='Next Page']").click()
                                    else
                                        splash:select("td.nowrapRegular ~ td > a").click()
                                    end
                                 splash:wait(3)
                                 hrefs[#hrefs+1] = splash:html()
    							 local t1=splash:select("td.nowrapRegular b:nth-child(1)").node.innerHTML
                                 local t2=splash:select("td.nowrapRegular b:nth-child(2)").node.innerHTML
  								 i= string.find(t1, t2)
    							 if i==nil then
    								i=999
                                 else
                                   break
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

        for page in temp:
            soup = BeautifulSoup(page, 'html.parser')
            if soup.find('td'):
                tree = html.fromstring(str(soup))
                urls = tree.xpath('//td/b/a/@href')
                for i in urls:
                    gen = urljoin(response2.url, i)
                    print("@@@@@@@@@@@@", gen)
                    yield SplashRequest(gen, self.parse_url, endpoint='execute',
                                        args={'lua_source': script2, 'wait': 2.0, 'timeout': 360})

    def parse_url(self, response2):

        temp = response2.data['page']
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
            # print len(row)
            if len(row) == 2:
                result[row[0].getText()] = row[1].getText()

        parsed_result.append(result)
        return parsed_result
