#!/usr/bin/python
#!coding=utf-8
import time
import string
import threading
import stockdb
import stockparser
import stockconfig

def get_date():
	return time.strftime('%Y-%m-%d',time.localtime(time.time()))

def get_time():
	return time.strftime('%T',time.localtime(time.time()))

class taskthread(threading.Thread):
	def __init__(self, list, day, update_jidu, thread_id, stock_parser, stock_db):
		threading.Thread.__init__(self)
		self.list = list
		self.day = day
		self.update_jidu = update_jidu
		self.thread_id = thread_id
		self.stock_parser = stock_parser
		self.stock_db = stock_db

	def run(self):
		split = self.day.split('-')
		year = string.atoi(split[0])
		month = string.atoi(split[1])
		day = string.atoi(split[2])
		jidu = (month + 2) / 3
		for item in self.list:
			if self.update_jidu:
				index = self.stock_parser.get_index_list(item, year, jidu, 1)
				if len(index) > 0:
					print 'update index day:' + self.day + '  id:' + str(self.thread_id) + '  stock:' + item
					self.stock_db.write_data_jidu(item, index, year, jidu)
				else:
					self.list.remove(item)
					continue
			if self.stock_db.has_data_day(item, year, month, day) == False:
				detail = self.stock_parser.get_detailed_exchange(item, year, month, day)
				print 'update detail day:' + self.day + '  id:' + str(self.thread_id) + '  stock:' + item
				if len(detail) > 0:
					self.stock_db.write_data_day(item, detail, year, month, day)
			else:
				validate = self.stock_db.read_data_day(item, year, month, day)
				if validate == '':
					detail = self.stock_parser.get_detailed_exchange(item, year, month, day)
					print 'reupdate detail day:' + self.day + '  id:' + str(self.thread_id) + '  stock:' + item
					if len(detail) > 0:
						self.stock_db.write_data_day(item, detail, year, month, day)
		print '---------exit thread:' + str(self.thread_id)

	def stop(self):
		self.thread_stop = True

class stockroot():
	parser = stockparser.stock_parser()
	db = stockdb.stockdb()
	thread_num = stockconfig.FIG_THREAD_NUM
	started = False

	def set_thread_num(self, num):
		self.thread_num = num

	def start(self):
		self.started = True

	def stop(self):
		self.started = False

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

	def __get_year_jidu(self, day_string):
		day = day_string.split('-')
		year = string.atoi(day[0])
		month = string.atoi(day[1])
		jidu = (month + 2) / 3
		return year, jidu

	def __is_same_jidu(self, day1, day2):
		year1, jidu1 = self.__get_year_jidu(day1)
		year2, jidu2 = self.__get_year_jidu(day2)
		if year1 == year2 and jidu1 == jidu2:
			return True
		else:
			return False

	def __get_next_day(self, today):
		year, jidu = self.__get_year_jidu(today)
		next = self.__get_next_day_by_sh(year, jidu, today)
		if next == '':
			year, next_jidu = self.__next_jidu(year, jidu)
			next = self.__get_next_day_by_sh(year, next_jidu, today)
		return next

	def __real_update(self, list, day, update_jidu):
		print day + '-' + str(update_jidu)
		threadx = []
		id = 1
		for item in list:
			task = taskthread(item, day, update_jidu, id, self.parser, self.db)
			task.start()
			threadx.append(task)
			id = id + 1
		for item in threadx:
			item.join()
		year, jidu = self.__get_year_jidu(day)
		sh = self.parser.get_index_list('000001', year, jidu, 0)
		self.db.write_data_jidu('sh000001', sh, year, jidu)
		sz = self.parser.get_index_list('399001', year, jidu, 0)
		self.db.write_data_jidu('sz399001', sh, year, jidu)
		print 'update--------------ok'

	def looper(self):
		last_jidu_update_day = '0000-00-00'
		task_list = []
		while self.started == True:
			today = get_date()
			last = self.db.get_last_update_day()
			if cmp(today, last):
				next = self.__get_next_day(last)
				if next != '':
					update_jidu = False
					current_jidu = self.__is_same_jidu(next, today)
					same_jidu = self.__is_same_jidu(next, last_jidu_update_day)
					if current_jidu == True or same_jidu == False:
						list = self.parser.get_stock_list()
						task_list = self.__splite_task(list)
						last_jidu_update_day = next
						update_jidu = True
					self.__real_update(task_list, next, update_jidu)
					self.db.update_last_update_day(next)
				else:
					time.sleep(1800)
			else:
				time.sleep(1800)

x = stockroot()
x.start()
x.looper()
