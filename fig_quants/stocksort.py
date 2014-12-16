#!/usr/bin/python
#!coding=utf-8
import stockmanager

def __get_sort():
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
		result_day.append(stock)
		for day in e:
			volume = day[6]
			sum = sum + volume
			count = count + 1
		result_day.append(sum / count)
		result.append(result_day)
	result.sort(cmp = lambda x,y: cmp(x[1],y[1]))
	return result
