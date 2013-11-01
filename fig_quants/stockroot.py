#!/usr/bin/python
#!coding=utf-8
import stockdb
import stockparser
import stockconfig

class stockroot():
	parser = stockparser.stock_parser()
	db = stockdb.stockdb()
	thread_num = stockconfig.FIG_THREAD_NUM

	def splite_task(self):
		task = []
		for i in range(0, self.thread_num):
			task.append([])
		index = self.parser.get_stock_list()
		seed = 0
		for stock in index:
			task[seed % self.thread_num].append(stock)
			seed = seed + 1
		return task

x = stockroot()
x = x.splite_task()
print x[2]

