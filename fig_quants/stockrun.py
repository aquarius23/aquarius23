#!/usr/bin/python
#!coding=utf-8
import stockmanager

class stockrun():
	manager = stockmanager.stockmanager()
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

	def fix_index(self, adjust):
		index = self.current_index + adjust
		if index < 0:
			index = 0
		if index > self.size - 1:
			index = self.size - 1
		return index

	def run(self):
		index = 0
		for item in self.exchange:
			lable, feature = self.get_lable_feature(index)
			self.lable_feature(lable, feature)
			index = index + 1

	def get_lable_feature(self, index):
		lable = self.get_lable(index)
		feature = self.get_feature(index)
		return lable, feature

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

	def get_lable(self, index):
		return self.get_state(index, self.exchange, self.kline)

	def get_feature(self, index):
		self.current_index = index
		features = []
		macd_feature = self.feature_macd(self.exchange, index, self.macd)
		features.extend(macd_feature)

		kdj_feature = self.feature_kdj(self.exchange, index, self.kdj)
		features.extend(kdj_feature)

		boll_feature = self.feature_boll(self.exchange, index, self.boll)
		features.extend(boll_feature)

		ma_feature = self.feature_ma(self.exchange, index, self.ma)
		features.extend(ma_feature)

		volume_ma_feature = self.feature_volume_ma(self.exchange, index, self.volume_ma)
		features.extend(volume_ma_feature)

		price_range_feature = self.feature_price_range(self.exchange, index, self.price_range_low, self.price_range_high)
		features.extend(price_range_feature)

		volume_range_feature = self.feature_volume_range(self.exchange, index, self.volume_range_low, self.volume_range_high)
		features.extend(volume_range_feature)

		closeprice_range_feature = self.feature_closeprice_range(self.exchange, index, self.closeprice_range_low, self.closeprice_range_high)
		features.extend(closeprice_range_feature)

		kline_feature = self.feature_kline(self.exchange, index, self.kline)
		features.extend(kline_feature)

		exchange_feature = self.feature_exchange(index, self.exchange)
		features.extend(exchange_feature)
		return features

	def lable_feature(self, lable, feature):
		pass

	def get_state(self, index, exchange, kline):
		return []

	def feature_macd(self, exchange, index, macd):
		return []

	def feature_kdj(self, exchange, index, kdj):
		return []

	def feature_boll(self, exchange, index, boll):
		return []

	def feature_ma(self, exchange, index, ma):
		return []

	def feature_volume_ma(self, exchange, index, volume_ma):
		return []

	def feature_price_range(self, exchange, index, low, high):
		return []

	def feature_volume_range(self, exchange, index, low, high):
		return []

	def feature_closeprice_range(self, exchange, index, low, high):
		return []

	def feature_kline(self, exchange, index, kline):
		return []

	def feature_exchange(self, index, exchange):
		return []
