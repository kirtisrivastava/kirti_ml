from ladders_scrapy.db.db_connection import db_connection


class db_operations(object):

    def __init__(self, env="iopex_server", config=None):
        self.env = env
        self.db = db_connection(self.env, config)
        self.db = self.db.get_connection()
        self.cursor = self.db.cursor()

    def insert_in_to_master(self, input_rec,ats):
        for rec in input_rec:
            self.cursor.execute("""INSERT INTO crawl_urls (url, flag, company_name,ats) VALUES ('%s', '%s', '%s','%s')"""%
                            (rec, 'ACTIVE', rec.split('/')[2],ats))
        self.db.commit()
        self.db.close()

    def read_input_from_master(self, ats):
        statement = "select url from crawl_urls where ats ='" + ats + "'"
        self.cursor.execute(statement)
        records = self.cursor.fetchall()
        self.db.close()
        records = [url[0] for url in records]
        return records

    def update_deactive(self,urls):
        print("deactivating~~~~~~~~~~~~~~~~~~",len(urls))
        for url in urls:
            statement = """update crawl_urls set flag = 'INACTIVE' where url = '%s'"""% (url)
            self.cursor.execute(statement)
        self.db.close()

    def deactive_lever(self,urls,ats):
        deactive_url_list=[]
        statement = "select url from crawl_urls where ats ='"+ats+"'"
        self.cursor.execute(statement)
        records = self.cursor.fetchall()
        dbrecords = [url[0] for url in records]
        deactive_url_list.extend(list(set(dbrecords) - set(urls)))
        print("deactivating~~~~~~~~~~~~~~~~~~", len(deactive_url_list))
        for url in deactive_url_list:
            statement = """update crawl_urls set flag ='INACTIVE' where url = '%s'""" % (url)
            self.cursor.execute(statement)
        self.db.close()




