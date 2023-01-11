from holmium.core import Page, Element, Elements, ElementMap, Section, Locators, conditions, TestCase
from selenium.webdriver.support import expected_conditions as EC
import selenium
import time
import json
import sys, traceback

class taleo_pattern_two_holmiun_page(Page):

    search = Element(Locators.CSS_SELECTOR, '.menu-items li a', timeout=20,)
    job_elements = Elements(Locators.CSS_SELECTOR, "table .contentlist tr.ftlcopy.ftlrow",
                               only_if=lambda el: el[0].is_displayed(), timeout=20, value=lambda el: {
            'job_link': el.find_element_by_css_selector('.titlelink a'),
        })
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

class pattern_two_automation(TestCase):

    HEADER_TAG = ['h2', 'b', 'strong']
    DESCRIPTION_TAG = ['p', 'li', 'span.text']

    def __init__(self, driver):
        self.driver = driver
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
                    time.sleep(1)
                    return True
        return next_page

    def fetch_value_and_back_to_home(self, next_pos):
        print("--------------------- >>")
        time.sleep(1)
        url = self.page.job_elements_2[next_pos]['job_link'].get_attribute('href')
        self.page.job_elements_2[next_pos]['job_link'].click()
#
        try:
            self.fetch_value(url)
        except Exception as e:
            print("problem in data ::", e)
            traceback.print_tb(sys.exc_info(), limit=1, file=sys.stdout)
            pass
        self.assertTrue(self.page.return_to_home)
        time.sleep(1)
        self.page.return_to_home.click()
        print("-------- RERTUREN ------------>>")
        time.sleep(1)

    def fetch_value(self, url=None):
        data = {'no_header': [], 'url': url}
        time.sleep(5)
        for divs in self.page.all_div:
            #check for header
            header = None
            for head_tag in self.HEADER_TAG:
                time.sleep(1)
                header = divs.find_elements_by_css_selector(head_tag)
                if header and str(header[0].text).strip() != '':
                    header = divs.find_element_by_css_selector(head_tag)
                    header = header.text
                    self.current_header = str(header)
                    data[str(self.current_header)] = ""
                    #print(" HEADER :: ", header)

                    for desc_tag in self.DESCRIPTION_TAG:
                        description =  divs.find_elements_by_css_selector(desc_tag)


                        if description:
                            #self.scrollElementIntoView(description)
                            #time.sleep(2)
                            try:
                                description = [desc.text for desc in description]
                            except:
                               # print(" Missing  =============================> ")
                                description = [' missing ']
                                traceback.print_tb(sys.exc_info(), limit=1, file=sys.stdout)
                            description = ' '.join(description)
                            #print("HEADER ", self.current_header,  data)
                            data[self.current_header] = data[self.current_header] + " " +str(description)
                            #print(" Description  ::", data)

        self.result.append(data)

    def get_job_detail(self,url):
        self.page = taleo_pattern_two_holmiun_page(self.driver, url)
        time.sleep(1)
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
        #self.fetch_value()
        next = self.check_next()
        print(self.result)
        return self.result



if __name__ == '__main__':
    url_list = [
        'http://mosaic.taleo.net/careersection/cdn_corporate/jobsearch.ftl'
    ]

    url_list_group =[
        'http://mosaic.taleo.net/careersection/cdn_corporate/jobsearch.ftl',
        'https://engie.taleo.net/careersection/10550/jobsearch.ftl',
        'https://nordstrom.taleo.net/careersection/2/jobsearch.ftl?'
    ]
    driver = selenium.webdriver.Firefox(
        executable_path="D:\\Nissan\\geckodriver-v0.16.0-win64(1)\\geckodriver.exe")  # Chrome('D:\\Nissan\\chromedriver.exe')
    au = pattern_two_automation(driver)
    for url in url_list:
        print(" current Url :: ", url)
        file_name = url.split('/')[2] + ".txt"
        try:
            result = au.get_job_detail(url)
            with open(file_name, 'w') as outfile:
                json.dump(result, outfile)
        except Exception as e:
            with open(file_name, 'w') as outfile:
                json.dump(au.result, outfile)
            print('problem in ur :: ', url, e, sys.exc_info()[0])
            traceback.print_tb(sys.exc_info(), limit=1, file=sys.stdout)

    driver.close()
