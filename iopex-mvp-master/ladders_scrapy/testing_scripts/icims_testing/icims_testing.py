import json
import re
import time
import xlsxwriter

import datetime

class icims_testing(object):

    def write_result_xlsx(self, input_records):

        workbook = xlsxwriter.Workbook(str(datetime.datetime.now()).replace(':', '-') + 'result.xlsx')
        worksheet = workbook.add_worksheet()
        row = 0
        for rec in input_records:
            if rec:
                row = row + 1
                col = 1
                for v in rec:
                    worksheet.write(row, col, v)
                    col = col + 1

    def write_list_to_xlsx(self, input_records):

        workbook = xlsxwriter.Workbook(str(datetime.datetime.now()).replace(':', '-') + 'url_result.xlsx')
        worksheet = workbook.add_worksheet()
        row = 0
        for rec in input_records:
            row = row + 1
            col = 1
            worksheet.write(row, col, rec)

    def get_url(self):
        with open("url.json") as icims_json_file:
            crawled_data = json.loads(icims_json_file.read())
        all_urls = []
        for rec in crawled_data:
            all_urls.append(rec['url'])
        self.write_result_xlsx( all_urls)

    def analyse_fields(self):
        crawled_data = None
        with open("icims.json") as icims_json_file:
            crawled_data = json.loads(icims_json_file.read())
        all_keys = []
        for rec in crawled_data:
            #print rec.keys()
            t = ['other_details', 'table_content']
            keys_list =[rec['url'][0]]
            for k in t:
               # print type(rec[k])
                temp =[]
                if isinstance(rec[k], list):
                    for s in rec[k]:
                      #  print s.keys()
                        keys_list.append(list(s.keys())[0])
                #keys_list.append(temp)
            all_keys.append(keys_list)
        for i in all_keys:
            print("------------------")
            print(i)
        print((all_keys.sort()))
        #$self.write_result_xlsx(all_keys)

if __name__ == '__main__':
    #icims_testing().analyse_fields()
    icims_testing().get_url()