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

        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001458&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001464&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001474&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001485&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001486&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001488&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001492&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001499&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001501&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001518&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001521&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001522&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001525&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001526&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001551&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001553&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001556&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001575&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001595&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001603&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001606&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001610&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001614&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001616&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001617&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001618&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001629&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001634&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001638&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001656&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001657&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001661&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001667&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001669&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001672&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001677&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001680&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001687&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001689&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001690&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001692&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001693&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001702&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001713&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001723&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001733&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001737&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001742&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001751&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001773&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001785&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001787&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001805&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001816&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001817&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001839&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001845&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001849&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001854&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001858&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001862&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001869&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001883&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001884&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001886&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001888&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001896&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001900&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001901&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001902&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001906&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001916&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001932&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001935&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001939&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001942&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001945&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001954&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001957&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001960&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001963&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001964&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001970&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001976&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001982&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001983&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001985&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001986&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001990&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001992&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001995&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002000&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002001&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002004&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002008&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002009&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002013&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002014&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002015&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002018&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002019&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002021&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002025&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002026&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002028&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002029&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002040&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002041&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002042&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002046&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002047&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002049&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002050&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002062&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002069&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002073&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002077&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002079&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002081&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002082&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002087&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002088&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002094&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002098&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002099&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002119&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002129&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002131&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002132&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002134&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002136&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002142&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002151&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002157&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002161&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002162&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002164&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002169&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002174&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002179&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002187&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002189&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002190&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002202&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002212&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002215&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002218&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002221&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002224&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002226&tz=GMT%2B05%3A30",

    ]

    driver = selenium.webdriver.Firefox(executable_path="D:\\Nissan\\geckodriver-v0.16.0-win64(1)\\geckodriver.exe") #Chrome('D:\\Nissan\\chromedriver.exe')

    au = taleo_automation(driver)

    try:
        result = au.get_job_detail(url_list)
        file_name = url_list[0].split('/')[2] + "_third.txt"
        with open(file_name, 'w') as outfile:
            json.dump(result, outfile)
    except:
         print(" Problem in :: " )
    # driver.close()
