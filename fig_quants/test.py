#!/usr/bin/python
#!coding=utf-8
import stockmanager

manager = stockmanager.stockmanager()
x = manager.get_stock_index('002204')
x = manager.cal_kline(x)
for i in x:
	print i
