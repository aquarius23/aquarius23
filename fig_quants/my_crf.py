#!/usr/bin/python
#!coding=utf-8
import stocksort
import stockmodel

def c_continue(index, size):
	return 0

def c_break(index, size):
	return 0

index = 0
while(True):
	list = stocksort.get_sort_cl(index)
	if list == []:
		break
	name = str(index) + '.crf'
	index = index + 1
	stockmodel.get_stock_modle(list, name, c_continue, c_break)

