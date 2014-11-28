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
		next = self.fix_index(1)
		today = kline[index][0]
		tomorrow = kline[next][0]
		return str(today) + '=' + str(tomorrow)

	def feature_kdj(self, exchange, index, kdj):
		adj1 = self.fix_index(-1)
		ret = []
		j =  kdj[index][2]
		if j < 20:
			ret.append('j=-1')
		elif j >80:
			ret.append('j=1')
		else:
			ret.append('j=0')
		return ret

	def feature_macd(self, exchange, index, macd):
		ret = []
		return ret

	def feature_boll(self, exchange, index, macd):
		return []

manager = stockmanager.stockmanager()
list = manager.get_stock_list()
list = ['600015','600030','600036','600050','600029']
list = ['600015']
for index in list:
	print index
	e = manager.get_stock_index(index)
	if e == []:
		continue
	run = myrun()
	run.feed(e)
	run.run()
