#!/usr/bin/python
#!coding=utf-8
import stockmanager

def __normalize(list):
	sum = 0
	ret = []
	for item in list:
		sum = sum + item
	for item in list:
		nor = 0
		if sum != 0:
			nor = (float(item)/float(sum))*100.0
		ret.append(nor)
	return ret

manager = stockmanager.stockmanager()
list = manager.get_stock_list()
result = []
for i in range(0, 41):
	result.append(0)
for index in list:
	print index
	e = manager.get_stock_index(index)
	if e == []:
		continue
	kline = manager.cal_kline(e)
	for item in kline:
		state = item[0]
		if state < -10:
			state = -10
		elif state > 10:
			state = 10
		state = (int)(round((state * 2)))
		state = state + 20 #base0 = -10
		result[state] = result[state] + 1
nor = __normalize(result)
for i, item in enumerate(nor):
	print str((i - 20))+'='+str(item)
