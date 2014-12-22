#!/usr/bin/python
#!coding=utf-8
import string
import stocksort
import stockmanager
import arccos
import stockmodel
import stockdb

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

def filter_cos(cos, max, thr):
	count = 0
	ret = []
	for item in cos:
		if item[1] < thr:
			count = count + 1
			val = item[:]
			ret.append(val)
			if count >= max:
				break
	return ret

def delete_index(list, index):
	for item in list:
		if index == item[0]:
			list.remove(item)
			break

def delete_filter(list, filter):
	for item in filter:
		delete_index(list, item[0])

def cos_to_string(list):
	for item in list:
		item[1] = str(item[1])
	return list

manager = stockmanager.stockmanager()
sort = stocksort.get_sort(0)

write_count = 0
while True:
	list = get_max_filter(20, sort)
	print list
	if len(list) < 10:
		break
	stockmodel.get_stock_modle(list, 'crftemp.bin', c_continue, c_break)

	model = stockmodel.stockmodeltag()
	model.open_model('crftemp.bin', tag_filter)
	arg = []
	arg.append(list[0][0])
	ref = model.get_result(arg)

	cos = cal_cos(model, ref, sort)
	cos = filter_cos(cos, 30, 35)
	print 'filter cos------'
	print cos
	if len(cos) < 10:
		break
	db = stockdb.stockdb()
	name = 'crf'+str(write_count)+'.bin'
	write_count = write_count + 1
	cos = cos_to_string(cos)
	db.write_data_crf(name, cos)
	delete_filter(sort, cos)
	model.close_model()
