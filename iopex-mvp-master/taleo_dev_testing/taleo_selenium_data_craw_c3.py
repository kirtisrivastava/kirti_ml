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

        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002235&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002244&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002256&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002257&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002264&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002272&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002276&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002293&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002297&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002302&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002305&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002306&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002307&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002313&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002317&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002319&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002326&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002345&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002346&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002359&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002362&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002364&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002365&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002367&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002369&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002371&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002373&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002374&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002382&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002386&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002400&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002408&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002409&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002413&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002416&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002418&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002425&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002430&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002441&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002442&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002443&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002447&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002448&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002457&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002458&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002459&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002462&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002469&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002470&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002481&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002482&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002484&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002488&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002489&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002503&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002505&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002507&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002508&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002512&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002513&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002515&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002518&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002522&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002523&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002524&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002525&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002530&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002531&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002535&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002538&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002539&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002540&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002543&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002545&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002547&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002549&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002553&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002554&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002556&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002558&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002559&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002560&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002561&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002565&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002566&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002567&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002568&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002569&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002571&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002572&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002573&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002574&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002576&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002580&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002584&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002590&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002591&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002593&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002595&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002602&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002604&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002605&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002606&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002609&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002612&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002615&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002616&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002620&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002621&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002624&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002627&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002629&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002631&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002633&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002636&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002638&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002641&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002643&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002646&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002647&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002652&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002655&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002656&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002658&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002661&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002663&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002671&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002672&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002673&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002679&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002684&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002693&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002701&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002704&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002708&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002710&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002712&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002731&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002733&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002735&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002736&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002737&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002738&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002741&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002748&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002750&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002751&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002752&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002754&tz=GMT%2B05%3A30",
        "https://mckesson.taleo.net/careersection/ex/jobdetail.ftl?job=17002761&tz=GMT%2B05%3A30",

    ]

    driver = selenium.webdriver.Firefox(executable_path="D:\\Nissan\\geckodriver-v0.16.0-win64(1)\\geckodriver.exe") #Chrome('D:\\Nissan\\chromedriver.exe')

    au = taleo_automation(driver)

    try:
        result = au.get_job_detail(url_list)
        file_name = url_list[0].split('/')[2] + "_fourth.txt"
        with open(file_name, 'w') as outfile:
            json.dump(result, outfile)
    except:
         print(" Problem in :: " )
    # driver.close()
