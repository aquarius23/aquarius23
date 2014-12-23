#!/usr/bin/python
#!coding=utf-8
import stocksort
import stockmodel

def c_continue(index, size):
	return 0

def c_break(index, size):
	if index > (size * 2 / 3):
		return 1
	return 0

list = stocksort.get_sort_cl(0)
stockmodel.get_stock_modle(list, 'crftest.bin', c_continue, c_break)

