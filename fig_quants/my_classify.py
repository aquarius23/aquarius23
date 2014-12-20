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

def tag_filter(index, size, tag, p, m):
	ret = string.atoi(tag[-1])
	if ret >= 3 and p > 0.2 and m > 0.7:
		#print str(p) + '  ' + str(m)
		return 1
	return 0

def cal_cos(model, ref, list):
	output = []
	for index in list:
		index = index[0]
		arg = []
		arg.append(index)
		ret = model.get_result(arg)
		print ret
		cos = arccos.vec_acos(ref, ret)
		x = []
		x.append(index)
		x.append(cos)
		output.append(x)
		print 'cos = ' + str(cos)
	output.sort(cmp = lambda x,y: cmp(x[1],y[1]))
	return output

manager = stockmanager.stockmanager()
sort = stocksort.get_sort(0)
list = get_max_filter(20, sort)
#stockmodel.get_stock_modle(list, 'crftemp.bin', c_continue, c_break)

model = stockmodel.stockmodeltag()
model.open_model('crftemp.bin', tag_filter)
zxzj = model.get_result(['600030'])

print cal_cos(model, zxzj, list)
model.close_model()
