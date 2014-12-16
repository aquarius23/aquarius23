#!/usr/bin/python
#!coding=utf-8
import string
import stocksort
import stockmanager
import stockcrfrun
import stockcrf
import arccos

def get_max_filter(size, list):
	ret = []
	for stock in list:
		if size <= 0:
			break
		ret.append(stock[:])
		size = size - 1
	return ret

def get_crf_modle(list, name):
	trainer = stockcrf.stockcrftrainer()
	trainer.clear()
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
			if count < 30:
				continue
			trainer.set_tag_feature(tag, feature)
	trainer.get_model(name)

manager = stockmanager.stockmanager()
sort = stocksort.get_sort(0)
list = get_max_filter(20, sort)
#get_crf_modle(list, 'crftemp.bin')

mycrftag = stockcrf.stockcrftagger()
mycrftag.open_model('crftemp.bin')

class myemu(stockcrfrun.stockcrfrun):
	def filter_exchange(self, index, exchange):
		tag, feature = self.tag_feature_by_index(index)
		if index < 30:
			return 0
		if feature != []:
			tag, p, m = mycrftag.tag_lable(feature)
			ret = string.atoi(tag[-1])
			if ret >= 3 and p > 0.3 and m > 0.8:
				#print str(p) + '  ' + str(m)
				return 1
		return 0
emu = myemu()

def get_result(list):
	emu.reset_score()
	for index in list:
		print 'emu run: '+index
		e = manager.get_stock_index(index)
		if e == []:
			continue
		emu.feed(e)
		emu.run()
	return emu.get_middle()[0]

zxzj = get_result(['600030'])
for index in list:
	index = index[0]
	print '------------'
	arg = []
	arg.append(index)
	ret = get_result(arg)
	print ret
	cos = arccos.vec_acos(zxzj, ret)
	print 'cos='+str(cos)
mycrftag.close_model()
