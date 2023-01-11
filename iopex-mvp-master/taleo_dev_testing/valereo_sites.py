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

#sys.setdefaultencoding('utf-8')

class valero_holmiun_page(Page):

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

class valero_automation():

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

    def fetch_value(self):
        self.data = {'no_header': []}
        job = ''
        if self.page.job_title:
            job = [j.text for j in self.page.job_title]
            job = " ".join(job)

        self.data = {'job' : job}
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

    def get_job_detail(self,url):
        self.page = valero_holmiun_page(self.driver, url)
        time.sleep(1)

        #self.page.search.click()
        time.sleep(2)
        self.scrollElementIntoView(self.page.scroll_pos)
        time.sleep(2)

       # self.scrollElementIntoView(self.page.job_elements[0])
        time.sleep(10)
        self.page.job_elements[0]['job_link'].click()
        time.sleep(5)
        result ={}
        current_label = None
        tittle = []
        self.fetch_value()
        next = False #self.check_next()

        while(next):
            print(" NEXT URLS ")
            time.sleep(3)
            next = self.check_next()
            self.fetch_value()

        print("===========================")
        return result


if __name__ == '__main__':
    url = 'https://valero.taleo.net/careersection/2/jobsearch.ftl'
    #url = 'https://caterpillar.taleo.net/careersection/cat+external+cs/jobsearch.ftl' #'https://valero.taleo.net/careersection/2/jobsearch.ftl' #'https://kelloggs.taleo.net/careersection/2/jobdetail.ftl' #''https://www.aflac.com/careers/default.aspx'
    driver = selenium.webdriver.Firefox(executable_path="D:\\Nissan\\geckodriver-v0.16.0-win64(1)\\geckodriver.exe") #Chrome('D:\\Nissan\\chromedriver.exe')
    #driver.maximize_window()
    au = valero_automation(driver)
    au.get_job_detail(url)
    driver.close()
