#!/usr/bin/python
#!coding=utf-8
import string
import stockutils
import stockdb
import stockparser
import stockconfig
from index import macd
from index import kdj
from index import boll
from index import ma
from index import volume_ma
from index import price_range
from index import volume_range
from index import closeprice_range
from index import kline

class stockmanager():
	parser = stockparser.stock_parser()
	db = stockdb.stockdb()
	macd = macd.macd()
	kdj = kdj.kdj()
	boll = boll.boll()
	ma = ma.ma()
	volume_ma = volume_ma.volume_ma()
	price_range = price_range.price_range()
	volume_range = volume_range.volume_range()
	closeprice_range = closeprice_range.closeprice_range()
	kline = kline.kline()

	def cal_macd(self, list):
		return self.macd.cal_macd(list)

	def cal_kdj(self, list):
		return self.kdj.cal_kdj(list)

	def cal_boll(self, list):
		return self.boll.cal_boll(list)

	def cal_ma(self, list):
		return self.ma.cal_ma(list)

	def cal_volume_ma(self, list):
		return self.volume_ma.cal_ma(list)

	def cal_price_range(self, list):
		return self.price_range.cal_range(list)

	def cal_volume_range(self, list):
		return self.volume_range.cal_range(list)

	def cal_closeprice_range(self, list):
		return self.closeprice_range.cal_range(list)

	def cal_kline(self, list):
		return self.kline.cal_kline(list)

	def get_stock_list(self):
		return self.parser.get_stock_list()

	def __get_stock_index_jidu(self, name, year, jidu):
		data = self.db.read_data_jidu(name, year, jidu)
		if len(data) <= 0:
			return []
		list = data.split('\n')
		ret = []
		for line in list:
			day_exchange = line.split(',')
			start = string.atof(day_exchange[1])
			end = string.atof(day_exchange[3])
			low = string.atof(day_exchange[4])
			high = string.atof(day_exchange[2])
			day_exchange[1] = start
			day_exchange[2] = end
			day_exchange[3] = low
			day_exchange[4] = high
			day_exchange[5] = string.atoi(day_exchange[5])
			day_exchange[6] = string.atoi(day_exchange[6])
			ret.append(day_exchange)
		return ret

	def get_stock_detailed(self, name, year, month, day):
		data = self.db.read_data_day(name, year, month, day)
		if len(data) <= 0:
			return []
		list = data.split('\n')
		ret = []
		for line in list:
			one_exchange = line.split(',')
			new = []
			hand = string.atoi(one_exchange[2])
			if hand == 0:
				continue
			price = string.atof(one_exchange[1])
			money = (int)(hand * price * 100)
			new.append(money)
			new.append(string.atoi(one_exchange[3]))
			ret.append(new)
		return ret

	def get_stock_index(self, name):
		today = stockutils.get_date().split('-')
		start = stockconfig.FIG_START_DAY.split('-')
		start_year = string.atoi(start[0])
		start_jidu = (string.atoi(start[1]) + 2) / 3
		end_year = string.atoi(today[0])
		end_jidu = (string.atoi(today[1]) + 2) / 3
		index = []
		while True:
			data = self.__get_stock_index_jidu(name, start_year, start_jidu)
			index.extend(data)
			if(start_year == end_year) and (start_jidu == end_jidu):
				break;
			start_year, start_jidu = stockutils.next_jidu(start_year, start_jidu)
		return index

