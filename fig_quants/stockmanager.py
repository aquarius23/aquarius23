#!/usr/bin/python
#!coding=utf-8
import time
import string
import stockdb
import stockparser
import stockconfig

def get_date():
	return time.strftime('%Y-%m-%d',time.localtime(time.time()))

def next_jidu(year, jidu):
	if(jidu == 4):
		jidu = 0
		year = year + 1
	jidu = jidu + 1
	return year, jidu

class stockmanager():
	parser = stockparser.stock_parser()
	db = stockdb.stockdb()

	def get_stock_list(self):
		return self.parser.get_stock_list()

	def get_stock_index(self, name):
		today = get_date()
		start = stockconfig.FIG_START_DAY
		print today
		print start

x = stockmanager()
x.get_stock_index('600015')
for i in range(1, 12 + 1):
	jidu = (i + 2) / 3

