#!/usr/bin/python
#!coding=utf-8
import stockmanager
import stockcrfrun
import stockcrf

manager = stockmanager.stockmanager()
trainer = stockcrf.stockcrftrainer()
list = manager.get_stock_list()
run = stockcrfrun.stockcrfrun()
#list = ['600015','600030','600036','600050','600029']
#list = ['002204']
for index in list:
	print index
	e = manager.get_stock_index(index)
	if e == []:
		continue
	run.feed(e)
	for tag, feature in run.tag_feature():
		trainer.set_tag_feature(tag, feature)
trainer.get_model('crf.bin')
