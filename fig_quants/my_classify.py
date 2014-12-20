#!/usr/bin/python
#!coding=utf-8
import string
import stocksort
import stockmanager
import arccos
import stockmodel

def get_max_filter(size, list):
	ret = []
	for stock in list:
		if size <= 0:
			break
		ret.append(stock[:])
		size = size - 1
	return ret

def c_continue(index, size):
	return 0

def c_break(index, size):
	return 0
manager = stockmanager.stockmanager()
sort = stocksort.get_sort(0)
list = get_max_filter(1, sort)
#stockmodel.get_stock_modle(list, 'crftemp.bin', c_continue, c_break)

def tag_filter(index, size, tag, p, m):
	ret = string.atoi(tag[-1])
	if ret >= 3 and p > 0.3 and m > 0.8:
		print str(p) + '  ' + str(m)
		return 1
	return 0

model = stockmodel.stockmodeltag()
model.open_model('crftemp.bin', tag_filter)
zxzj = model.get_result(['600030'])
output = []
for index in sort:
	index = index[0]
	print '------------'
	arg = []
	arg.append(index)
	ret = model.get_result(arg)
	print ret
	cos = arccos.vec_acos(zxzj, ret)
	x = []
	x.append(index)
	x.append(cos)
	output.append(x)
	print 'cos='+str(cos)
model.close_model()
output.sort(cmp = lambda x,y: cmp(x[1],y[1]))
for x in output:
	print x[0]+':'+str(x[1])
