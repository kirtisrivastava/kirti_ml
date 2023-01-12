import time 
import MySQLdb
from random import randint
import csv
import pymysql

def training_data(Db_connection,username,password,database,sql):
	
	db = pymysql.connect(Db_connection,username,password,database,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
	
	cursor = db.cursor()
	sql = sql
	print sql
	cursor.execute(sql)

	results = cursor.fetchall()
	
	return results





