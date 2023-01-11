from holmium.core import Page, Element, Elements, ElementMap, Section, Locators, conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import unittest
import selenium
import time
import json

from taleo_site.config import config
print(config.config.get('dev_environment','host'))
from ladders_scrapy.db.db_operations import db_operations

class taleo_holmiun_page(Page):

    no_job = Element(Locators.CSS_SELECTOR, '.titlelinkoff', timeout=20,)


class taleo_automation():

    master_url = db_operations('dev_environment', config).read_input_from_master('taleo')


    def __init__(self, driver):
        self.driver = driver


    def scrollElementIntoView(self, e):
        self.driver.execute_script("arguments[0].scrollIntoView()", e)

    def update_deactive_job(self):
        url_list =  db_operations('dev_environment', config).read_input_from_master('taleo')
        fetched_url =[]
        for url in url_list:
            self.page = taleo_holmiun_page(self.driver, url)
            if self.page.no_job:
                print('deactivwe')
                fetched_url.append(url)
            else:
                print('------------')
        db_operations('dev_environment', config).update_deactive(fetched_url)

if __name__ == '__main__':
    url_list =[
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=0800030",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=140000Q",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=14000D7",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=150009U",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=150009V",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=15000I0",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=15000JJ",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=15000R0",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=15000Y7",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=160002W",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=1600048",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=160004A",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=16000C7",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=16000G9",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=16000J7",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=16000JD",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=16000JF",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=16000JH",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=16000NJ",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=16000NY",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=16000OQ",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=16000OX",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=16000P7",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=16000PT",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=16000Q4",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=16000QK",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=16000R2",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=16000R4",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170000C",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170000D",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170000E",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170000F",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170000I",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170000K",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170000M",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170000R",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170000V",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170001E",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170001Q",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170001X",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=1700026",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170002E",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170002J",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170002T",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=1700034",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=1700036",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=1700039",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170003L",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170003Q",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170003S",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170003Z",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=1700042",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=1700043",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170004A",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170004E",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170004G",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170004M",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170004O",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170004P",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170004S",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170004V",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=1700053",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=1700054",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=1700056",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=1700057",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170005C",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170005D",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170005G",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170005I",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170005L",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170005M",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170005N",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170005S",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=170005U",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=1700061",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=1700063",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=1700064",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=1700065",
    "https://abercrombie.taleo.net/careersection/1.0/jobdetail.ftl?job=1700066",


    ]

    driver = selenium.webdriver.Firefox(executable_path="D:\\Nissan\\geckodriver-v0.16.0-win64(1)\\geckodriver.exe") #Chrome('D:\\Nissan\\chromedriver.exe')

    au = taleo_automation(driver)

#    try:
    result = au.update_deactive_job()

