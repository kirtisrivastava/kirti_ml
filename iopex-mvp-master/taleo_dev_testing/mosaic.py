from bs4 import BeautifulSoup
from holmium.core import Page, Element, Elements, ElementMap, Section, Locators, conditions, TestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import unittest
import selenium
import re
import time

import sys

#sys.setdefaultencoding('utf-8')

class mosaic_holmiun_page(Page):

    search = Element(Locators.CSS_SELECTOR, '.menu-items li a', timeout=20,)
    job_elements = Elements(Locators.CSS_SELECTOR, "table .contentlist tr.ftlcopy.ftlrow",
                               only_if=lambda el: el[0].is_displayed(), timeout=20, value=lambda el: {
            'job_link': el.find_element_by_css_selector('.titlelink a'),
        })
    #job_elements_2 = Elements(Locators.CSS_SELECTOR, '#jobs tbody tr', timeout=20)
    job_elements_2 = Elements(Locators.CSS_SELECTOR, "#jobs tbody tr",
                            only_if=lambda el: el[0].is_displayed(), timeout=20, value=lambda el: {
            'job_link': el.find_element_by_css_selector('a') if  el.find_element_by_css_selector('a')
                        else None
        })

    scroll_pos = Element(Locators.CSS_SELECTOR, '.tablelist', timeout=20)
    job_details = Elements(Locators.CSS_SELECTOR, 'p', timeout=20)
    job_title = Element(Locators.CLASS_NAME, 'contentlinepanel', timeout=5)
    pager_link = Elements(Locators.CLASS_NAME, 'pagerlink', timeout=10)
    all_div = Elements(Locators.CSS_SELECTOR, '.contentlinepanel', timeout=10)
    return_to_home = Element(Locators.ID, 'requisitionDescriptionInterface.backAction', timeout=10)
    next_button = Element(Locators.ID, 'next', timeout=10)

class mosaic_automation(TestCase):

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

    def fetch_value_and_back_to_home(self, next_pos):
        print("--------------------- >>")
        self.page.job_elements_2[next_pos]['job_link'].click()
        time.sleep(5)
        try:
            self.fetch_value()
        except:
            print("problem in lelelel ")
            pass
        self.assertTrue(self.page.return_to_home)
        time.sleep(2)
        self.page.return_to_home.click()
        print("-------- RERTUREN ------------>>")
        time.sleep(5)

    def fetch_value(self):
        self.data = {'no_header': []}
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
                    print(" HEADER :: ", header)

                    for desc_tag in self.DESCRIPTION_TAG:
                        description =  divs.find_elements_by_css_selector(desc_tag)


                        if description:
                            #self.scrollElementIntoView(description)
                            time.sleep(2)

                            try:
                                description = [desc.text for desc in description]
                            except:
                                print(" Missing  =============================> ")
                                description = [' missing ']
                            description = ' '.join(description)
                            print("HEADER ", self.current_header,  self.data)
                            self.data[self.current_header] = self.data[self.current_header] + " " +str(description)
                            print(" Description  ::", self.data)

        self.result.append(self.data)

    def get_job_detail(self,url):
        self.page = mosaic_holmiun_page(self.driver, url)
        time.sleep(5)
        next = True
        while(next):
            no_of_jobs = len(self.page.job_elements_2)
            for job in range(0, no_of_jobs):
                self.fetch_value_and_back_to_home(job)

            self.assertTrue(self.page.next_button)
            if self.page.next_button.get_attribute('class'):
                print(" NO NEXT exit ")
                next = False

            else:
                print(" NEXT  ")
                self.page.next_button.click()

        self.fetch_value()
        next = self.check_next()



if __name__ == '__main__':
    url = 'http://mosaic.taleo.net/careersection/cdn_corporate/jobsearch.ftl'
    driver = selenium.webdriver.Firefox(executable_path="D:\\Nissan\\geckodriver-v0.16.0-win64(1)\\geckodriver.exe") #Chrome('D:\\Nissan\\chromedriver.exe')
    #driver.maximize_window()
    au = mosaic_automation(driver)
    au.get_job_detail(url)
    driver.close()
