#!/usr/bin/python
#!coding=utf-8
import stockmanager
import stockscore
import stockcrfrun

class myemu(stockcrfrun.stockcrfrun):

	def filter_kdj(self, exchange, index, kdj):
		if kdj[index][2] > 0:
			return 0
		adj1 = self.fix_index(-1)
		if kdj[adj1][2] > kdj[index][2]:
			return 0
		return 1

	def filter_macd(self, exchange, index, macd):
		return 1

	def filter_boll(self, exchange, index, macd):
		return 1

manager = stockmanager.stockmanager()
list = manager.get_stock_list()
list = ['600015','600030','600036','600050','600029']
for index in list:
	print index
	e = manager.get_stock_index(index)
	if e == []:
		continue
	emu = myemu()
	emu.feed(e)
	emu.run()
x = emu.get_middle()
for i in x:
	print '----------------------'
	for j in i:
		print j
