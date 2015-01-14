#!/usr/bin/python
#!coding=utf-8
import string
import stockcrfrun
import stockcrf
import stockmanager
import stockflow
import stockconfig

def __cal_filter_index(pre, cur):
	ret = []
	start = cur - (stockconfig.FIG_CRF_CHAIN - 1)
	end = cur + stockconfig.FIG_CRF_DAY + 1
	if pre != -1:
		pre = pre + stockconfig.FIG_CRF_DAY + 1
	pre = pre + 1
	if start < pre:
		start = pre
	for i in range(start, end + 1):
		ret.append(i)
	return ret

def cal_filter(list):
	ret = []
	pre = -1
	for item in list:
		ret.extend(__cal_filter_index(pre, item))
		pre =  item
	return ret

def filter_skip(filter, index):
	for item in filter:
		if item == index:
			return 1
	return 0

def get_stock_modle(list, name, c_continue, c_break):
	manager = stockmanager.stockmanager()
	trainer = stockcrf.stockcrftrainer()
	run = stockcrfrun.stockcrfrun()
	flow = stockflow.stockflow()
	for index in list:
		index = index[0]
		print index
		e = manager.get_stock_index(index)
		size = len(e)
		if e == []:
			continue
		run.feed(e)
		rflow, rmiss = flow.read_flow(index)
		filter = cal_filter(rmiss)
		run.feed_flow(rflow)
		count  = 0
		for tag, feature in run.tag_feature():
			count = count + 1
			if count <= 30:
				continue
			if c_continue(count, size) == 1:
				continue
			if c_break(count, size) == 1:
				break
			if filter_skip(filter, count - 1) == 1:
				continue
			trainer.set_tag_feature(tag, feature)
	trainer.get_model(name)
	trainer.clear()

class stockmodeltag(stockcrfrun.stockcrfrun):
	stockcrftag = stockcrf.stockcrftagger()
	manager = stockmanager.stockmanager()
	cflow = stockflow.stockflow()

	def open_model(self, file, filter):
		self.stockcrftag.open_model(file)
		self.tagfilter = filter

	def close_model(self):
		self.stockcrftag.close_model()

	def filter_exchange(self, index, exchange):
		if filter_skip(self.flow_filter, index) == 1:
			return 0
		tag, feature = self.tag_feature_by_index(index)
		if index < 30:
			return 0
		if feature != []:
			tag, p, m = self.stockcrftag.tag_lable(feature)
			if self.tagfilter(index, len(exchange), tag, p, m) == 1:
				return 1
		return 0

	def last_result(self, list):
		ret = []
		for index in list:
			print 'emu run: ' + index
			e = self.manager.get_stock_index(index)
			if e == []:
				continue
			self.feed(e)
			rflow, rmiss = self.cflow.read_flow(index)
			filter = cal_filter(rmiss)
			if filter_skip(filter, len(e) - 1) == 1:
				continue
			self.feed_flow(rflow)
			tag, feature = self.last_tag_feature()
			if feature != []:
				item = []
				tag, p, m = self.stockcrftag.tag_lable(feature)
				item.append(index)
				item.append(tag)
				item.append(p)
				item.append(m)
				ret.append(item)
		return ret

	def get_result(self, list):
		self.reset_score()
		for index in list:
			print 'emu run: ' + index
			e = self.manager.get_stock_index(index)
			if e == []:
				continue
			self.feed(e)
			rflow, rmiss = self.cflow.read_flow(index)
			self.flow_filter = cal_filter(rmiss)
			self.feed_flow(rflow)
			self.run()
		return self.get_middle()[0]

