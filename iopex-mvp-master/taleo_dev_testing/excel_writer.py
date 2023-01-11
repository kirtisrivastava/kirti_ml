import time

import xlrd
import xlsxwriter
import datetime

class excel_writer(object):

    def write_result_xlsx(self, site, input_records):

        workbook = xlsxwriter.Workbook(site + '_' + str(datetime.datetime.now()).replace(':', '-') + 'result.xlsx')
        worksheet = workbook.add_worksheet()
        row = 0
        for key, value in input_records.iteritems():
            row = row + 1
            col =1
            for v in value:
                worksheet.write(row, col, v)
                col = col + 1