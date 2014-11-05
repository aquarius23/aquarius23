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

	def reset(self):
		self.score.reset()

	def feed(self, exchange):
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

	#def filter(self, index):
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

	def filter_kline(self, low, high):
		return 1

	def filter_exchange(self, exchange):
		return 1

