#!/usr/bin/python
#!coding=utf-8
import stockmanager

manager = stockmanager.stockmanager()
list = manager.get_stock_list()
result = []
for stock in list:
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
for x in result:
	print x[0]+'='+str(x[1])
