#!/usr/bin/python
#!coding=utf-8
import string
import stocksort
import stockmodel

def tag_filter(index, size, tag, p, m):
	ret = string.atoi(tag[-1])
	if index < (size * 2 / 3):
		return 0
	if ret >= 3 and p > 0.3 and m > 0.8:
		print str(p) + '  ' + str(m)
		return 1
	return 0

list = stocksort.get_sort_cl(0)
model = stockmodel.stockmodeltag()
model.open_model('crftest.bin', tag_filter)
arg = []
for item in list:
	arg.append(item[0])
result = model.get_result(arg)
model.close_model()
print result
