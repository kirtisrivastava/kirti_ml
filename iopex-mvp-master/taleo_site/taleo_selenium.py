from holmium.core import Page, Element, Elements, ElementMap, Section, Locators, conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import unittest
import selenium
import time
import json


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

    HEADER_TAG = ['h2', 'strong', 'b', 'b font', '.subtitle']
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
        return self.result

    def get_job_detail(self,url):
        self.page = taleo_holmiun_page(self.driver, url)
        time.sleep(1)

        #self.page.search.click()
        time.sleep(2)
        self.scrollElementIntoView(self.page.scroll_pos)
        time.sleep(2)

       # self.scrollElementIntoView(self.page.job_elements[0])
        time.sleep(10)
        self.page.job_elements[0]['job_link'].click()
        time.sleep(5)
        #print " Detail" , self.page.job_details
        result ={}
        current_label = None
        tittle = []

        print(len(self.page.all_div))
        self.fetch_value()
        next = self.check_next()
        n = 0
        next = False
        while(next):
            time.sleep(3)
            next = self.check_next()
            self.fetch_value()
            n=n+1
            if n==1:
                next = False

        return json.dumps(self.result)


if __name__ == '__main__':
    url_list =[
        #'https://valero.taleo.net/careersection/2/jobsearch.ftl'
        'https://alliancedata.taleo.net/careersection/alliancedata/jobsearch.ftl?lang=en'
    ]
    url_list_old = [
            'https://valero.taleo.net/careersection/2/jobsearch.ftl',
            # 'http://mosaic.taleo.net/careersection/cdn_corporate/jobsearch.ftl',
            # 'https://abercrombie.taleo.net/careersection/1.0/jobsearch.ftl',
            # 'http://aflac.taleo.net/careersection/external/jobsearch.ftl',
            # 'https://alliancedata.taleo.net/careersection/alliancedata/jobsearch.ftl?lang=en',
            # 'https://caterpillar.taleo.net/careersection/cat+external+cs/jobsearch.ftl',
            # 'https://easternbank.taleo.net/careersection/ex/jobsearch.ftl',
            # 'https://emerson.taleo.net/careersection/ex/jobsearch.ftl?lang=en',
            # 'http://www.gendex.com/careers',
            # 'https://manitowoc.taleo.net/careersection/prof_engineer/jobsearch.ftl',
            # 'https://pru.taleo.net/careersection/2/jobsearch.ftl',
    ]
    driver = selenium.webdriver.Firefox(executable_path="D:\\Nissan\\geckodriver-v0.16.0-win64(1)\\geckodriver.exe") #Chrome('D:\\Nissan\\chromedriver.exe')

    au = taleo_automation(driver)
    for url in url_list:
        print("==================== :: ", url)
        #try:
        result = au.get_job_detail(url)
        file_name = url.split('/')[2] + "_fix.json"
        with open(file_name, 'w') as outfile:
            json.dump(result, outfile)
        # except:
        #     print(" Problem in :: " , url)
    driver.close()
