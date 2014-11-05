#!/usr/bin/python
#!coding=utf-8
import stockmanager
import stockscore
import stockemu

class myemu(stockemu.stockemu):

	def filter_kdj(self, index, kdj):
		if kdj[index][2] < -5:
			return 1
		return 0

manager = stockmanager.stockmanager()
e = manager.get_stock_index('600015')
emu = myemu()
emu.feed(e)
emu.run()
x = emu.get_middle()
for i in x:
	print '----------------------'
	for j in i:
		print j
