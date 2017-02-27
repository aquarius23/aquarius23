#!/usr/bin/python
#!coding=utf-8
import time
import string
import rawdb

class stockdb():
	def __init__(self, db, start_day):
		self.mdb = db
		self.mstart_day = start_day

	def __list2str(self, list):
		return ','.join(list)

	def __stocklist2str(self, lists):
		lists.reverse()
		str = []
		for list in lists:
			str.append(self.__list2str(list))
		return '\n'.join(str)

	def __get_path_day(self, year, month, day):
		return 'detail/' + str(year) + '/' + str(month) + '/' + str(day)

	def __get_path_jidu(self, year, jidu):
		return 'index/' + str(year) + '/' + str(jidu)

	def __get_path_cal_index(self, name, index):
		return 'index2/' + name + '/' + index

	def write_data_day(self, name, list, year, month, day):
		path = self.__get_path_day(year, month, day)
		value = self.__stocklist2str(list)
		rawdb.write_file(path, name, value, self.mdb)

	def read_data_day(self, name, year, month, day):
		path = self.__get_path_day(year, month, day)
		for i in range(1, 3):
			value = rawdb.read_file(path, name, self.mdb)
			if value != '':
				return value
			time.sleep(1)
		return ''

	def has_data_day(self, name, year, month, day):
		path = self.__get_path_day(year, month, day)
		return rawdb.is_file_exist(path, name, self.mdb)

	def write_data_jidu(self, name, list, year, jidu):
		path = self.__get_path_jidu(year, jidu)
		value = self.__stocklist2str(list)
		rawdb.write_file(path, name, value, self.mdb)

	def read_data_jidu(self, name, year, jidu):
		path = self.__get_path_jidu(year, jidu)
		for i in range(1, 3):
			value = rawdb.read_file(path, name, self.mdb)
			if value != '':
				return value
			#time.sleep(1)
		return ''

	def write_data_crf(self, name, list):
		str = self.__stocklist2str(list)
		rawdb.write_file('crf', name, str, self.mdb)

	def read_data_crf(self, name):
		str = rawdb.read_file('crf', name, self.mdb)
		return str

	def write_data_flow(self, name, list):
		str = self.__stocklist2str(list)
		rawdb.write_file('flow', name, str, self.mdb)

	def read_data_flow(self, name):
		str = rawdb.read_file('flow', name, self.mdb)
		return str

	def get_last_update_day(self):
		day = rawdb.read_file('', 'last', self.mdb)
		if day == '':
			day = self.mstart_day
			rawdb.write_file('', 'last', day, self.mdb)
		return day

	def update_last_update_day(self, day_string):
		rawdb.write_file('', 'last', day_string, self.mdb)

