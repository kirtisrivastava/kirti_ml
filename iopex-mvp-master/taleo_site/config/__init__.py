print('__innit_config_')
import os
import sys
project_path = os.path.dirname( os.path.dirname( os.path.abspath(__file__)))
print(" Project Path :: ", project_path)
project_path = project_path.split('\\')
project_path = '\\'.join(project_path)
print(" project Payh final :: ", project_path)
sys.path.append(project_path)

from ladders_scrapy.config import config