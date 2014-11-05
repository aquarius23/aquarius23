#!/usr/bin/python
#!coding=utf-8
import stockmanager
import stockscore

class stockemu():
	score = stockscore.stockscore()
	manager = stockmanager.stockmanager()
	score.reset()
	macd = []
	kdj = []
	boll = []
	ma = []
	volume_ma = []
	price_range_low = []
	price_range_high = []
	volume_range_low = []
	volume_range_high = []
	closeprice_range_low = []
	closeprice_range_high = []
	kline = []
	exchange = []
	size = 0
	current_index = 0

	def reset(self):
		self.score.reset()

	def fix_index(self, adjust):
		if adjust > 0:
			adjust = 0
		index = self.current_index + adjust
		if index < 0:
			index = 0
		return index

	def feed(self, exchange):
		self.size = len(exchange)
		self.exchange = exchange
		self.macd = self.manager.cal_macd(exchange)
		self.kdj = self.manager.cal_kdj(exchange)
		self.boll = self.manager.cal_boll(exchange)
		self.ma = self.manager.cal_ma(exchange)
		self.volume_ma = self.manager.cal_volume_ma(exchange)
		self.price_range_low, self.price_range_high = self.manager.cal_price_range(exchange)
		self.volume_range_low, self.volume_range_high = self.manager.cal_volume_range(exchange)
		self.closeprice_range_low, self.closeprice_range_high = self.manager.cal_closeprice_range(exchange)
		self.kline = self.manager.cal_kline(exchange)

	def filter(self, index):
		self.current_index = index
		if self.filter_macd(index, self.macd) != 1:
			return 0
		if self.filter_kdj(index, self.kdj) != 1:
			return 0
		if self.filter_boll(index, self.boll) != 1:
			return 0
		if self.filter_ma(index, self.ma) != 1:
			return 0
		if self.filter_volume_ma(index, self.volume_ma) != 1:
			return 0
		if self.filter_price_range(index, self.price_range_low, self.price_range_high) != 1:
			return 0
		if self.filter_volume_range(index, self.volume_range_low, self,volume_range_high) != 1:
			return 0
		if self.filter_closeprice_range(index, self.closeprice_range_low, self.closeprice_range_high) != 1:
			return 0
		if self.filter_kline(self, self.kline) != 1:
			return 0
		if self.filter_exchange(self, self.exchange) != 1:
			return 0
		return 1

	def filter_macd(self, index, macd):
		return 1

	def filter_kdj(self, index, kdj):
		return 1

	def filter_boll(self, index, boll):
		return 1

	def filter_ma(self, index, ma):
		return 1

	def filter_volume_ma(self, index, volume_ma):
		return 1

	def filter_price_range(self, low, high):
		return 1

	def filter_volume_range(self, low, high):
		return 1

	def filter_closeprice_range(self, low, high):
		return 1

	def filter_kline(self, kline):
		return 1

	def filter_exchange(self, exchange):
		return 1

