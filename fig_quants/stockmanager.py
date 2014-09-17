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

	def __get_stock_index_jidu(self, name, year, jidu):
		data = self.db.read_data_jidu(name, year, jidu)
		print data

	def get_stock_index(self, name):
		today = get_date().split('-')
		start = stockconfig.FIG_START_DAY.split('-')
		start_year = string.atoi(start[0])
		start_jidu = (string.atoi(start[1]) + 2) / 3
		end_year = string.atoi(today[0])
		end_jidu = (string.atoi(today[1]) + 2) / 3
		while True:
			self.__get_stock_index_jidu(name, start_year, start_jidu)
			if(start_year == end_year) and (start_jidu == end_jidu):
				break;
			start_year, start_jidu = next_jidu(start_year, start_jidu)

x = stockmanager()
x.get_stock_index('600050')
