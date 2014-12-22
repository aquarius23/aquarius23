#!/usr/bin/python
#!coding=utf-8
import string
import stockcrfrun
import stockcrf
import stockmanager

def get_stock_modle(list, name, c_continue, c_break):
	manager = stockmanager.stockmanager()
	trainer = stockcrf.stockcrftrainer()
	run = stockcrfrun.stockcrfrun()
	for index in list:
		index = index[0]
		print index
		e = manager.get_stock_index(index)
		size = len(e)
		if e == []:
			continue
		run.feed(e)
		count  = 0
		for tag, feature in run.tag_feature():
			count = count + 1
			if count <= 30:
				continue
			if c_continue(count, size) == 1:
				continue
			if c_break(count, size) == 1:
				break
			trainer.set_tag_feature(tag, feature)
	trainer.get_model(name)
	trainer.clear()

class stockmodeltag(stockcrfrun.stockcrfrun):
	stockcrftag = stockcrf.stockcrftagger()
	manager = stockmanager.stockmanager()

	def open_model(self, file, filter):
		self.stockcrftag.open_model(file)
		self.tagfilter = filter

	def close_model(self):
		self.stockcrftag.close_model()

	def filter_exchange(self, index, exchange):
		tag, feature = self.tag_feature_by_index(index)
		if index < 30:
			return 0
		if feature != []:
			tag, p, m = self.stockcrftag.tag_lable(feature)
			if self.tagfilter(index, len(exchange), tag, p, m) == 1:
				return 1
		return 0

	def get_result(self, list):
		self.reset_score()
		for index in list:
			print 'emu run: ' + index
			e = self.manager.get_stock_index(index)
			if e == []:
				continue
			self.feed(e)
			self.run()
		return self.get_middle()[0]

