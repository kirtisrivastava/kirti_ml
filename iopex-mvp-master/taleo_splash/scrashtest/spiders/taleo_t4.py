# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import json
import w3lib.html
from .items import JobItem
from urllib.parse import urljoin, urlparse, urlunparse
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule


class TaleoSpider(scrapy.Spider):
    name = "taleo_t4"

    url_list = [

    "https://chp.tbe.taleo.net/chp04/ats/careers/v2/searchResults?org=KMMG&cws=46",
    "https://chp.tbe.taleo.net/chp02/ats/careers/v2/searchResults?org=WESTLAKECHEM&cws=46",
    "https://chp.tbe.taleo.net/chp02/ats/careers/v2/searchResults?org=WESTLAKECHEM&cws=48",
    "https://chp.tbe.taleo.net/chp02/ats/careers/v2/searchResults?org=WESTLAKECHEM&cws=41"


    ]

    def start_requests(self):
        script = """            
                           
                           function main(splash)
                                splash.images_enabled = false
                                splash.plugins_enabled = true
                                local num_scrolls = 10
                                local scroll_to = splash:jsfunc("window.scrollTo")
                                local get_body_height = splash:jsfunc(
                                    "function() {return document.body.scrollHeight;}"
                                )
                                assert(splash:go(splash.args.url))
                                splash:wait(2)
                            
                                for _ = 1, num_scrolls do
                                    scroll_to(0, get_body_height())
                                    splash:wait(5)
                                end        
                                return splash:html()
                            end
                        
                     """

        for i in self.url_list:
            yield SplashRequest(i, self.form_url, endpoint='execute', args={'lua_source': script, 'timeout': 3600})

    def form_url(self, response2):
        urls=response2.xpath("//h4[@class='oracletaleocwsv2-head-title']/a/@href").extract()
        print("@@@@@@@@",urls)
        for i in urls:
                   yield SplashRequest(i,self.parse_url, endpoint='render.html', args={'wait': 2.0, 'timeout': 3600})

    def parse_url(self, response3):

        l = ItemLoader(item=JobItem(), response=response3)
        l.add_value("url", response3.url)
        data = self.parse_first_type(response3.body)
        l.add_value("content_t1", data)
        yield l.load_item()

    def parse_first_type(self, stri):
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

