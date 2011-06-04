#!/usr/bin/python
#!coding=utf-8

import string
import time
import stockdb
import stockparser

start_day = '2011-01-01'
end_day = time.strftime('%Y-%m-%d',time.localtime(time.time()))
stock_db = stockdb.stockdb()
stock_db.open('stock2011.db')
stocklist = stockparser.get_stock_list()

def stockloop(table, list):
	print 'start ' + table + ' ----------------------'
	list.reverse()
	date = stock_db.get_newest_date(table)
	for index in list:
		if date == 'None' or cmp(index[0], date) > 0:
			print index
			stock_db.insert(table, index[0], index[1], index[3], index[2], index[4], index[5][0:-2], index[6])
		

def jiduloop(year, jidu):
	stockloop('sz399001', stockparser.get_index_list('399001', year, jidu, 0))
	for stock in stocklist:
		stockloop('st' + stock, stockparser.get_index_list(stock, year, jidu, 1))
	stockloop('sh000001', stockparser.get_index_list('000001', year, jidu, 0))

def mainloop():
	db_day = stock_db.get_newest_date('sh000001')
	if db_day != 'None':
		start = db_day
	else:
		start = start_day
	
	start = start.split('-')
	s_y = string.atoi(start[0])
	s_j = (string.atoi(start[1]) - 1) / 3 + 1
	
	end = end_day.split('-')
	e_y = string.atoi(end[0])
	e_j = (string.atoi(end[1]) - 1) / 3 + 1

	for i in range(s_y, e_y + 1):
		if i == s_y:
			s = s_j
		else:
			s = 1

		if i == e_y:
			e = e_j
		else:
			e = 4

		for j in range(s, e + 1):
			print 'start parser year = ' + str(i) + '  jidu = ' + str(j)
			jiduloop(i, j)

mainloop()
stock_db.close()
