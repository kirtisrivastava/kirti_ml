Overview:
Scrapy spider to crawl websites under three ATS(lever,taleo and ICIMS) systems.
URL is stored in MYSQL database to achieve delta fetch
Output is given in JSON format

Software Requirements

Python 3.x latest version
Python IDE (ex:Pycharm)
mysql server

Python Library dependencies
scrapy
selenium
holmium.core
mysqlclient

Browser Dependencies
Firefox latest version
geckodriver(Firefox Driver)

Pip command to install a python library
pip install <library-name>
         or
pip install <library-name>==<version number>
        or
pip install <text-file with python libraries names> #Refer requirements.text in Git


Execution Steps:

1)Install Python 3.x, Python IDE
2)Install python libraries
3)Install MySQl server and execute table DDL in tabel_setup.sql
4)Edit conif.ini in "ladders_scrapy/config/config.ini" as per the local db setup
5)Sync latest code version from Git
6)To run Lever/Icims Spider use following command in cmd/terminal
scrapy runspider <project path + ladders_scrapy/spiders><python-code.py> -o output.json

To RUN TALEO :
    config the geckodriver path inside the following two files , find the configuration path by searching "geckodriver"
    in the py files

    config the db set up in \taleo_site\config\config.ini

    1)To run Taleo Spider 1st pattern, Right click on the "ladders_project\taleo_site\taleo_selenium.py" and run
            for running other company need to change the company URL in "url_list" variable, sample url are given in
            "url_list_old" vraible, refer in "__main__"

    2)To run Taleo Spider 2nd pattern, Right click on the "ladders_project\taleo_site\taleo_selenium_crawling.py" and run
            for running other job url need to change the job URL in "url_list" variable,  vraible, refer in "__main__"

            for getting job url run "taleo_data.py" in "\ladders_scrapy\data" and give generated job urls to previous
            step.

# Notes for setting on a Mac/OSX
1. We used brew to install mysql -- otherwise it was difficult to get the mysqlclient installed properly.
2. To run: navigate to the ladders_scrapy directory and run the following:
PYTHONPATH=../ scrapy runspider ./spiders/lever_spider.py -o lever-2017-0524-0804.json

# Notes for setting on a CentOS7 on AWS:
1. I installed MariaDB, but everything works with mysql clients.  (sudo systemctl start mariadb)
2. admin-qa-1.aws.theladders.com is the server for now.
3. Temporarily, I have set up cron to run every 10 minutes: /home/ksandine/run-lever.sh



