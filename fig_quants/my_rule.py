#!/usr/bin/python
#!coding=utf-8
import sys
import string
import stocksort
import stockmodel
import stockmanager

def tag_filter(index, size, tag, p, m):
	return 0

stock_step = 20
if len(sys.argv) > 1:
	stock_step = string.atoi(sys.argv[1])

model = stockmodel.stockmodeltag()
manager = stockmanager.stockmanager()
date = manager.get_stock_index('sh000001')[-1][0]
list = stocksort.get_sort(0)
start = 0
size = 40
ret = []
while(True):
	if list == []:
		break
	end = start + stock_step
	name = str(start) + '-' + str(end) + '.bin'
	if end > size:
		break
	crflist = list[start:end]
	start = end
	print name
	name = 'db/crf/' + name

	model.open_model(name, tag_filter)
	arg = []
	for item in crflist:
		stock_date = manager.get_stock_index(item[0])[-1][0]
		if stock_date == date:
			arg.append(item[0])
	result = model.last_result(arg)
	model.close_model()
	ret.extend(result)
ret.sort(cmp = lambda x,y: cmp(x[3],y[3]), reverse = True)

print len(ret)
for x in ret:
	print x
