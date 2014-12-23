#!/usr/bin/python
#!coding=utf-8
import stocksort
import stockmodel

def c_continue(index, size):
	return 0

def c_break(index, size):
	return 0

sort = stocksort.get_sort_cl(0)
print sort
#stockmodel.get_stock_modle(list, 'crftemp.bin', c_continue, c_break)

