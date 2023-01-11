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


class taleo_holmiun_page(Page):

    search = Element(Locators.CSS_SELECTOR, '.menu-items li a', timeout=20,)
    job_elements_2 = Elements(Locators.CSS_SELECTOR, "#jobs tbody tr",
                            only_if=lambda el: el[0].is_displayed(), timeout=20, value=lambda el: {
            'job_link': el.find_element_by_css_selector('a') if  el.find_element_by_css_selector('a')
                        else None
        })
    job_elements_3 = Elements(Locators.CSS_SELECTOR, "#multilineListContainer ul li",
                              only_if=lambda el: el[0].is_displayed(), timeout=20, value=lambda el: {
            'job_link': el.find_element_by_css_selector('a') if el.find_element_by_css_selector('a')
            else None
        })
    job_elements_4 = Elements(Locators.CSS_SELECTOR, "td a",timeout=10)
    next_button = Element(Locators.ID, 'next', timeout=10)


class mosaic_data(TestCase):

    def __init__(self):
        self.url = 'https://chk.tbe.taleo.net/chk05/ats/careers/searchResults.jsp?org=CMEGROUP&cws=1'
        self.driver = selenium.webdriver.Firefox(
            executable_path="D:\\Nissan\\geckodriver-v0.16.0-win64(1)\\geckodriver.exe")

    def get_url_by_a_tag(self):
        self.page = taleo_holmiun_page(self.driver, self.url)
        for link in self.page.job_elements_4:
            print((link.get_attribute('href')))

    def get_start_urls(self):
        self.page = taleo_holmiun_page(self.driver, self.url)


        next = True
        link_list = []
        while (next):
            time.sleep(15)
            no_of_jobs = len(self.page.job_elements_3)
            print(no_of_jobs)

           # urls = [link_list.append(link['job_link'].get_attribute('href')) for link in self.page.job_elements_2]
            for link in self.page.job_elements_3:
                print((link['job_link'].get_attribute('href')))
                link_list.append(link['job_link'].get_attribute('href'))

            if self.page.next_button.get_attribute('class'):
                next = False

            else:
                self.page.next_button.click()
        return link_list

if __name__ == '__main__':
    url = 'https://mckesson.taleo.net/careersection/ex/jobsearch.ftl'
    #driver = selenium.webdriver.Firefox(executable_path="D:\Nissan\geckodriver-v0.16.0-win64(1)\geckodriver.exe") #Chrome('D:\\Nissan\\chromedriver.exe')
    #driver.maximize_window()
    au = mosaic_data()
    #au.get_start_urls()
    au.get_url_by_a_tag()
    #driver.close()
