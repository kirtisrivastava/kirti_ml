from bs4 import BeautifulSoup
from holmium.core import Page, Element, Elements, ElementMap, Section, Locators, conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import unittest
import selenium
import re
import time

import xlrd
import xlsxwriter
import datetime
import logging
import os
import os.path

import requests
import json
import sys



class taleo_holmiun_page(Page):

    search = Element(Locators.CSS_SELECTOR, '.menu-items li a', timeout=20,)
    job_elements = Elements(Locators.CSS_SELECTOR, "table .contentlist tr.ftlcopy.ftlrow",
                               only_if=lambda el: el[0].is_displayed(), timeout=20, value=lambda el: {
            'job_link': el.find_element_by_css_selector('.titlelink a'),
        })
    scroll_pos = Element(Locators.CSS_SELECTOR, '.tablelist', timeout=20)
    job_details = Elements(Locators.CSS_SELECTOR, 'p', timeout=20)
    job_title = Elements(Locators.CSS_SELECTOR, '.contentlinepanel .titlepage', timeout=10)
    pager_link = Elements(Locators.CLASS_NAME, 'pagerlink', timeout=10)
    all_div = Elements(Locators.CSS_SELECTOR, '.contentlinepanel', timeout=10)
    all_div = Elements(Locators.CSS_SELECTOR, '.contentlinepanel', timeout=10)

class taleo_automation():

    HEADER_TAG = ['h2', 'strong']
    DESCRIPTION_TAG = ['p', 'li', 'span.text']

    def __init__(self, driver):
        self.driver = driver
        self.data = {'no_header': ""}
        self.current_header = 'no_header'
        self.result = []

    def scrollElementIntoView(self, e):
        self.driver.execute_script("arguments[0].scrollIntoView()", e)

    def check_next(self):
        paginations = self.page.pager_link
        next_page = False
        if paginations:
            for next in paginations:
                link = next.find_element_by_tag_name("a")
                if 'next' in link.get_attribute('title'):
                    link.click()
                    time.sleep(10)
                    return True

        return next_page

    def fetch_value(self,url):
        self.data = { 'no_header': []}
        job = ''
        if self.page.job_title:
            job = [j.text for j in self.page.job_title]
            job = " ".join(job)

        self.data = {'job' : job, 'url': url}
        for divs in self.page.all_div:
            #check for header
            header = None
            for head_tag in self.HEADER_TAG:
                header = divs.find_elements_by_css_selector(head_tag)
                if header and str(header[0].text).strip() != '':
                    header = divs.find_element_by_css_selector(head_tag)
                    header = header.text
                    self.current_header = str(header)
                    self.data[str(self.current_header)] = ""

                    for desc_tag in self.DESCRIPTION_TAG:
                        description =  divs.find_elements_by_css_selector(desc_tag)
                        if description:
                            description = [desc.text for desc in description]
                            description = ' '.join(description)
                            self.data[self.current_header] = self.data[self.current_header] + " " +str(description)

        self.result.append(self.data)
        return json.dumps(self.result)

    def get_job_detail(self, url_list):
        for url in url_list:
            self.page = taleo_holmiun_page(self.driver, url)

            time.sleep(5)
            #print " Detail" , self.page.job_details
            result ={}
            current_label = None
            tittle = []

            print(len(self.page.all_div))

            try:
                self.fetch_value(url)
            except:
                print(" error in :: ", url)
        return self.result


if __name__ == '__main__':
    url_list =[

        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002763&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002764&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002769&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002770&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002772&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002774&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002807&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002808&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002810&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002811&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002813&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002814&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002816&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002818&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002823&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002825&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002826&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002828&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002829&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002830&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002831&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002832&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002834&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002835&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002843&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002846&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002848&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002850&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002852&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002858&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002862&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002868&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002873&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002876&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002877&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002879&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002880&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002881&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002882&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002883&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002884&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002885&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002886&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002887&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002888&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002889&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002890&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002892&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002894&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002898&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002899&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002905&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002913&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002914&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002917&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002921&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002924&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002926&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002928&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002930&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002931&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002933&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002939&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002940&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002944&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002945&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002950&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002951&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002954&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002956&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002959&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002961&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002966&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002967&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002971&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002975&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002980&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002985&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002986&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002987&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002988&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002989&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002990&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002991&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002992&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002994&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002998&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003004&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003010&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003015&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003017&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003023&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003024&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003025&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003026&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003028&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003029&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003030&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003031&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003032&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003036&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003037&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003038&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003039&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003046&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003047&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003048&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003049&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003050&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003051&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003053&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003065&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003067&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003070&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003071&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003076&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003078&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003080&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003081&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003086&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003088&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003089&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003092&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003093&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003094&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003102&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003104&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003105&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003109&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003111&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003117&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003124&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003125&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003126&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003127&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003130&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003133&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003138&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003141&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003143&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003144&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003145&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003146&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003148&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003155&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003157&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003158&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003159&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003161&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003164&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003165&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003167&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003168&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003169&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003170&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003173&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003174&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003175&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003183&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003186&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003191&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003192&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003195&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003198&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003200&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003203&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003204&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003205&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003207&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003213&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003215&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003217&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003220&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003221&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003224&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003227&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003229&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003234&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003235&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003237&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003264&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003265&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003267&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003269&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003271&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003277&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003280&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003282&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003283&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003284&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003295&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003313&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003323&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003325&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003327&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003329&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003333&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003337&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003338&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003339&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003396&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003421&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17003436&tz=GMT%2B05%3A30",

    ]

    driver = selenium.webdriver.Firefox(executable_path="D:\\Nissan\\geckodriver-v0.16.0-win64(1)\\geckodriver.exe") #Chrome('D:\\Nissan\\chromedriver.exe')

    au = taleo_automation(driver)

    try:
        result = au.get_job_detail(url_list)
        file_name = url_list[0].split('/')[2] + "_fifth.txt"
        with open(file_name, 'w') as outfile:
            json.dump(result, outfile)
    except:
         print(" Problem in :: " )
    # driver.close()
