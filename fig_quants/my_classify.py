#!/usr/bin/python
#!coding=utf-8
import stocksort
import stockmanager
import stockcrfrun
import stockcrf

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
get_crf_modle(list, 'crftemp.bin')
