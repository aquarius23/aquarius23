#!/usr/bin/python
#!coding=utf-8
import string
import rawdb
import stockconfig

class stockdb():
	def __list2str(self, list):
		return ','.join(list)

	def __stocklist2str(self, lists):
		str = []
		for list in lists:
			str.append(self.__list2str(list))
		return '\n'.join(str)

	def __get_path_day(self, year, month, day):
		return 'detail/' + str(year) + '/' + str(month) + '/' + str(day)

	def __get_path_jidu(self, year, jidu):
		return 'index/' + str(year) + '/' + str(jidu)

	def write_data_day(self, name, list, year, month, day):
		path = self.__get_path_day(year, month, day)
		value = self.__stocklist2str(list)
		rawdb.write_file(path, name, value)

	def read_data_day(self, name, year, month, day):
		path = self.__get_path_day(year, month, day)
		for i in range(1, 3):
			value = rawdb.read_file(path, name)
			if value != '':
				return value
			sleep(1)
		return ''

	def has_data_day(self, name, year, month, day):
		path = self.__get_path_day(year, month, day)
		return rawdb.is_file_exist(path, name)

	def write_data_jidu(self, name, list, year, jidu):
		path = self.__get_path_jidu(year, jidu)
		value = self.__stocklist2str(list)
		rawdb.write_file(path, name, value)

	def read_data_jidu(self, name, year, jidu):
		path = self.__get_path_jidu(year, jidu)
		for i in range(1, 3):
			value = rawdb.read_file(path, name)
			if value != '':
				return value
			sleep(1)
		return ''

	def get_last_update_day(self):
		day = rawdb.read_file('', 'last')
		if day == '':
			day = stockconfig.FIG_START_DAY
			rawdb.write_file('', 'last', day)
		return day

	def update_last_update_day(self, day_string):
		rawdb.write_file('', 'last', day_string)

