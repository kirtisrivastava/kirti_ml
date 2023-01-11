import MySQLdb
from ladders_scrapy.config import config


class db_connection(object):

    def __init__(self, env='iopex_server', config_obj = None):

        config_obj = config
        if config_obj:
            config_obj = config_obj

        self.host = config_obj.config.get(env,'host')
        self.user = config_obj.config.get(env,'user')
        self.password = config_obj.config.get(env,'password')
        self.db = config_obj.config.get(env,'db')

    def get_connection(self):
        db = MySQLdb.connect(self.host, self.user, self.password, self.db)
        return db