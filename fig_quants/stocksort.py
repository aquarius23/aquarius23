#!/usr/bin/python
#!coding=utf-8
import stockmanager
import string
import stockdb

def get_vol():
	manager = stockmanager.stockmanager()
	list = manager.get_stock_list()
	result = []
	for stock in list:
		print stock
		e = manager.get_stock_index(stock)
		if e == []:
			continue
		sum = 0
		count = 0
		result_day = []
		result_day.append(str(stock))
		for day in e:
			volume = day[6]
			sum = sum + volume
			count = count + 1
		result_day.append(str(sum / count))
		result.append(result_day)
	result.sort(cmp = lambda x,y: cmp(x[1],y[1]))
	return result

def get_sort(up_sort):
	db = stockdb.stockdb()
	data = db.read_data_crf('vol_sort')
	list = data.split('\n')
	ret = []
	for line in list:
		day_exchange = line.split(',')
		day_exchange[1] = string.atoi(day_exchange[1])
		ret.append(day_exchange)
	if up_sort == 1:
		ret.sort(cmp = lambda x,y: cmp(x[1],y[1]))
	else:
		ret.sort(cmp = lambda x,y: cmp(x[1],y[1]), reverse = True)
	return ret
