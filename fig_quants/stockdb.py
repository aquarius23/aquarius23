#!/usr/bin/python
#!coding=utf-8
import rawdb
import stockparser
p = stockparser.stock_parser()
m = p.get_detailed_exchange('600015', 2013, 10, 30)

def __list2str(list):
	return ','.join(list)

def __stocklist2str(lists):
	str = []
	for list in lists:
		str.append(__list2str(list))
	return '\n'.join(str)

