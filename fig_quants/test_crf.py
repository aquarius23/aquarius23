#!/usr/bin/python
#!coding=utf-8
import stockmanager
import stockrun

class myrun(stockrun.stockrun):

	def lable_feature(self, lable, feature):
		print '-------------------'
		print lable
		print feature

	def get_state(self, index, exchange, kline):
		return 'up'

	def feature_kdj(self, exchange, index, kdj):
		adj1 = self.fix_index(-1)
		ret = []
		ret.append('kdj')
		return ret

	def feature_macd(self, exchange, index, macd):
		ret = []
		ret.append('macd')
		return ret

	def feature_boll(self, exchange, index, macd):
		return []

manager = stockmanager.stockmanager()
list = manager.get_stock_list()
list = ['600015','600030','600036','600050','600029']
for index in list:
	print index
	e = manager.get_stock_index(index)
	if e == []:
		continue
	run = myrun()
	run.feed(e)
	run.run()
