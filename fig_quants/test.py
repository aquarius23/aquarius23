#!/usr/bin/python
#!coding=utf-8
import stockmanager
import score

manager = stockmanager.stockmanager()
x = manager.get_stock_index('002204')
x = manager.cal_kline(x)
score = score.score()
x =score.get_level()
for i in x:
	print i
