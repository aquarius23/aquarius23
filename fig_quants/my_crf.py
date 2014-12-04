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
	count = 0
	for tag, feature in run.tag_feature():
		count = count + 1
		trainer.set_tag_feature(tag, feature)
	print 'count = '+ str(count)
	if count > 0:
		trainer.get_model('crf/'+str(index)+'.bin')
	trainer.clear()
