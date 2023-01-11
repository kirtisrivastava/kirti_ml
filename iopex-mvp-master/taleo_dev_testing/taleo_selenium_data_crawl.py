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
    "https://chp.tbe.taleo.net/chp04/ats/careers/v2/viewRequisition?org=KMMG&cws=46&rid=1414",
"https://chp.tbe.taleo.net/chp04/ats/careers/v2/viewRequisition?org=KMMG&cws=46&rid=1419",
"https://chp.tbe.taleo.net/chp04/ats/careers/v2/viewRequisition?org=KMMG&cws=46&rid=1415",
"https://chp.tbe.taleo.net/chp04/ats/careers/v2/viewRequisition?org=KMMG&cws=46&rid=1418",
"https://chp.tbe.taleo.net/chp04/ats/careers/v2/viewRequisition?org=KMMG&cws=46&rid=1407",
"http://chk.tbe.taleo.net/chk06/ats/careers/requisition.jsp?org=MOBITV&cws=1&rid=1901",
"http://chk.tbe.taleo.net/chk06/ats/careers/requisition.jsp?org=MOBITV&cws=1&rid=1902",
"http://chk.tbe.taleo.net/chk06/ats/careers/requisition.jsp?org=MOBITV&cws=1&rid=1900",
"http://chc.tbe.taleo.net/chc01/ats/careers/requisition.jsp?org=APRIVA&cws=1&rid=323",
"http://chc.tbe.taleo.net/chc01/ats/careers/requisition.jsp?org=APRIVA&cws=1&rid=308",
"http://chc.tbe.taleo.net/chc01/ats/careers/requisition.jsp?org=APRIVA&cws=1&rid=233",
"http://chc.tbe.taleo.net/chc01/ats/careers/requisition.jsp?org=APRIVA&cws=1&rid=267",
"http://chc.tbe.taleo.net/chc01/ats/careers/requisition.jsp?org=APRIVA&cws=1&rid=322",
"http://chp.tbe.taleo.net/chp03/ats/careers/requisition.jsp?org=DREAMBOX&cws=1&rid=294",
"http://chp.tbe.taleo.net/chp03/ats/careers/requisition.jsp?org=DREAMBOX&cws=1&rid=295",
"http://chp.tbe.taleo.net/chp03/ats/careers/requisition.jsp?org=DREAMBOX&cws=1&rid=296",
"http://chp.tbe.taleo.net/chp03/ats/careers/requisition.jsp?org=DREAMBOX&cws=1&rid=297",
"http://chp.tbe.taleo.net/chp03/ats/careers/requisition.jsp?org=DREAMBOX&cws=1&rid=293",
"http://chp.tbe.taleo.net/chp03/ats/careers/requisition.jsp?org=DREAMBOX&cws=1&rid=291",
"http://chp.tbe.taleo.net/chp03/ats/careers/requisition.jsp?org=DREAMBOX&cws=1&rid=298",
"http://chp.tbe.taleo.net/chp03/ats/careers/requisition.jsp?org=DREAMBOX&cws=1&rid=284",
"http://chp.tbe.taleo.net/chp03/ats/careers/requisition.jsp?org=DREAMBOX&cws=1&rid=273",
"http://chp.tbe.taleo.net/chp03/ats/careers/requisition.jsp?org=DREAMBOX&cws=1&rid=281",


    ]

    driver = selenium.webdriver.Firefox(executable_path="D:\\Nissan\\geckodriver-v0.16.0-win64(1)\\geckodriver.exe") #Chrome('D:\\Nissan\\chromedriver.exe')

    au = taleo_automation(driver)

    try:
        result = au.get_job_detail(url_list)
        file_name = url_list[0].split('/')[2] + "_first.txt"
        with open(file_name, 'w') as outfile:
            json.dump(result, outfile)
    except:
         print(" Problem in :: " )
    # driver.close()
