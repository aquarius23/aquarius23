#!/usr/bin/python
#!coding=utf-8
import string
import stockutils
import stockdb
import stockparser
import stockconfig

class stockmanager():
	parser = stockparser.stock_parser()
	db = stockdb.stockdb()

	def get_stock_list(self):
		return self.parser.get_stock_list()

	def __get_stock_index_jidu(self, name, year, jidu):
		data = self.db.read_data_jidu(name, year, jidu)
		if len(data) <= 0:
			return []
		list = data.split('\n')
		ret = []
		for line in list:
			day_exchange = line.split(',')
			ret.append(day_exchange)
		return ret

	def get_stock_index(self, name):
		today = stockutils.get_date().split('-')
		start = stockconfig.FIG_START_DAY.split('-')
		start_year = string.atoi(start[0])
		start_jidu = (string.atoi(start[1]) + 2) / 3
		end_year = string.atoi(today[0])
		end_jidu = (string.atoi(today[1]) + 2) / 3
		index = []
		while True:
			data = self.__get_stock_index_jidu(name, start_year, start_jidu)
			index.extend(data)
			if(start_year == end_year) and (start_jidu == end_jidu):
				break;
			start_year, start_jidu = stockutils.next_jidu(start_year, start_jidu)
		return index

x = stockmanager()
x = x.get_stock_index('300397')
for i in x:
	print i
