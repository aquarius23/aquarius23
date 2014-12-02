#!/usr/bin/python
#!coding=utf-8
import stockmanager
import stockscore
import stockcrfrun
import stockcrf

class myemu(stockcrfrun.stockcrfrun):
	mycrftag = stockcrf.stockcrftagger()
	mycrftag.open_model('crf.bin')

	def get_state(self, index, exchange, kline):
		next = self.fix_index(1)
		today = kline[index][0]
		if today >= 1:
			today = 1
		elif today <= -1:
			today = -1
		else:
			today = 0

		tomorrow = kline[next][0]
		if tomorrow >= 1:
			tomorrow = 1
		elif tomorrow <= -1:
			tomorrow = -1
		else:
			tomorrow = 0

		return str(tomorrow)

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
		macd = macd[index][2]
		if macd >= 0:
			ret.append('macd=1')
		else:
			ret.append('macd=-1')
		return ret

	def feature_boll(self, exchange, index, macd):
		return []

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

	def filter_exchange(self, index, exchange):
		tag, feature = self.tag_feature_by_index(index)
		if feature != []:
			self.mycrftag.tag_lable(feature)
		return 1

manager = stockmanager.stockmanager()
list = manager.get_stock_list()
list = ['600015','600030','600036','600050','600029']
list = ['600015']
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
