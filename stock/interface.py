#!/usr/bin/python
#!coding=utf-8

import time
import string
import stockdb
import stockparser

def get_db_list(start, end):
	db_list = []
	start = string.atoi(start.split('-')[0])
	end = string.atoi(end.split('-')[0])
	for i in range(start, end + 1):
		db_list.append(i)
	return db_list

def get_db_kv(list):
	kv = {}
	for i in list:
		file = 'stock' + str(i) + '.db'
		db_real = stockdb.stockdb()
		db_real.open(file)
		kv[i] = db_real
	return kv

def get_table_name(index, real_stock):
	if real_stock:
		return 'st' + index
	elif index[0] == '0':
		return 'sh' + index
	else:
		return 'sz' + index

class stock_al():
	start_day = '2006-01-01'
	end_day = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	db_list = get_db_list(start_day, end_day)
	db_key = get_db_kv(db_list)

	def get_all_list(self, index, real_stock):
		all = []
		table = get_table_name(index, real_stock)
		for year in self.db_list:
			all.extend(self.db_key[year].get_all_list(table, 0))
		return all

	def get_all_list_from_date(self, date, index, real_stock):
		all = []
		year = string.atoi(date.split('-')[0])
		table = get_table_name(index, real_stock)
		all.extend(self.db_key[year].get_all_list_from_date(table, date, 0))
		year += 1
		end = self.db_list[-1]
		if year <= end:
			for year2 in range(year, end + 1):
				all.extend(self.db_key[year2].get_all_list(table, 0))
		return all

	def get_date_list(self, index, real_stock):
		all = []
		table = get_table_name(index, real_stock)
		for year in self.db_list:
			all.extend(self.db_key[year].get_date_list(table, 0))
		return all
	
	def get_date_list_from_date(self, date, index, real_stock):
		all = []
		year = string.atoi(date.split('-')[0])
		table = get_table_name(index, real_stock)
		all.extend(self.db_key[year].get_date_list_from_date(table, date, 0))
		year += 1
		end = self.db_list[-1]
		if year <= end:
			for year2 in range(year, end + 1):
				all.extend(self.db_key[year2].get_date_list(table, 0))
		return all

	def get_stock_list(self):
		return stockparser.get_stock_list();
	
	def get_stock_key(self):
		return stockparser.get_stock_key()

