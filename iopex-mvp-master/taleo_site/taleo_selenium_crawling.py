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

    master_url = db_operations('dev_environment', config).read_input_from_master('taleo')


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
        url_list =set(url_list)
        print(self.master_url)
        url_list = url_list - set(self.master_url)
        fetched_url =[]

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
                fetched_url.append(url)
            except:
                print(" error in :: ", url)
        db_operations('dev_environment', config).insert_in_to_master(fetched_url, 'taleo')
        return self.result


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

    try:
        result = au.get_job_detail(url_list)
        file_name = url_list[0].split('/')[2] + "_first.txt"
        with open(file_name, 'w') as outfile:
            json.dump(result, outfile)
    except:
        print(" Problem in :: " )
        driver.close()
