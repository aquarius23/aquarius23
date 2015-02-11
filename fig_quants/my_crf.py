#!/usr/bin/python
#!coding=utf-8
import sys
import string
import stocksort
import stockmodel

def c_continue(index, size):
	return 0

def c_break(index, size):
	return 0

stock_step = 20
if len(sys.argv) > 1:
	stock_step = string.atoi(sys.argv[1])

list = stocksort.get_sort(0)
size = len(list)
start = 0
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
	stockmodel.get_stock_modle(crflist, name, c_continue, c_break)

