#!/usr/bin/python
#!coding=utf-8
import stockmanager
import stockcrfrun
import stockcrf

class myrun(stockcrfrun.stockcrfrun):

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

manager = stockmanager.stockmanager()
trainer = stockcrf.stockcrftrainer()
list = manager.get_stock_list()
list = ['600015','600030','600036','600050','600029']
list = ['sh000001']
for index in list:
	print index
	e = manager.get_stock_index(index)
	if e == []:
		continue
	run = myrun()
	run.feed(e)
	for tag, feature in run.tag_feature():
		trainer.set_tag_feature(tag, feature)
	trainer.get_model('crf.txt')

	crftag = stockcrf.stockcrftagger()
	crftag.open_model('crf.txt')
	size = len(e)
	run.reset()
	for i in range(size-5, size):
		tag, feature = run.get_lable_feature(i)
		tag, feature = run.set_tag_feature(tag, feature)
		if feature != []:
			crftag.tag_lable(feature)
