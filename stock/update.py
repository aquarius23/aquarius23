#!/usr/bin/python
#!coding=utf-8

import string
import time
import stockdb
import stockparser

def stockloop(stock_db, table, list):
	print 'start ' + table + ' ----------------------'
	list.reverse()
	date = stock_db.get_newest_date(table)
	for index in list:
		if date == 'None' or cmp(index[0], date) > 0:
			print index
			stock_db.insert(table, index[0], index[1], index[3], index[2], index[4], index[5][0:-2], index[6])
		
def mainloop():
	year = 2011
	jidu = 1
	stock_db = stockdb.stockdb()
	db = 'stock' + str(year) + '.db'
	db = '/mnt/git/stock/' + db
	stock_db.open(db)
	newest = stockparser.get_index_list('000001', year, jidu, 0)
	if len(newest) > 0:
		newest = newest[0]
		date = stock_db.get_newest_date('sh000001')
		if date == 'None' or cmp(newest[0], date) > 0:
			stocklist = stockparser.get_stock_list()
			stockloop(stock_db, 'sz399001', stockparser.get_index_list('399001', year, jidu, 0))
			for stock in stocklist:
				stockloop(stock_db, 'st' + stock, stockparser.get_index_list(stock, year, jidu, 1))
			stockloop(stock_db, 'sh000001', stockparser.get_index_list('000001', year, jidu, 0))
	stock_db.close()

