#!/usr/bin/python
#!coding=utf-8
import stockmanager
import stockcrfrun
import stockcrf

manager = stockmanager.stockmanager()
list = manager.get_stock_list()
list.append('sh000001')
list.append('sz399001')
for index in list:
	print index
	e = manager.get_stock_index(index)
	if e == []:
		continue
	trainer = stockcrf.stockcrftrainer()
	run = stockcrfrun.stockcrfrun()
	run.feed(e)
	for tag, feature in run.tag_feature():
		trainer.set_tag_feature(tag, feature)
	trainer.get_model('crf/'+str(index)+'.bin')
