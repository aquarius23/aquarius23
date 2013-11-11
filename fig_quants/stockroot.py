#!/usr/bin/python
#!coding=utf-8
import time
import string
import stockdb
import stockparser
import stockconfig

def get_date():
	return time.strftime('%Y-%m-%d',time.localtime(time.time()))

def get_time():
	return time.strftime('%T',time.localtime(time.time()))

class stockroot():
	parser = stockparser.stock_parser()
	db = stockdb.stockdb()
	thread_num = stockconfig.FIG_THREAD_NUM
	started = 0

	def set_thread_num(self, num):
		self.thread_num = num

	def start(self):
		self.started = 1

	def stop(self):
		self.started = 0

	def __splite_task(self, list):
		task = []
		for i in range(0, self.thread_num):
			task.append([])
		seed = 0
		for stock in list:
			task[seed % self.thread_num].append(stock)
			seed = seed + 1
		return task

	def __next_jidu(self, year, jidu):
		if jidu >= 4:
			year = year + 1
			jidu = 0
		return year, jidu + 1

	def __get_next_day_by_sh(self, year, jidu, day_string):
		list = self.parser.get_index_list('000001', year, jidu, 0) #sh000001 index
		if len(list) == 0:
			return ''
		if cmp(list[0][0], day_string) > 0:
			last = ''
			for item in list:
				if cmp(item[0], day_string) <= 0:
					return last
				last = item[0]
			return last
		return ''

	def get_next_day(self, today):
		day = today.split('-')
		year = string.atoi(day[0])
		month = string.atoi(day[1])
		jidu = (month + 2) / 3
		next = self.__get_next_day_by_sh(year, jidu, today)
		if next == '':
			year, next_jidu = self.__next_jidu(year, jidu)
			next = self.__get_next_day_by_sh(year, next_jidu, today)
		return next

	def looper(self):
		while self.started == 1:
			today = get_date()
			last = self.db.get_last_update_day()
			if cmp(today, last):
				print 'true'
			time.sleep(1800)

x = stockroot()
x.start()
print x.get_next_day('2012-12-31')
x.looper()
