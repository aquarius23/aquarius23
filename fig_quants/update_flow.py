#!/usr/bin/python
#!coding=utf-8
import stockflow
import stockmanager

flow = stockflow.stockflow()
manager = stockmanager.stockmanager()
list = manager.get_stock_list()
for index in list:
	print index
	flow.update_flow(index)
