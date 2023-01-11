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

        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=16010324&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=16010327&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=16010329&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=16010358&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=16010383&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=16010393&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=16010462&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=16010463&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=16010467&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=16010482&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=16010528&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=16010532&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=16010630&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000024&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000029&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000039&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000045&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000065&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000073&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000127&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000161&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000164&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000165&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000182&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000216&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000244&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000268&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000269&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000274&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000296&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000301&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000304&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000315&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000318&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000343&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000359&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000379&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000408&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000422&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000430&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000432&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000434&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000450&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000502&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000528&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000532&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000535&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000536&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000541&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000567&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000574&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000589&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000591&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000606&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000608&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000621&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000667&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000671&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000690&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000692&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000708&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000719&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000731&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000745&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000756&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000760&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000767&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000795&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000799&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000812&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000834&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000836&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000840&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000846&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000853&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000874&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000880&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000892&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000921&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000922&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000923&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000928&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000944&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000951&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000962&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000967&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000972&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000975&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000977&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000985&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000995&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17000997&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001002&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001018&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001023&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001025&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001031&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001034&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001035&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001036&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001037&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001038&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001042&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001065&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001076&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001080&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001127&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001132&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001136&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001152&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001171&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001193&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001212&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001216&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001222&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001230&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001240&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001252&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001254&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001274&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001279&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001281&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001282&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001283&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001293&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001299&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001308&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001311&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001327&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001328&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001330&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001346&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001355&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001357&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001362&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001365&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001366&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001367&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001369&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001394&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001402&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001425&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001440&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001442&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001445&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001450&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001451&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001453&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001456&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17001457&tz=GMT%2B05%3A30",

    ]

    driver = selenium.webdriver.Firefox(executable_path="D:\\Nissan\\geckodriver-v0.16.0-win64(1)\\geckodriver.exe") #Chrome('D:\\Nissan\\chromedriver.exe')

    au = taleo_automation(driver)

    try:
        result = au.get_job_detail(url_list)
        file_name = url_list[0].split('/')[2] + "_second.txt"
        with open(file_name, 'w') as outfile:
            json.dump(result, outfile)
    except:
         print(" Problem in :: " )
    # driver.close()
